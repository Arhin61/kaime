from fastapi import APIRouter, status

from app.dependencies import SchoolServiceDep
from app.schemas import TermCreate, TermRead, TermUpdate

router = APIRouter(prefix="/dashboard/terms", tags=["Academic Terms"])


@router.post("", response_model=TermRead, status_code=status.HTTP_201_CREATED)
def create_term(payload: TermCreate, service: SchoolServiceDep):
    return service.create_term(payload)


@router.get("", response_model=list[TermRead])
def list_terms(service: SchoolServiceDep):
    return service.list_terms()


@router.get("/current", response_model=TermRead)
def get_current_term(service: SchoolServiceDep):
    return service.get_current_term()


@router.get("/{term_id}", response_model=TermRead)
def get_term(term_id: int, service: SchoolServiceDep):
    return service.get_term(term_id)


@router.patch("/{term_id}", response_model=TermRead)
def update_term(term_id: int, payload: TermUpdate, service: SchoolServiceDep):
    return service.update_term(term_id, payload)


@router.delete("/{term_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_term(term_id: int, service: SchoolServiceDep):
    service.delete_term(term_id)
