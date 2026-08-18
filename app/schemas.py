from datetime import date, datetime, time
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlmodel import SQLModel


class UserBase(BaseModel):
    first_name: str = Field(max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str = Field(max_length=100)
    email: EmailStr = Field(max_length=255)
    phone_number: str = Field(max_length=20)


class UserIn(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime | None = Field(default=None)


class UserUpdateMe(BaseModel):
    first_name: str | None = Field(default=None, max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)


class UsersList(BaseModel):
    users: list[UserOut]
    count: int


class EventEmailTemplate(StrEnum):
    ANNOUNCEMENT = "announcement.html"
    DEADLINE_REMINDER = "deadline_reminder.html"
    EVENT_REMINDER = "event_reminder.html"
    EXAM_REMINDER = "exam_reminder.html"
    REGISTRATION_CLOSING = "registration_closing.html"
    REGISTRATION_OPEN = "registration_open.html"
    REGISTRATION_REMINDER = "registration_reminder.html"
    RESULTS_PUBLISHED = "results_published.html"
    RESULTS_PUBLISHED_REMINDER = "results_published_reminder.html"
    UPCOMING_EVENT_REMINDER = "upcoming_event_reminder.html"
    VAC_RE_OPENING_REMINDER = "vac-re-opening_reminder.html"


class SubscriberCreate(SQLModel):
    name: str
    program: str
    email: str
    surname: str
    other_names: str | None


class SubscriberUpdate(SQLModel):
    name: str | None = None
    program: str | None = None
    surname: str | None = None
    other_names: str | None = None


class SubscriberRead(SQLModel):
    name: str
    program: str
    email: str
    surname: str
    other_names: str


class EventCreate(SQLModel):
    title: str
    body: str
    start_date: datetime
    end_date: datetime | None = None
    notification_days_before: int | None = None
    notification_offsets: list[int] | None = None
    email_template: EventEmailTemplate
    is_active: bool = True


class EventUpdate(SQLModel):
    title: str | None = None
    body: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    notification_days_before: int | None = None
    notification_offsets: list[int] | None = None
    email_template: EventEmailTemplate | None = None
    is_active: bool | None = None


class EventRead(SQLModel):
    id: int
    title: str
    body: str
    start_date: datetime
    end_date: datetime | None
    notification_days_before: int | None
    notification_offsets: list[int] | None
    email_template: EventEmailTemplate
    is_active: bool


# --- School management ---------------------------------------------------


class StudentStatus(StrEnum):
    ACTIVE = "active"
    DEFERRED = "deferred"
    SUSPENDED = "suspended"
    GRADUATED = "graduated"
    WITHDRAWN = "withdrawn"


class EnrollmentStatus(StrEnum):
    ENROLLED = "enrolled"
    DROPPED = "dropped"
    COMPLETED = "completed"


class AttendanceStatus(StrEnum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"


class AssessmentKind(StrEnum):
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    MIDTERM = "midterm"
    PROJECT = "project"
    EXAM = "exam"


class InvoiceStatus(StrEnum):
    UNPAID = "unpaid"
    PARTIAL = "partial"
    PAID = "paid"
    VOID = "void"


class PaymentMethod(StrEnum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"
    CARD = "card"
    SCHOLARSHIP = "scholarship"


# Academic terms


class TermCreate(SQLModel):
    name: str = Field(max_length=100)
    academic_year: str = Field(max_length=20)
    start_date: date
    end_date: date
    is_current: bool = False


class TermUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=100)
    academic_year: str | None = Field(default=None, max_length=20)
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None


class TermRead(SQLModel):
    id: int
    name: str
    academic_year: str
    start_date: date
    end_date: date
    is_current: bool


# Students


class StudentCreate(SQLModel):
    index_number: str = Field(max_length=50)
    email: EmailStr = Field(max_length=255)
    first_name: str = Field(max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str = Field(max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)
    program: str = Field(max_length=150)
    level: int = Field(default=100, ge=0)
    gender: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = None
    status: StudentStatus = StudentStatus.ACTIVE
    enrolled_on: date | None = None


class StudentUpdate(SQLModel):
    index_number: str | None = Field(default=None, max_length=50)
    email: EmailStr | None = Field(default=None, max_length=255)
    first_name: str | None = Field(default=None, max_length=100)
    middle_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)
    program: str | None = Field(default=None, max_length=150)
    level: int | None = Field(default=None, ge=0)
    gender: str | None = Field(default=None, max_length=20)
    date_of_birth: date | None = None
    status: StudentStatus | None = None


class StudentRead(SQLModel):
    id: UUID
    index_number: str
    email: EmailStr
    subscriber_email: str | None
    first_name: str
    middle_name: str | None
    last_name: str
    full_name: str
    phone_number: str | None
    program: str
    level: int
    gender: str | None
    date_of_birth: date | None
    status: StudentStatus
    enrolled_on: date


# Courses


class CourseCreate(SQLModel):
    code: str = Field(max_length=20)
    title: str = Field(max_length=200)
    description: str | None = None
    credit_hours: int = Field(default=3, ge=0)
    department: str | None = Field(default=None, max_length=150)
    level: int | None = Field(default=None, ge=0)
    lecturer_name: str | None = Field(default=None, max_length=150)
    is_active: bool = True


class CourseUpdate(SQLModel):
    code: str | None = Field(default=None, max_length=20)
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    credit_hours: int | None = Field(default=None, ge=0)
    department: str | None = Field(default=None, max_length=150)
    level: int | None = Field(default=None, ge=0)
    lecturer_name: str | None = Field(default=None, max_length=150)
    is_active: bool | None = None


class CourseRead(SQLModel):
    id: int
    code: str
    title: str
    description: str | None
    credit_hours: int
    department: str | None
    level: int | None
    lecturer_name: str | None
    is_active: bool


# Enrollments


class EnrollmentCreate(SQLModel):
    student_id: UUID
    course_id: int
    term_id: int


class EnrollmentUpdate(SQLModel):
    status: EnrollmentStatus


class EnrollmentRead(SQLModel):
    id: UUID
    student_id: UUID
    course_id: int
    term_id: int
    status: EnrollmentStatus
    enrolled_at: datetime | None
    student_name: str | None = None
    student_index_number: str | None = None
    course_code: str | None = None
    course_title: str | None = None
    term_name: str | None = None


# Timetable


class ClassSessionCreate(SQLModel):
    course_id: int
    term_id: int
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    room: str | None = Field(default=None, max_length=100)
    lecturer_name: str | None = Field(default=None, max_length=150)


class ClassSessionUpdate(SQLModel):
    course_id: int | None = None
    term_id: int | None = None
    day_of_week: int | None = Field(default=None, ge=0, le=6)
    start_time: time | None = None
    end_time: time | None = None
    room: str | None = Field(default=None, max_length=100)
    lecturer_name: str | None = Field(default=None, max_length=150)


class ClassSessionRead(SQLModel):
    id: int
    course_id: int
    term_id: int
    day_of_week: int
    start_time: time
    end_time: time
    room: str | None
    lecturer_name: str | None
    course_code: str | None = None
    course_title: str | None = None


# Attendance


class AttendanceEntry(SQLModel):
    enrollment_id: UUID
    status: AttendanceStatus = AttendanceStatus.PRESENT
    remarks: str | None = None


class AttendanceMark(SQLModel):
    """Bulk register marking for one course sitting."""

    course_id: int
    term_id: int
    session_date: date
    class_session_id: int | None = None
    entries: list[AttendanceEntry]


class AttendanceRead(SQLModel):
    id: UUID
    enrollment_id: UUID
    class_session_id: int | None
    session_date: date
    status: AttendanceStatus
    remarks: str | None
    student_name: str | None = None
    student_index_number: str | None = None


class AttendanceSummaryRead(SQLModel):
    student_id: UUID
    student_name: str
    student_index_number: str
    course_id: int
    course_code: str
    sessions_held: int
    present: int
    late: int
    excused: int
    absent: int
    attendance_rate: float


# Grades


class AssessmentCreate(SQLModel):
    course_id: int
    term_id: int
    title: str = Field(max_length=200)
    kind: AssessmentKind = AssessmentKind.ASSIGNMENT
    max_score: Decimal = Field(default=Decimal("100"), gt=0)
    weight: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    due_date: datetime | None = None


class AssessmentUpdate(SQLModel):
    title: str | None = Field(default=None, max_length=200)
    kind: AssessmentKind | None = None
    max_score: Decimal | None = Field(default=None, gt=0)
    weight: Decimal | None = Field(default=None, ge=0, le=100)
    due_date: datetime | None = None


class AssessmentRead(SQLModel):
    id: int
    course_id: int
    term_id: int
    title: str
    kind: AssessmentKind
    max_score: Decimal
    weight: Decimal
    due_date: datetime | None
    course_code: str | None = None


class ScoreEntry(SQLModel):
    enrollment_id: UUID
    score: Decimal = Field(ge=0)
    remarks: str | None = None


class ScoreRecord(SQLModel):
    """Bulk score entry for a single assessment."""

    assessment_id: int
    entries: list[ScoreEntry]


class ScoreRead(SQLModel):
    id: UUID
    assessment_id: int
    enrollment_id: UUID
    score: Decimal
    remarks: str | None
    graded_at: datetime | None
    student_name: str | None = None
    student_index_number: str | None = None
    assessment_title: str | None = None
    max_score: Decimal | None = None


class CourseResultRead(SQLModel):
    enrollment_id: UUID
    student_id: UUID
    student_name: str
    student_index_number: str
    course_id: int
    course_code: str
    course_title: str
    credit_hours: int
    weighted_score: float
    graded_weight: float
    letter_grade: str
    grade_point: float


class StudentResultsRead(SQLModel):
    student_id: UUID
    student_name: str
    student_index_number: str
    term_id: int
    term_name: str
    results: list[CourseResultRead]
    total_credits: int
    gpa: float


# Fees


class FeeStructureCreate(SQLModel):
    term_id: int
    name: str = Field(max_length=150)
    description: str | None = None
    amount: Decimal = Field(ge=0)
    program: str | None = Field(default=None, max_length=150)
    level: int | None = Field(default=None, ge=0)
    due_date: date


class FeeStructureUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=150)
    description: str | None = None
    amount: Decimal | None = Field(default=None, ge=0)
    program: str | None = Field(default=None, max_length=150)
    level: int | None = Field(default=None, ge=0)
    due_date: date | None = None


class FeeStructureRead(SQLModel):
    id: int
    term_id: int
    name: str
    description: str | None
    amount: Decimal
    program: str | None
    level: int | None
    due_date: date
    term_name: str | None = None


class InvoiceCreate(SQLModel):
    student_id: UUID
    term_id: int
    fee_structure_id: int | None = None
    description: str | None = Field(default=None, max_length=200)
    amount: Decimal | None = Field(default=None, ge=0)
    due_date: date | None = None


class InvoiceRead(SQLModel):
    id: UUID
    student_id: UUID
    term_id: int
    fee_structure_id: int | None
    description: str
    amount: Decimal
    issued_on: date
    due_date: date
    status: InvoiceStatus
    amount_paid: Decimal
    balance: Decimal
    student_name: str | None = None
    student_index_number: str | None = None


class PaymentCreate(SQLModel):
    invoice_id: UUID
    amount: Decimal = Field(gt=0)
    method: PaymentMethod = PaymentMethod.CASH
    reference: str | None = Field(default=None, max_length=100)
    paid_on: date | None = None


class PaymentRead(SQLModel):
    id: UUID
    invoice_id: UUID
    amount: Decimal
    method: PaymentMethod
    reference: str | None
    paid_on: date
    recorded_at: datetime | None


class StudentBalanceRead(SQLModel):
    student_id: UUID
    student_name: str
    student_index_number: str
    total_billed: Decimal
    total_paid: Decimal
    balance: Decimal
    invoices: list[InvoiceRead]


class BillingRunRead(SQLModel):
    fee_structure_id: int
    invoices_created: int
    students_skipped: int
