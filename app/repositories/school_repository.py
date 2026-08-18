from datetime import date
from uuid import UUID

from sqlmodel import Session, col, or_, select

from app.models import (
    AcademicTerm,
    Assessment,
    AssessmentScore,
    AttendanceRecord,
    ClassSession,
    Course,
    Enrollment,
    FeeStructure,
    Invoice,
    Payment,
    Student,
    Subscriber,
)


class SchoolRepository:
    """Data access for the school management domain."""

    def __init__(self, session: Session):
        self.session = session

    # --- shared -----------------------------------------------------------

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity) -> None:
        self.session.delete(entity)
        self.session.commit()

    def save(self) -> None:
        self.session.commit()

    def refresh(self, entity) -> None:
        self.session.refresh(entity)

    # --- academic terms ---------------------------------------------------

    def list_terms(self) -> list[AcademicTerm]:
        return list(
            self.session.exec(
                select(AcademicTerm).order_by(col(AcademicTerm.start_date).desc())
            )
        )

    def get_term(self, term_id: int) -> AcademicTerm | None:
        return self.session.get(AcademicTerm, term_id)

    def get_term_by_name(self, name: str) -> AcademicTerm | None:
        return self.session.exec(
            select(AcademicTerm).where(AcademicTerm.name == name)
        ).first()

    def get_current_term(self) -> AcademicTerm | None:
        return self.session.exec(
            select(AcademicTerm).where(AcademicTerm.is_current == True)  # noqa: E712
        ).first()

    def clear_current_term_flag(self, keep_id: int | None = None) -> None:
        statement = select(AcademicTerm).where(AcademicTerm.is_current == True)  # noqa: E712
        for term in self.session.exec(statement):
            if keep_id is not None and term.id == keep_id:
                continue
            term.is_current = False
            self.session.add(term)

    # --- students ---------------------------------------------------------

    def list_students(
        self,
        program: str | None = None,
        level: int | None = None,
        status: str | None = None,
        search: str | None = None,
    ) -> list[Student]:
        statement = select(Student)
        if program:
            statement = statement.where(Student.program == program)
        if level is not None:
            statement = statement.where(Student.level == level)
        if status:
            statement = statement.where(Student.status == status)
        if search:
            pattern = f"%{search.lower()}%"
            statement = statement.where(
                or_(
                    col(Student.first_name).ilike(pattern),
                    col(Student.last_name).ilike(pattern),
                    col(Student.index_number).ilike(pattern),
                    col(Student.email).ilike(pattern),
                )
            )
        statement = statement.order_by(col(Student.last_name), col(Student.first_name))
        return list(self.session.exec(statement))

    def get_student(self, student_id: UUID) -> Student | None:
        return self.session.get(Student, student_id)

    def get_student_by_index(self, index_number: str) -> Student | None:
        return self.session.exec(
            select(Student).where(Student.index_number == index_number)
        ).first()

    def get_student_by_email(self, email: str) -> Student | None:
        return self.session.exec(
            select(Student).where(col(Student.email) == email)
        ).first()

    def get_subscriber(self, email: str) -> Subscriber | None:
        return self.session.get(Subscriber, email)

    # --- courses ----------------------------------------------------------

    def list_courses(
        self,
        department: str | None = None,
        level: int | None = None,
        is_active: bool | None = None,
    ) -> list[Course]:
        statement = select(Course)
        if department:
            statement = statement.where(Course.department == department)
        if level is not None:
            statement = statement.where(Course.level == level)
        if is_active is not None:
            statement = statement.where(Course.is_active == is_active)
        return list(self.session.exec(statement.order_by(col(Course.code))))

    def get_course(self, course_id: int) -> Course | None:
        return self.session.get(Course, course_id)

    def get_course_by_code(self, code: str) -> Course | None:
        return self.session.exec(select(Course).where(Course.code == code)).first()

    # --- enrollments ------------------------------------------------------

    def list_enrollments(
        self,
        student_id: UUID | None = None,
        course_id: int | None = None,
        term_id: int | None = None,
        status: str | None = None,
    ) -> list[tuple[Enrollment, Student, Course, AcademicTerm]]:
        statement = (
            select(Enrollment, Student, Course, AcademicTerm)
            .join(Student, col(Enrollment.student_id) == col(Student.id))
            .join(Course, col(Enrollment.course_id) == col(Course.id))
            .join(AcademicTerm, col(Enrollment.term_id) == col(AcademicTerm.id))
        )
        if student_id is not None:
            statement = statement.where(Enrollment.student_id == student_id)
        if course_id is not None:
            statement = statement.where(Enrollment.course_id == course_id)
        if term_id is not None:
            statement = statement.where(Enrollment.term_id == term_id)
        if status:
            statement = statement.where(Enrollment.status == status)
        statement = statement.order_by(
            col(Course.code), col(Student.last_name), col(Student.first_name)
        )
        return list(self.session.exec(statement))

    def get_enrollment(self, enrollment_id: UUID) -> Enrollment | None:
        return self.session.get(Enrollment, enrollment_id)

    def get_enrollment_by_keys(
        self, student_id: UUID, course_id: int, term_id: int
    ) -> Enrollment | None:
        return self.session.exec(
            select(Enrollment).where(
                Enrollment.student_id == student_id,
                Enrollment.course_id == course_id,
                Enrollment.term_id == term_id,
            )
        ).first()

    def get_enrollments_with_students(
        self, enrollment_ids: list[UUID]
    ) -> list[tuple[Enrollment, Student]]:
        if not enrollment_ids:
            return []
        statement = (
            select(Enrollment, Student)
            .join(Student, col(Enrollment.student_id) == col(Student.id))
            .where(col(Enrollment.id).in_(enrollment_ids))
        )
        return list(self.session.exec(statement))

    def count_enrollments_for_course(self, course_id: int) -> int:
        return len(
            list(
                self.session.exec(
                    select(Enrollment).where(Enrollment.course_id == course_id)
                )
            )
        )

    # --- timetable --------------------------------------------------------

    def list_class_sessions(
        self, term_id: int | None = None, course_id: int | None = None
    ) -> list[tuple[ClassSession, Course]]:
        statement = select(ClassSession, Course).join(
            Course, col(ClassSession.course_id) == col(Course.id)
        )
        if term_id is not None:
            statement = statement.where(ClassSession.term_id == term_id)
        if course_id is not None:
            statement = statement.where(ClassSession.course_id == course_id)
        statement = statement.order_by(
            col(ClassSession.day_of_week), col(ClassSession.start_time)
        )
        return list(self.session.exec(statement))

    def get_class_session(self, session_id: int) -> ClassSession | None:
        return self.session.get(ClassSession, session_id)

    def find_room_clashes(
        self,
        term_id: int,
        day_of_week: int,
        room: str,
        exclude_id: int | None = None,
    ) -> list[ClassSession]:
        statement = select(ClassSession).where(
            ClassSession.term_id == term_id,
            ClassSession.day_of_week == day_of_week,
            ClassSession.room == room,
        )
        if exclude_id is not None:
            statement = statement.where(col(ClassSession.id) != exclude_id)
        return list(self.session.exec(statement))

    # --- attendance -------------------------------------------------------

    def get_attendance_record(
        self,
        enrollment_id: UUID,
        session_date: date,
        class_session_id: int | None,
    ) -> AttendanceRecord | None:
        statement = select(AttendanceRecord).where(
            AttendanceRecord.enrollment_id == enrollment_id,
            AttendanceRecord.session_date == session_date,
        )
        if class_session_id is None:
            statement = statement.where(col(AttendanceRecord.class_session_id).is_(None))
        else:
            statement = statement.where(
                AttendanceRecord.class_session_id == class_session_id
            )
        return self.session.exec(statement).first()

    def list_attendance(
        self,
        course_id: int | None = None,
        term_id: int | None = None,
        student_id: UUID | None = None,
        session_date: date | None = None,
    ) -> list[tuple[AttendanceRecord, Enrollment, Student]]:
        statement = (
            select(AttendanceRecord, Enrollment, Student)
            .join(Enrollment, col(AttendanceRecord.enrollment_id) == col(Enrollment.id))
            .join(Student, col(Enrollment.student_id) == col(Student.id))
        )
        if course_id is not None:
            statement = statement.where(Enrollment.course_id == course_id)
        if term_id is not None:
            statement = statement.where(Enrollment.term_id == term_id)
        if student_id is not None:
            statement = statement.where(Enrollment.student_id == student_id)
        if session_date is not None:
            statement = statement.where(AttendanceRecord.session_date == session_date)
        statement = statement.order_by(
            col(AttendanceRecord.session_date).desc(),
            col(Student.last_name),
        )
        return list(self.session.exec(statement))

    def delete_attendance_for_enrollments(self, enrollment_ids: list[UUID]) -> None:
        if not enrollment_ids:
            return
        statement = select(AttendanceRecord).where(
            col(AttendanceRecord.enrollment_id).in_(enrollment_ids)
        )
        for record in self.session.exec(statement):
            self.session.delete(record)
        # Flush so the children are gone before a parent delete is issued.
        self.session.flush()

    # --- assessments and scores -------------------------------------------

    def list_assessments(
        self, course_id: int | None = None, term_id: int | None = None
    ) -> list[tuple[Assessment, Course]]:
        statement = select(Assessment, Course).join(
            Course, col(Assessment.course_id) == col(Course.id)
        )
        if course_id is not None:
            statement = statement.where(Assessment.course_id == course_id)
        if term_id is not None:
            statement = statement.where(Assessment.term_id == term_id)
        return list(self.session.exec(statement.order_by(col(Assessment.id))))

    def get_assessment(self, assessment_id: int) -> Assessment | None:
        return self.session.get(Assessment, assessment_id)

    def get_score(
        self, assessment_id: int, enrollment_id: UUID
    ) -> AssessmentScore | None:
        return self.session.exec(
            select(AssessmentScore).where(
                AssessmentScore.assessment_id == assessment_id,
                AssessmentScore.enrollment_id == enrollment_id,
            )
        ).first()

    def list_scores_for_assessment(
        self, assessment_id: int
    ) -> list[tuple[AssessmentScore, Enrollment, Student]]:
        statement = (
            select(AssessmentScore, Enrollment, Student)
            .join(Enrollment, col(AssessmentScore.enrollment_id) == col(Enrollment.id))
            .join(Student, col(Enrollment.student_id) == col(Student.id))
            .where(AssessmentScore.assessment_id == assessment_id)
            .order_by(col(Student.last_name), col(Student.first_name))
        )
        return list(self.session.exec(statement))

    def list_scores_for_enrollments(
        self, enrollment_ids: list[UUID]
    ) -> list[tuple[AssessmentScore, Assessment]]:
        if not enrollment_ids:
            return []
        statement = (
            select(AssessmentScore, Assessment)
            .join(Assessment, col(AssessmentScore.assessment_id) == col(Assessment.id))
            .where(col(AssessmentScore.enrollment_id).in_(enrollment_ids))
        )
        return list(self.session.exec(statement))

    def delete_scores_for_assessment(self, assessment_id: int) -> None:
        statement = select(AssessmentScore).where(
            AssessmentScore.assessment_id == assessment_id
        )
        for score in self.session.exec(statement):
            self.session.delete(score)
        self.session.flush()

    def delete_scores_for_enrollments(self, enrollment_ids: list[UUID]) -> None:
        if not enrollment_ids:
            return
        statement = select(AssessmentScore).where(
            col(AssessmentScore.enrollment_id).in_(enrollment_ids)
        )
        for score in self.session.exec(statement):
            self.session.delete(score)
        self.session.flush()

    # --- fees -------------------------------------------------------------

    def list_fee_structures(
        self, term_id: int | None = None
    ) -> list[tuple[FeeStructure, AcademicTerm]]:
        statement = select(FeeStructure, AcademicTerm).join(
            AcademicTerm, col(FeeStructure.term_id) == col(AcademicTerm.id)
        )
        if term_id is not None:
            statement = statement.where(FeeStructure.term_id == term_id)
        return list(self.session.exec(statement.order_by(col(FeeStructure.due_date))))

    def get_fee_structure(self, structure_id: int) -> FeeStructure | None:
        return self.session.get(FeeStructure, structure_id)

    def list_invoices(
        self,
        student_id: UUID | None = None,
        term_id: int | None = None,
        status: str | None = None,
    ) -> list[tuple[Invoice, Student]]:
        statement = select(Invoice, Student).join(
            Student, col(Invoice.student_id) == col(Student.id)
        )
        if student_id is not None:
            statement = statement.where(Invoice.student_id == student_id)
        if term_id is not None:
            statement = statement.where(Invoice.term_id == term_id)
        if status:
            statement = statement.where(Invoice.status == status)
        statement = statement.order_by(col(Invoice.due_date), col(Student.last_name))
        return list(self.session.exec(statement))

    def get_invoice(self, invoice_id: UUID) -> Invoice | None:
        return self.session.get(Invoice, invoice_id)

    def get_invoice_for_structure(
        self, student_id: UUID, fee_structure_id: int
    ) -> Invoice | None:
        return self.session.exec(
            select(Invoice).where(
                Invoice.student_id == student_id,
                Invoice.fee_structure_id == fee_structure_id,
            )
        ).first()

    def list_invoices_for_structure(self, fee_structure_id: int) -> list[Invoice]:
        return list(
            self.session.exec(
                select(Invoice).where(Invoice.fee_structure_id == fee_structure_id)
            )
        )

    def list_payments(self, invoice_id: UUID) -> list[Payment]:
        return list(
            self.session.exec(
                select(Payment)
                .where(Payment.invoice_id == invoice_id)
                .order_by(col(Payment.paid_on))
            )
        )

    def list_payments_for_invoices(self, invoice_ids: list[UUID]) -> list[Payment]:
        if not invoice_ids:
            return []
        return list(
            self.session.exec(
                select(Payment).where(col(Payment.invoice_id).in_(invoice_ids))
            )
        )

    def delete_payments_for_invoice(self, invoice_id: UUID) -> None:
        for payment in self.list_payments(invoice_id):
            self.session.delete(payment)
        self.session.flush()
