import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from scalar_fastapi import get_scalar_api_reference
from sqlmodel import Session

from app.core.config import notification_settings
from app.core.session import engine
from app.repositories.notification_repository import NotificationRepository
from app.routers.attendance import router as attendance_router
from app.routers.courses import router as courses_router
from app.routers.enrollments import router as enrollments_router
from app.routers.events import router as events_router
from app.routers.fees import router as fees_router
from app.routers.grades import router as grades_router
from app.routers.students import router as students_router
from app.routers.subscribers import router as subscribers_router
from app.routers.terms import router as terms_router
from app.routers.timetable import router as timetable_router
from app.routers.users import router as users_router
from app.services.channels.email import EmailNotificationChannel
from app.services.exceptions import ResourceConflictError, ResourceNotFoundError
from app.services.notification_service import NotificationOrchestratorService
from app.services.scheduler_service import SchedulerService
from app.services.template_renderer import TemplateRenderer

logger = logging.getLogger(__name__)


def build_notification_orchestrator() -> NotificationOrchestratorService:
    session = Session(engine)
    repository = NotificationRepository(session=session)
    renderer = TemplateRenderer(template_dir=notification_settings.TEMPLATE_DIR)
    email_channel = EmailNotificationChannel(settings=notification_settings)
    return NotificationOrchestratorService(
        repository=repository,
        renderer=renderer,
        email_channel=email_channel,
        settings=notification_settings,
    )


async def run_notification_cycle() -> None:
    orchestrator = build_notification_orchestrator()
    try:
        await orchestrator.process_due_notifications()
    finally:
        orchestrator.repository.session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = SchedulerService(
        notification_job=run_notification_cycle,
        settings=notification_settings,
    )
    scheduler.start()
    app.state.scheduler = scheduler
    logger.info("Application startup complete")
    yield
    scheduler.shutdown()
    logger.info("Application shutdown complete")


app = FastAPI(
    lifespan=lifespan,
    title="Academic Notification Service",
    docs_url=None,
    redoc_url=None,
)


@app.exception_handler(ResourceNotFoundError)
async def handle_resource_not_found(_request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
    )


@app.exception_handler(ResourceConflictError)
async def handle_resource_conflict(_request: Request, exc: ResourceConflictError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
    )


app.include_router(subscribers_router)
app.include_router(events_router)
app.include_router(users_router)
app.include_router(terms_router)
app.include_router(students_router)
app.include_router(courses_router)
app.include_router(enrollments_router)
app.include_router(timetable_router)
app.include_router(attendance_router)
app.include_router(grades_router)
app.include_router(fees_router)


@app.get("/docs", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url)


@app.post("/internal/notifications/run")
async def run_notifications_now():
    await run_notification_cycle()
    return {"status": "ok"}


app.frontend(path="/", directory="frontend/dist")
