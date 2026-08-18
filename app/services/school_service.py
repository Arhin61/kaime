from uuid import UUID

from app.models import (
    AcademicTerm,
    ClassSession,
    Course,
    Enrollment,
    Student,
)
from app.repositories.school_repository import SchoolRepository
from app.schemas import (
    ClassSessionCreate,
    ClassSessionRead,
    ClassSessionUpdate,
    CourseCreate,
    CourseUpdate,
    EnrollmentCreate,
    EnrollmentRead,
    EnrollmentStatus,
    StudentCreate,
    StudentStatus,
    StudentUpdate,
    TermCreate,
    TermUpdate,
)
from app.services.exceptions import ResourceConflictError, ResourceNotFoundError


class SchoolService:
    """Student records, course catalogue, enrollment and timetable."""

    def __init__(self, repository: SchoolRepository):
        self.repository = repository

    # --- academic terms ---------------------------------------------------

    def create_term(self, payload: TermCreate) -> AcademicTerm:
        if payload.end_date < payload.start_date:
            raise ResourceConflictError("end_date must not be earlier than start_date.")
        if self.repository.get_term_by_name(payload.name):
            raise ResourceConflictError(f"Term {payload.name} already exists.")
        term = AcademicTerm.model_validate(payload)
        if term.is_current:
            self.repository.clear_current_term_flag()
        return self.repository.add(term)

    def list_terms(self) -> list[AcademicTerm]:
        return self.repository.list_terms()

    def get_term(self, term_id: int) -> AcademicTerm:
        term = self.repository.get_term(term_id)
        if term is None:
            raise ResourceNotFoundError(f"Term with id {term_id} was not found.")
        return term

    def get_current_term(self) -> AcademicTerm:
        term = self.repository.get_current_term()
        if term is None:
            raise ResourceNotFoundError("No term is marked as current.")
        return term

    def update_term(self, term_id: int, payload: TermUpdate) -> AcademicTerm:
        term = self.get_term(term_id)
        updates = payload.model_dump(exclude_none=True)
        for key, value in updates.items():
            setattr(term, key, value)
        if term.end_date < term.start_date:
            raise ResourceConflictError("end_date must not be earlier than start_date.")
        if term.is_current:
            self.repository.clear_current_term_flag(keep_id=term.id)
        self.repository.save()
        self.repository.refresh(term)
        return term

    def delete_term(self, term_id: int) -> None:
        term = self.get_term(term_id)
        if self.repository.list_enrollments(term_id=term_id):
            raise ResourceConflictError(
                "Term still has enrollments; drop them before deleting the term."
            )
        self.repository.delete(term)

    # --- students ---------------------------------------------------------

    def create_student(self, payload: StudentCreate) -> Student:
        index_number = payload.index_number.strip().upper()
        email = self._normalize_email(payload.email)
        if self.repository.get_student_by_index(index_number):
            raise ResourceConflictError(f"Student {index_number} already exists.")
        if self.repository.get_student_by_email(email):
            raise ResourceConflictError(f"Student with email {email} already exists.")

        data = payload.model_dump(exclude_none=True)
        data["index_number"] = index_number
        data["email"] = email
        data["status"] = str(payload.status)
        student = Student.model_validate(data)
        # Link to the notification subscriber list when the address is known.
        if self.repository.get_subscriber(email):
            student.subscriber_email = email
        return self.repository.add(student)

    def list_students(
        self,
        program: str | None = None,
        level: int | None = None,
        status: StudentStatus | None = None,
        search: str | None = None,
    ) -> list[Student]:
        return self.repository.list_students(
            program=program,
            level=level,
            status=str(status) if status else None,
            search=search,
        )

    def get_student(self, student_id: UUID) -> Student:
        student = self.repository.get_student(student_id)
        if student is None:
            raise ResourceNotFoundError(f"Student with id {student_id} was not found.")
        return student

    def get_student_by_index(self, index_number: str) -> Student:
        student = self.repository.get_student_by_index(index_number.strip().upper())
        if student is None:
            raise ResourceNotFoundError(f"Student {index_number} was not found.")
        return student

    def update_student(self, student_id: UUID, payload: StudentUpdate) -> Student:
        student = self.get_student(student_id)
        updates = payload.model_dump(exclude_none=True)

        if "index_number" in updates:
            updates["index_number"] = updates["index_number"].strip().upper()
            existing = self.repository.get_student_by_index(updates["index_number"])
            if existing and existing.id != student.id:
                raise ResourceConflictError(
                    f"Student {updates['index_number']} already exists."
                )
        if "email" in updates:
            updates["email"] = self._normalize_email(updates["email"])
            existing = self.repository.get_student_by_email(updates["email"])
            if existing and existing.id != student.id:
                raise ResourceConflictError(
                    f"Student with email {updates['email']} already exists."
                )
            subscriber = self.repository.get_subscriber(updates["email"])
            student.subscriber_email = updates["email"] if subscriber else None
        if "status" in updates:
            updates["status"] = str(updates["status"])

        for key, value in updates.items():
            setattr(student, key, value)
        self.repository.save()
        self.repository.refresh(student)
        return student

    def delete_student(self, student_id: UUID) -> None:
        student = self.get_student(student_id)
        if self.repository.list_enrollments(student_id=student_id):
            raise ResourceConflictError(
                "Student still has enrollments; drop them before deleting the record."
            )
        if self.repository.list_invoices(student_id=student_id):
            raise ResourceConflictError(
                "Student still has invoices; clear them before deleting the record."
            )
        self.repository.delete(student)

    # --- courses ----------------------------------------------------------

    def create_course(self, payload: CourseCreate) -> Course:
        code = payload.code.strip().upper()
        if self.repository.get_course_by_code(code):
            raise ResourceConflictError(f"Course {code} already exists.")
        course = Course.model_validate(payload)
        course.code = code
        return self.repository.add(course)

    def list_courses(
        self,
        department: str | None = None,
        level: int | None = None,
        is_active: bool | None = None,
    ) -> list[Course]:
        return self.repository.list_courses(
            department=department, level=level, is_active=is_active
        )

    def get_course(self, course_id: int) -> Course:
        course = self.repository.get_course(course_id)
        if course is None:
            raise ResourceNotFoundError(f"Course with id {course_id} was not found.")
        return course

    def update_course(self, course_id: int, payload: CourseUpdate) -> Course:
        course = self.get_course(course_id)
        updates = payload.model_dump(exclude_none=True)
        if "code" in updates:
            updates["code"] = updates["code"].strip().upper()
            existing = self.repository.get_course_by_code(updates["code"])
            if existing and existing.id != course.id:
                raise ResourceConflictError(f"Course {updates['code']} already exists.")
        for key, value in updates.items():
            setattr(course, key, value)
        self.repository.save()
        self.repository.refresh(course)
        return course

    def set_course_active(self, course_id: int, is_active: bool) -> Course:
        course = self.get_course(course_id)
        course.is_active = is_active
        self.repository.save()
        self.repository.refresh(course)
        return course

    def delete_course(self, course_id: int) -> None:
        course = self.get_course(course_id)
        if self.repository.count_enrollments_for_course(course_id):
            raise ResourceConflictError(
                "Course still has enrollments; drop them before deleting the course."
            )
        if self.repository.list_assessments(course_id=course_id):
            raise ResourceConflictError(
                "Course still has assessments; delete them before deleting the course."
            )
        if self.repository.list_class_sessions(course_id=course_id):
            raise ResourceConflictError(
                "Course still has timetable slots; delete them before deleting the course."
            )
        self.repository.delete(course)

    # --- enrollments ------------------------------------------------------

    def enroll_student(self, payload: EnrollmentCreate) -> EnrollmentRead:
        student = self.get_student(payload.student_id)
        course = self.get_course(payload.course_id)
        term = self.get_term(payload.term_id)

        if student.status != StudentStatus.ACTIVE:
            raise ResourceConflictError(
                f"Student {student.index_number} is {student.status} and cannot be enrolled."
            )
        if not course.is_active:
            raise ResourceConflictError(f"Course {course.code} is not active.")

        existing = self.repository.get_enrollment_by_keys(
            student.id, course.id, term.id
        )
        if existing is not None:
            if existing.status == EnrollmentStatus.DROPPED:
                existing.status = str(EnrollmentStatus.ENROLLED)
                self.repository.save()
                self.repository.refresh(existing)
                return self._to_enrollment_read(existing, student, course, term)
            raise ResourceConflictError(
                f"{student.index_number} is already enrolled in {course.code} for {term.name}."
            )

        enrollment = Enrollment(
            student_id=student.id,
            course_id=course.id,
            term_id=term.id,
        )
        enrollment = self.repository.add(enrollment)
        return self._to_enrollment_read(enrollment, student, course, term)

    def list_enrollments(
        self,
        student_id: UUID | None = None,
        course_id: int | None = None,
        term_id: int | None = None,
        status: EnrollmentStatus | None = None,
    ) -> list[EnrollmentRead]:
        rows = self.repository.list_enrollments(
            student_id=student_id,
            course_id=course_id,
            term_id=term_id,
            status=str(status) if status else None,
        )
        return [
            self._to_enrollment_read(enrollment, student, course, term)
            for enrollment, student, course, term in rows
        ]

    def get_enrollment(self, enrollment_id: UUID) -> Enrollment:
        enrollment = self.repository.get_enrollment(enrollment_id)
        if enrollment is None:
            raise ResourceNotFoundError(
                f"Enrollment with id {enrollment_id} was not found."
            )
        return enrollment

    def set_enrollment_status(
        self, enrollment_id: UUID, status: EnrollmentStatus
    ) -> EnrollmentRead:
        enrollment = self.get_enrollment(enrollment_id)
        enrollment.status = str(status)
        self.repository.save()
        self.repository.refresh(enrollment)
        student = self.get_student(enrollment.student_id)
        course = self.get_course(enrollment.course_id)
        term = self.get_term(enrollment.term_id)
        return self._to_enrollment_read(enrollment, student, course, term)

    def delete_enrollment(self, enrollment_id: UUID) -> None:
        enrollment = self.get_enrollment(enrollment_id)
        # Attendance and scores hang off the enrollment; clear them first.
        self.repository.delete_attendance_for_enrollments([enrollment.id])
        self.repository.delete_scores_for_enrollments([enrollment.id])
        self.repository.delete(enrollment)

    # --- timetable --------------------------------------------------------

    def create_class_session(self, payload: ClassSessionCreate) -> ClassSessionRead:
        course = self.get_course(payload.course_id)
        self.get_term(payload.term_id)
        if payload.end_time <= payload.start_time:
            raise ResourceConflictError("end_time must be later than start_time.")
        self._assert_no_room_clash(
            term_id=payload.term_id,
            day_of_week=payload.day_of_week,
            room=payload.room,
            start=payload.start_time,
            end=payload.end_time,
        )
        session = self.repository.add(ClassSession.model_validate(payload))
        return self._to_class_session_read(session, course)

    def list_class_sessions(
        self, term_id: int | None = None, course_id: int | None = None
    ) -> list[ClassSessionRead]:
        rows = self.repository.list_class_sessions(term_id=term_id, course_id=course_id)
        return [
            self._to_class_session_read(session, course) for session, course in rows
        ]

    def get_class_session(self, session_id: int) -> ClassSession:
        session = self.repository.get_class_session(session_id)
        if session is None:
            raise ResourceNotFoundError(
                f"Class session with id {session_id} was not found."
            )
        return session

    def update_class_session(
        self, session_id: int, payload: ClassSessionUpdate
    ) -> ClassSessionRead:
        session = self.get_class_session(session_id)
        updates = payload.model_dump(exclude_none=True)
        if "course_id" in updates:
            self.get_course(updates["course_id"])
        if "term_id" in updates:
            self.get_term(updates["term_id"])
        for key, value in updates.items():
            setattr(session, key, value)
        if session.end_time <= session.start_time:
            raise ResourceConflictError("end_time must be later than start_time.")
        self._assert_no_room_clash(
            term_id=session.term_id,
            day_of_week=session.day_of_week,
            room=session.room,
            start=session.start_time,
            end=session.end_time,
            exclude_id=session.id,
        )
        self.repository.save()
        self.repository.refresh(session)
        return self._to_class_session_read(session, self.get_course(session.course_id))

    def delete_class_session(self, session_id: int) -> None:
        session = self.get_class_session(session_id)
        self.repository.delete(session)

    # --- helpers ----------------------------------------------------------

    def _assert_no_room_clash(
        self,
        term_id: int,
        day_of_week: int,
        room: str | None,
        start,
        end,
        exclude_id: int | None = None,
    ) -> None:
        if not room:
            return
        for other in self.repository.find_room_clashes(
            term_id=term_id,
            day_of_week=day_of_week,
            room=room,
            exclude_id=exclude_id,
        ):
            if start < other.end_time and other.start_time < end:
                raise ResourceConflictError(
                    f"Room {room} is already booked "
                    f"{other.start_time:%H:%M}-{other.end_time:%H:%M} on that day."
                )

    @staticmethod
    def _to_enrollment_read(
        enrollment: Enrollment,
        student: Student,
        course: Course,
        term: AcademicTerm,
    ) -> EnrollmentRead:
        return EnrollmentRead(
            id=enrollment.id,
            student_id=enrollment.student_id,
            course_id=enrollment.course_id,
            term_id=enrollment.term_id,
            status=EnrollmentStatus(enrollment.status),
            enrolled_at=enrollment.enrolled_at,
            student_name=student.full_name,
            student_index_number=student.index_number,
            course_code=course.code,
            course_title=course.title,
            term_name=term.name,
        )

    @staticmethod
    def _to_class_session_read(
        session: ClassSession, course: Course
    ) -> ClassSessionRead:
        return ClassSessionRead(
            id=session.id,
            course_id=session.course_id,
            term_id=session.term_id,
            day_of_week=session.day_of_week,
            start_time=session.start_time,
            end_time=session.end_time,
            room=session.room,
            lecturer_name=session.lecturer_name,
            course_code=course.code,
            course_title=course.title,
        )

    @staticmethod
    def _normalize_email(email: str) -> str:
        return email.strip().lower()
