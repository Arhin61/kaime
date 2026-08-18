from fastapi import APIRouter, status

from app.dependencies import GradingServiceDep, SchoolServiceDep
from app.schemas import (
    CourseCreate,
    CourseRead,
    CourseResultRead,
    CourseUpdate,
    EnrollmentRead,
)

router = APIRouter(prefix="/dashboard/courses", tags=["Courses"])


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, service: SchoolServiceDep):
    return service.create_course(payload)


@router.get("", response_model=list[CourseRead])
def list_courses(
    service: SchoolServiceDep,
    department: str | None = None,
    level: int | None = None,
    is_active: bool | None = None,
):
    return service.list_courses(
        department=department, level=level, is_active=is_active
    )


@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, service: SchoolServiceDep):
    return service.get_course(course_id)


@router.patch("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, payload: CourseUpdate, service: SchoolServiceDep):
    return service.update_course(course_id, payload)


@router.patch("/{course_id}/activate", response_model=CourseRead)
def activate_course(course_id: int, service: SchoolServiceDep):
    return service.set_course_active(course_id, True)


@router.patch("/{course_id}/deactivate", response_model=CourseRead)
def deactivate_course(course_id: int, service: SchoolServiceDep):
    return service.set_course_active(course_id, False)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, service: SchoolServiceDep):
    service.delete_course(course_id)


@router.get("/{course_id}/roster", response_model=list[EnrollmentRead])
def get_course_roster(
    course_id: int,
    service: SchoolServiceDep,
    term_id: int | None = None,
):
    return service.list_enrollments(course_id=course_id, term_id=term_id)


@router.get("/{course_id}/results", response_model=list[CourseResultRead])
def get_course_results(course_id: int, term_id: int, service: GradingServiceDep):
    return service.course_results(course_id, term_id)
