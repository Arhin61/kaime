from fastapi import APIRouter, status

from app.dependencies import SchoolServiceDep
from app.schemas import ClassSessionCreate, ClassSessionRead, ClassSessionUpdate

router = APIRouter(prefix="/dashboard/timetable", tags=["Timetable"])


@router.post("", response_model=ClassSessionRead, status_code=status.HTTP_201_CREATED)
def create_class_session(payload: ClassSessionCreate, service: SchoolServiceDep):
    return service.create_class_session(payload)


@router.get("", response_model=list[ClassSessionRead])
def list_class_sessions(
    service: SchoolServiceDep,
    term_id: int | None = None,
    course_id: int | None = None,
):
    return service.list_class_sessions(term_id=term_id, course_id=course_id)


@router.patch("/{session_id}", response_model=ClassSessionRead)
def update_class_session(
    session_id: int, payload: ClassSessionUpdate, service: SchoolServiceDep
):
    return service.update_class_session(session_id, payload)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_session(session_id: int, service: SchoolServiceDep):
    service.delete_class_session(session_id)
