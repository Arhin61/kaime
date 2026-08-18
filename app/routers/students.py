from uuid import UUID

from fastapi import APIRouter, Query, status

from app.dependencies import FinanceServiceDep, GradingServiceDep, SchoolServiceDep
from app.schemas import (
    EnrollmentRead,
    StudentBalanceRead,
    StudentCreate,
    StudentRead,
    StudentResultsRead,
    StudentStatus,
    StudentUpdate,
)

router = APIRouter(prefix="/dashboard/students", tags=["Students"])


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, service: SchoolServiceDep):
    return service.create_student(payload)


@router.get("", response_model=list[StudentRead])
def list_students(
    service: SchoolServiceDep,
    program: str | None = None,
    level: int | None = None,
    student_status: StudentStatus | None = Query(default=None, alias="status"),
    search: str | None = None,
):
    return service.list_students(
        program=program, level=level, status=student_status, search=search
    )


@router.get("/by-index/{index_number}", response_model=StudentRead)
def get_student_by_index(index_number: str, service: SchoolServiceDep):
    return service.get_student_by_index(index_number)


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: UUID, service: SchoolServiceDep):
    return service.get_student(student_id)


@router.patch("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: UUID, payload: StudentUpdate, service: SchoolServiceDep
):
    return service.update_student(student_id, payload)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: UUID, service: SchoolServiceDep):
    service.delete_student(student_id)


@router.get("/{student_id}/enrollments", response_model=list[EnrollmentRead])
def list_student_enrollments(
    student_id: UUID,
    service: SchoolServiceDep,
    term_id: int | None = None,
):
    return service.list_enrollments(student_id=student_id, term_id=term_id)


@router.get("/{student_id}/results", response_model=StudentResultsRead)
def get_student_results(
    student_id: UUID, term_id: int, service: GradingServiceDep
):
    return service.student_results(student_id, term_id)


@router.get("/{student_id}/balance", response_model=StudentBalanceRead)
def get_student_balance(
    student_id: UUID,
    service: FinanceServiceDep,
    term_id: int | None = None,
):
    return service.student_balance(student_id, term_id=term_id)
