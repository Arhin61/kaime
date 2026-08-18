from uuid import UUID

from fastapi import APIRouter, Query, status

from app.dependencies import SchoolServiceDep
from app.schemas import (
    EnrollmentCreate,
    EnrollmentRead,
    EnrollmentStatus,
    EnrollmentUpdate,
)

router = APIRouter(prefix="/dashboard/enrollments", tags=["Enrollments"])


@router.post("", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def enroll_student(payload: EnrollmentCreate, service: SchoolServiceDep):
    return service.enroll_student(payload)


@router.get("", response_model=list[EnrollmentRead])
def list_enrollments(
    service: SchoolServiceDep,
    student_id: UUID | None = None,
    course_id: int | None = None,
    term_id: int | None = None,
    enrollment_status: EnrollmentStatus | None = Query(default=None, alias="status"),
):
    return service.list_enrollments(
        student_id=student_id,
        course_id=course_id,
        term_id=term_id,
        status=enrollment_status,
    )


@router.patch("/{enrollment_id}", response_model=EnrollmentRead)
def update_enrollment(
    enrollment_id: UUID, payload: EnrollmentUpdate, service: SchoolServiceDep
):
    return service.set_enrollment_status(enrollment_id, payload.status)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: UUID, service: SchoolServiceDep):
    service.delete_enrollment(enrollment_id)
