from fastapi import APIRouter, status

from app.dependencies import GradingServiceDep
from app.schemas import (
    AssessmentCreate,
    AssessmentRead,
    AssessmentUpdate,
    ScoreRead,
    ScoreRecord,
)

router = APIRouter(prefix="/dashboard/grades", tags=["Grades"])


@router.post(
    "/assessments", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED
)
def create_assessment(payload: AssessmentCreate, service: GradingServiceDep):
    return service.create_assessment(payload)


@router.get("/assessments", response_model=list[AssessmentRead])
def list_assessments(
    service: GradingServiceDep,
    course_id: int | None = None,
    term_id: int | None = None,
):
    return service.list_assessments(course_id=course_id, term_id=term_id)


@router.patch("/assessments/{assessment_id}", response_model=AssessmentRead)
def update_assessment(
    assessment_id: int, payload: AssessmentUpdate, service: GradingServiceDep
):
    return service.update_assessment(assessment_id, payload)


@router.delete("/assessments/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assessment(assessment_id: int, service: GradingServiceDep):
    service.delete_assessment(assessment_id)


@router.post("/scores", response_model=list[ScoreRead])
def record_scores(payload: ScoreRecord, service: GradingServiceDep):
    return service.record_scores(payload)


@router.get("/assessments/{assessment_id}/scores", response_model=list[ScoreRead])
def list_scores(assessment_id: int, service: GradingServiceDep):
    return service.list_scores(assessment_id)
