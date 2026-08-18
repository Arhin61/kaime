from decimal import Decimal
from uuid import UUID

from app.models import Assessment, AssessmentScore
from app.repositories.school_repository import SchoolRepository
from app.schemas import (
    AssessmentCreate,
    AssessmentKind,
    AssessmentRead,
    AssessmentUpdate,
    CourseResultRead,
    EnrollmentStatus,
    ScoreRead,
    ScoreRecord,
    StudentResultsRead,
)
from app.services.exceptions import ResourceConflictError, ResourceNotFoundError

# Percentage floor -> (letter, grade point).
GRADE_SCALE: tuple[tuple[float, str, float], ...] = (
    (80.0, "A", 4.0),
    (75.0, "B+", 3.5),
    (70.0, "B", 3.0),
    (65.0, "C+", 2.5),
    (60.0, "C", 2.0),
    (55.0, "D+", 1.5),
    (50.0, "D", 1.0),
    (0.0, "F", 0.0),
)


def grade_for(percentage: float) -> tuple[str, float]:
    for floor, letter, point in GRADE_SCALE:
        if percentage >= floor:
            return letter, point
    return "F", 0.0


class GradingService:
    """Assessments, score entry and result computation."""

    def __init__(self, repository: SchoolRepository):
        self.repository = repository

    # --- assessments ------------------------------------------------------

    def create_assessment(self, payload: AssessmentCreate) -> AssessmentRead:
        course = self.repository.get_course(payload.course_id)
        if course is None:
            raise ResourceNotFoundError(
                f"Course with id {payload.course_id} was not found."
            )
        if self.repository.get_term(payload.term_id) is None:
            raise ResourceNotFoundError(
                f"Term with id {payload.term_id} was not found."
            )
        self._assert_weight_budget(
            course_id=payload.course_id,
            term_id=payload.term_id,
            added_weight=payload.weight,
        )

        data = payload.model_dump()
        data["kind"] = str(payload.kind)
        assessment = self.repository.add(Assessment.model_validate(data))
        return self._to_assessment_read(assessment, course.code)

    def list_assessments(
        self, course_id: int | None = None, term_id: int | None = None
    ) -> list[AssessmentRead]:
        rows = self.repository.list_assessments(course_id=course_id, term_id=term_id)
        return [
            self._to_assessment_read(assessment, course.code)
            for assessment, course in rows
        ]

    def get_assessment(self, assessment_id: int) -> Assessment:
        assessment = self.repository.get_assessment(assessment_id)
        if assessment is None:
            raise ResourceNotFoundError(
                f"Assessment with id {assessment_id} was not found."
            )
        return assessment

    def update_assessment(
        self, assessment_id: int, payload: AssessmentUpdate
    ) -> AssessmentRead:
        assessment = self.get_assessment(assessment_id)
        updates = payload.model_dump(exclude_none=True)
        if "weight" in updates:
            self._assert_weight_budget(
                course_id=assessment.course_id,
                term_id=assessment.term_id,
                added_weight=updates["weight"],
                exclude_id=assessment.id,
            )
        if "kind" in updates:
            updates["kind"] = str(updates["kind"])
        for key, value in updates.items():
            setattr(assessment, key, value)
        self.repository.save()
        self.repository.refresh(assessment)
        course = self.repository.get_course(assessment.course_id)
        return self._to_assessment_read(assessment, course.code if course else None)

    def delete_assessment(self, assessment_id: int) -> None:
        assessment = self.get_assessment(assessment_id)
        self.repository.delete_scores_for_assessment(assessment_id)
        self.repository.delete(assessment)

    # --- scores -----------------------------------------------------------

    def record_scores(self, payload: ScoreRecord) -> list[ScoreRead]:
        if not payload.entries:
            raise ResourceConflictError("At least one score entry is required.")

        assessment = self.get_assessment(payload.assessment_id)
        enrollment_ids = [entry.enrollment_id for entry in payload.entries]
        if len(set(enrollment_ids)) != len(enrollment_ids):
            raise ResourceConflictError(
                "Each enrollment may only appear once per assessment."
            )

        rows = self.repository.get_enrollments_with_students(enrollment_ids)
        by_id = {enrollment.id: (enrollment, student) for enrollment, student in rows}
        missing = set(enrollment_ids) - set(by_id)
        if missing:
            raise ResourceNotFoundError(
                f"Unknown enrollment ids: {', '.join(str(item) for item in missing)}."
            )

        results: list[ScoreRead] = []
        for entry in payload.entries:
            enrollment, student = by_id[entry.enrollment_id]
            if (
                enrollment.course_id != assessment.course_id
                or enrollment.term_id != assessment.term_id
            ):
                raise ResourceConflictError(
                    f"Enrollment {enrollment.id} is not for this assessment's course and term."
                )
            if entry.score > assessment.max_score:
                raise ResourceConflictError(
                    f"Score {entry.score} exceeds the maximum of {assessment.max_score}."
                )

            score = self.repository.get_score(assessment.id, enrollment.id)
            if score is None:
                score = AssessmentScore(
                    assessment_id=assessment.id,
                    enrollment_id=enrollment.id,
                    score=entry.score,
                    remarks=entry.remarks,
                )
            else:
                score.score = entry.score
                score.remarks = entry.remarks
            self.repository.session.add(score)

            results.append(
                ScoreRead(
                    id=score.id,
                    assessment_id=score.assessment_id,
                    enrollment_id=score.enrollment_id,
                    score=score.score,
                    remarks=score.remarks,
                    graded_at=score.graded_at,
                    student_name=student.full_name,
                    student_index_number=student.index_number,
                    assessment_title=assessment.title,
                    max_score=assessment.max_score,
                )
            )

        self.repository.save()
        return results

    def list_scores(self, assessment_id: int) -> list[ScoreRead]:
        assessment = self.get_assessment(assessment_id)
        rows = self.repository.list_scores_for_assessment(assessment_id)
        return [
            ScoreRead(
                id=score.id,
                assessment_id=score.assessment_id,
                enrollment_id=score.enrollment_id,
                score=score.score,
                remarks=score.remarks,
                graded_at=score.graded_at,
                student_name=student.full_name,
                student_index_number=student.index_number,
                assessment_title=assessment.title,
                max_score=assessment.max_score,
            )
            for score, _enrollment, student in rows
        ]

    # --- results ----------------------------------------------------------

    def course_results(self, course_id: int, term_id: int) -> list[CourseResultRead]:
        if self.repository.get_course(course_id) is None:
            raise ResourceNotFoundError(f"Course with id {course_id} was not found.")
        rows = self.repository.list_enrollments(course_id=course_id, term_id=term_id)
        return self._results_for(rows)

    def student_results(self, student_id: UUID, term_id: int) -> StudentResultsRead:
        student = self.repository.get_student(student_id)
        if student is None:
            raise ResourceNotFoundError(f"Student with id {student_id} was not found.")
        term = self.repository.get_term(term_id)
        if term is None:
            raise ResourceNotFoundError(f"Term with id {term_id} was not found.")

        rows = self.repository.list_enrollments(student_id=student_id, term_id=term_id)
        results = self._results_for(rows)

        total_credits = sum(result.credit_hours for result in results)
        weighted_points = sum(
            result.grade_point * result.credit_hours for result in results
        )
        gpa = round(weighted_points / total_credits, 2) if total_credits else 0.0

        return StudentResultsRead(
            student_id=student.id,
            student_name=student.full_name,
            student_index_number=student.index_number,
            term_id=term.id,
            term_name=term.name,
            results=results,
            total_credits=total_credits,
            gpa=gpa,
        )

    def _results_for(self, rows) -> list[CourseResultRead]:
        rows = [row for row in rows if row[0].status != EnrollmentStatus.DROPPED]
        if not rows:
            return []

        enrollment_ids = [enrollment.id for enrollment, _s, _c, _t in rows]
        scored = self.repository.list_scores_for_enrollments(enrollment_ids)

        earned: dict[UUID, float] = {}
        graded_weight: dict[UUID, float] = {}
        for score, assessment in scored:
            if assessment.max_score <= 0 or assessment.weight <= 0:
                continue
            fraction = float(score.score) / float(assessment.max_score)
            weight = float(assessment.weight)
            earned[score.enrollment_id] = (
                earned.get(score.enrollment_id, 0.0) + fraction * weight
            )
            graded_weight[score.enrollment_id] = (
                graded_weight.get(score.enrollment_id, 0.0) + weight
            )

        results: list[CourseResultRead] = []
        for enrollment, student, course, _term in rows:
            covered = graded_weight.get(enrollment.id, 0.0)
            points = earned.get(enrollment.id, 0.0)
            # Normalise over the weight actually graded so partial terms still rank.
            percentage = round(points / covered * 100, 2) if covered else 0.0
            letter, grade_point = grade_for(percentage)
            results.append(
                CourseResultRead(
                    enrollment_id=enrollment.id,
                    student_id=student.id,
                    student_name=student.full_name,
                    student_index_number=student.index_number,
                    course_id=course.id,
                    course_code=course.code,
                    course_title=course.title,
                    credit_hours=course.credit_hours,
                    weighted_score=percentage,
                    graded_weight=round(covered, 2),
                    letter_grade=letter,
                    grade_point=grade_point,
                )
            )
        return results

    # --- helpers ----------------------------------------------------------

    def _assert_weight_budget(
        self,
        course_id: int,
        term_id: int,
        added_weight: Decimal,
        exclude_id: int | None = None,
    ) -> None:
        existing = sum(
            assessment.weight
            for assessment, _course in self.repository.list_assessments(
                course_id=course_id, term_id=term_id
            )
            if assessment.id != exclude_id
        )
        if existing + added_weight > Decimal("100"):
            raise ResourceConflictError(
                f"Total assessment weight for this course would be {existing + added_weight}%, "
                "which exceeds 100%."
            )

    @staticmethod
    def _to_assessment_read(
        assessment: Assessment, course_code: str | None
    ) -> AssessmentRead:
        return AssessmentRead(
            id=assessment.id,
            course_id=assessment.course_id,
            term_id=assessment.term_id,
            title=assessment.title,
            kind=AssessmentKind(assessment.kind),
            max_score=assessment.max_score,
            weight=assessment.weight,
            due_date=assessment.due_date,
            course_code=course_code,
        )
