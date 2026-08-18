from datetime import date, datetime, time, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from pydantic import EmailStr
from sqlalchemy import JSON, Column, DateTime, UniqueConstraint
from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    phone_number: str = Field(max_length=20)
    email_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    password_hash: str = Field(exclude=True)


class User(UserBase, table=True):
    first_name: str = Field(max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str = Field(max_length=100)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )


class Subscriber(SQLModel, table=True):
    __tablename__ = "subscribers"

    name: str = Field(index=True)
    program: str
    email: str = Field(primary_key=True)
    surname: str = Field(index=True)
    other_names: str | None = Field(index=True)

    @property
    def full_name(self) -> str:
        joined = " ".join(
            part for part in [self.surname, self.other_names] if part
        ).strip()
        return joined or self.name


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str
    start_date: datetime
    end_date: datetime | None = Field(default=None)
    notification_days_before: int | None = Field(default=None, gt=-1)
    notification_offsets: list[int] | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )
    email_template: str = Field(default="event_reminder.html")
    is_active: bool = Field(default=True, nullable=False)


class NotificationDispatch(SQLModel, table=True):
    __tablename__ = "notification_dispatches"
    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "recipient_email",
            "channel",
            "days_before",
            "scheduled_for",
            "status",
            name="uq_notification_dispatch_key",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: int = Field(foreign_key="events.id", nullable=False, index=True)
    recipient_email: str = Field(nullable=False, index=True)
    channel: str = Field(default="email", nullable=False, index=True)
    days_before: int = Field(nullable=False)
    scheduled_for: date = Field(nullable=False)
    sent_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    status: str = Field(default="sent", nullable=False)
    error_message: str | None = Field(default=None)


# --- School management ---------------------------------------------------


class AcademicTerm(SQLModel, table=True):
    __tablename__ = "academic_terms"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=100)
    academic_year: str = Field(max_length=20)
    start_date: date
    end_date: date
    is_current: bool = Field(default=False, nullable=False)


class Student(SQLModel, table=True):
    __tablename__ = "students"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    index_number: str = Field(unique=True, index=True, max_length=50)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    subscriber_email: str | None = Field(
        default=None,
        foreign_key="subscribers.email",
        index=True,
    )
    first_name: str = Field(max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str = Field(index=True, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)
    program: str = Field(index=True, max_length=150)
    level: int = Field(default=100, ge=0)
    gender: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = Field(default=None)
    status: str = Field(default="active", index=True, max_length=20)
    enrolled_on: date = Field(default_factory=lambda: get_datetime_utc().date())
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )

    @property
    def full_name(self) -> str:
        parts = [self.first_name, self.middle_name, self.last_name]
        return " ".join(part for part in parts if part).strip()


class Course(SQLModel, table=True):
    __tablename__ = "courses"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True, max_length=20)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None)
    credit_hours: int = Field(default=3, ge=0)
    department: str | None = Field(default=None, index=True, max_length=150)
    level: int | None = Field(default=None, ge=0)
    lecturer_name: str | None = Field(default=None, max_length=150)
    is_active: bool = Field(default=True, nullable=False)


class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "course_id",
            "term_id",
            name="uq_enrollment_student_course_term",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    student_id: UUID = Field(foreign_key="students.id", nullable=False, index=True)
    course_id: int = Field(foreign_key="courses.id", nullable=False, index=True)
    term_id: int = Field(foreign_key="academic_terms.id", nullable=False, index=True)
    status: str = Field(default="enrolled", index=True, max_length=20)
    enrolled_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )


class ClassSession(SQLModel, table=True):
    """A recurring weekly timetable slot for a course within a term."""

    __tablename__ = "class_sessions"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", nullable=False, index=True)
    term_id: int = Field(foreign_key="academic_terms.id", nullable=False, index=True)
    day_of_week: int = Field(ge=0, le=6, index=True)
    start_time: time
    end_time: time
    room: str | None = Field(default=None, max_length=100)
    lecturer_name: str | None = Field(default=None, max_length=150)


class AttendanceRecord(SQLModel, table=True):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint(
            "enrollment_id",
            "session_date",
            "class_session_id",
            name="uq_attendance_enrollment_date_session",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    enrollment_id: UUID = Field(
        foreign_key="enrollments.id", nullable=False, index=True
    )
    class_session_id: int | None = Field(
        default=None, foreign_key="class_sessions.id", index=True
    )
    session_date: date = Field(index=True)
    status: str = Field(default="present", index=True, max_length=20)
    remarks: str | None = Field(default=None)
    recorded_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )


class Assessment(SQLModel, table=True):
    __tablename__ = "assessments"

    id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id", nullable=False, index=True)
    term_id: int = Field(foreign_key="academic_terms.id", nullable=False, index=True)
    title: str = Field(max_length=200)
    kind: str = Field(default="assignment", max_length=30)
    max_score: Decimal = Field(default=Decimal("100"), max_digits=6, decimal_places=2)
    weight: Decimal = Field(default=Decimal("0"), max_digits=5, decimal_places=2)
    due_date: datetime | None = Field(default=None)


class AssessmentScore(SQLModel, table=True):
    __tablename__ = "assessment_scores"
    __table_args__ = (
        UniqueConstraint(
            "assessment_id",
            "enrollment_id",
            name="uq_assessment_score_assessment_enrollment",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    assessment_id: int = Field(
        foreign_key="assessments.id", nullable=False, index=True
    )
    enrollment_id: UUID = Field(
        foreign_key="enrollments.id", nullable=False, index=True
    )
    score: Decimal = Field(max_digits=6, decimal_places=2)
    remarks: str | None = Field(default=None)
    graded_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )


class FeeStructure(SQLModel, table=True):
    __tablename__ = "fee_structures"

    id: Optional[int] = Field(default=None, primary_key=True)
    term_id: int = Field(foreign_key="academic_terms.id", nullable=False, index=True)
    name: str = Field(max_length=150)
    description: str | None = Field(default=None)
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    program: str | None = Field(default=None, index=True, max_length=150)
    level: int | None = Field(default=None, ge=0, index=True)
    due_date: date


class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    student_id: UUID = Field(foreign_key="students.id", nullable=False, index=True)
    term_id: int = Field(foreign_key="academic_terms.id", nullable=False, index=True)
    fee_structure_id: int | None = Field(
        default=None, foreign_key="fee_structures.id", index=True
    )
    description: str = Field(max_length=200)
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    issued_on: date = Field(default_factory=lambda: get_datetime_utc().date())
    due_date: date
    status: str = Field(default="unpaid", index=True, max_length=20)


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    invoice_id: UUID = Field(foreign_key="invoices.id", nullable=False, index=True)
    amount: Decimal = Field(max_digits=12, decimal_places=2)
    method: str = Field(default="cash", max_length=30)
    reference: str | None = Field(default=None, max_length=100)
    paid_on: date = Field(default_factory=lambda: get_datetime_utc().date())
    recorded_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )


# Backward-compatibility aliases for existing imports.
Subscribers = Subscriber
Events = Event
Mock_Subscribers = Subscriber
