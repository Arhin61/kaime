from datetime import date
from uuid import UUID

from app.models import AttendanceRecord
from app.repositories.school_repository import SchoolRepository
from app.schemas import (
    AttendanceMark,
    AttendanceRead,
    AttendanceStatus,
    AttendanceSummaryRead,
)
from app.services.exceptions import ResourceConflictError, ResourceNotFoundError

# Statuses that count towards the attendance rate.
_CREDITED_STATUSES = {
    AttendanceStatus.PRESENT,
    AttendanceStatus.LATE,
    AttendanceStatus.EXCUSED,
}


class AttendanceService:
    """Register marking and attendance reporting."""

    def __init__(self, repository: SchoolRepository):
        self.repository = repository

    def mark_attendance(self, payload: AttendanceMark) -> list[AttendanceRead]:
        if not payload.entries:
            raise ResourceConflictError("At least one attendance entry is required.")

        course = self.repository.get_course(payload.course_id)
        if course is None:
            raise ResourceNotFoundError(
                f"Course with id {payload.course_id} was not found."
            )
        if self.repository.get_term(payload.term_id) is None:
            raise ResourceNotFoundError(
                f"Term with id {payload.term_id} was not found."
            )
        if payload.class_session_id is not None:
            class_session = self.repository.get_class_session(payload.class_session_id)
            if class_session is None:
                raise ResourceNotFoundError(
                    f"Class session with id {payload.class_session_id} was not found."
                )
            if class_session.course_id != payload.course_id:
                raise ResourceConflictError(
                    "class_session_id does not belong to the given course."
                )

        enrollment_ids = [entry.enrollment_id for entry in payload.entries]
        if len(set(enrollment_ids)) != len(enrollment_ids):
            raise ResourceConflictError(
                "Each enrollment may only appear once per sitting."
            )

        rows = self.repository.get_enrollments_with_students(enrollment_ids)
        by_id = {enrollment.id: (enrollment, student) for enrollment, student in rows}
        missing = set(enrollment_ids) - set(by_id)
        if missing:
            raise ResourceNotFoundError(
                f"Unknown enrollment ids: {', '.join(str(item) for item in missing)}."
            )

        results: list[AttendanceRead] = []
        for entry in payload.entries:
            enrollment, student = by_id[entry.enrollment_id]
            if (
                enrollment.course_id != payload.course_id
                or enrollment.term_id != payload.term_id
            ):
                raise ResourceConflictError(
                    f"Enrollment {enrollment.id} is not for {course.code} in that term."
                )

            record = self.repository.get_attendance_record(
                enrollment_id=enrollment.id,
                session_date=payload.session_date,
                class_session_id=payload.class_session_id,
            )
            if record is None:
                record = AttendanceRecord(
                    enrollment_id=enrollment.id,
                    class_session_id=payload.class_session_id,
                    session_date=payload.session_date,
                    status=str(entry.status),
                    remarks=entry.remarks,
                )
                self.repository.session.add(record)
            else:
                # Re-marking the same sitting overwrites the earlier entry.
                record.status = str(entry.status)
                record.remarks = entry.remarks
                self.repository.session.add(record)

            results.append(
                AttendanceRead(
                    id=record.id,
                    enrollment_id=record.enrollment_id,
                    class_session_id=record.class_session_id,
                    session_date=record.session_date,
                    status=entry.status,
                    remarks=record.remarks,
                    student_name=student.full_name,
                    student_index_number=student.index_number,
                )
            )

        self.repository.save()
        return results

    def list_attendance(
        self,
        course_id: int | None = None,
        term_id: int | None = None,
        student_id: UUID | None = None,
        session_date: date | None = None,
    ) -> list[AttendanceRead]:
        rows = self.repository.list_attendance(
            course_id=course_id,
            term_id=term_id,
            student_id=student_id,
            session_date=session_date,
        )
        return [
            AttendanceRead(
                id=record.id,
                enrollment_id=record.enrollment_id,
                class_session_id=record.class_session_id,
                session_date=record.session_date,
                status=AttendanceStatus(record.status),
                remarks=record.remarks,
                student_name=student.full_name,
                student_index_number=student.index_number,
            )
            for record, _enrollment, student in rows
        ]

    def course_summary(
        self, course_id: int, term_id: int
    ) -> list[AttendanceSummaryRead]:
        course = self.repository.get_course(course_id)
        if course is None:
            raise ResourceNotFoundError(f"Course with id {course_id} was not found.")

        rows = self.repository.list_attendance(course_id=course_id, term_id=term_id)
        tallies: dict[UUID, dict] = {}
        for record, enrollment, student in rows:
            tally = tallies.setdefault(
                enrollment.student_id,
                {
                    "student": student,
                    "sessions_held": 0,
                    AttendanceStatus.PRESENT: 0,
                    AttendanceStatus.LATE: 0,
                    AttendanceStatus.EXCUSED: 0,
                    AttendanceStatus.ABSENT: 0,
                },
            )
            status = AttendanceStatus(record.status)
            tally["sessions_held"] += 1
            tally[status] += 1

        summaries: list[AttendanceSummaryRead] = []
        for student_id, tally in tallies.items():
            student = tally["student"]
            held = tally["sessions_held"]
            credited = sum(tally[status] for status in _CREDITED_STATUSES)
            summaries.append(
                AttendanceSummaryRead(
                    student_id=student_id,
                    student_name=student.full_name,
                    student_index_number=student.index_number,
                    course_id=course_id,
                    course_code=course.code,
                    sessions_held=held,
                    present=tally[AttendanceStatus.PRESENT],
                    late=tally[AttendanceStatus.LATE],
                    excused=tally[AttendanceStatus.EXCUSED],
                    absent=tally[AttendanceStatus.ABSENT],
                    attendance_rate=round(credited / held * 100, 2) if held else 0.0,
                )
            )
        summaries.sort(key=lambda item: item.student_name)
        return summaries

    def delete_record(self, record_id: UUID) -> None:
        record = self.repository.session.get(AttendanceRecord, record_id)
        if record is None:
            raise ResourceNotFoundError(
                f"Attendance record with id {record_id} was not found."
            )
        self.repository.delete(record)
