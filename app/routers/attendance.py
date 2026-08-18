from datetime import date
from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import AttendanceServiceDep
from app.schemas import AttendanceMark, AttendanceRead, AttendanceSummaryRead

router = APIRouter(prefix="/dashboard/attendance", tags=["Attendance"])


@router.post("", response_model=list[AttendanceRead], status_code=status.HTTP_201_CREATED)
def mark_attendance(payload: AttendanceMark, service: AttendanceServiceDep):
    return service.mark_attendance(payload)


@router.get("", response_model=list[AttendanceRead])
def list_attendance(
    service: AttendanceServiceDep,
    course_id: int | None = None,
    term_id: int | None = None,
    student_id: UUID | None = None,
    session_date: date | None = None,
):
    return service.list_attendance(
        course_id=course_id,
        term_id=term_id,
        student_id=student_id,
        session_date=session_date,
    )


@router.get("/summary", response_model=list[AttendanceSummaryRead])
def get_attendance_summary(
    course_id: int, term_id: int, service: AttendanceServiceDep
):
    return service.course_summary(course_id, term_id)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance_record(record_id: UUID, service: AttendanceServiceDep):
    service.delete_record(record_id)
