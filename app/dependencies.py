from collections.abc import Generator
from typing import Annotated
from uuid import UUID

from fastapi import BackgroundTasks, Depends, HTTPException, status
from sqlmodel import Session

from app.core.config import NotificationSettings, notification_settings
from app.core.security import decode_access_token
from app.core.session import get_session
from app.models import User
from app.repositories.academic_repository import AcademicRepository
from app.repositories.notification_repository import NotificationRepository
from app.repositories.school_repository import SchoolRepository
from app.services.academic_service import AcademicService
from app.services.attendance_service import AttendanceService
from app.services.channels.email import EmailNotificationChannel
from app.services.finance_service import FinanceService
from app.services.grading_service import GradingService
from app.services.notification_service import NotificationOrchestratorService
from app.services.school_service import SchoolService
from app.services.template_renderer import TemplateRenderer
from app.services.user_service import UserService

SessionDep = Annotated[Session, Depends(get_session)]


def get_user_service(session: SessionDep, tasks: BackgroundTasks) -> UserService:
    return UserService(session=session, tasks=tasks)


def get_current_user(token: str, session: SessionDep) -> User:
    payload = decode_access_token(token)

    user = session.get(User, UUID(payload.get("sub")))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_notification_settings() -> NotificationSettings:
    return notification_settings


def get_template_renderer(
    settings: NotificationSettings = Depends(get_notification_settings),
) -> TemplateRenderer:
    return TemplateRenderer(template_dir=settings.TEMPLATE_DIR)


def get_email_channel(
    settings: NotificationSettings = Depends(get_notification_settings),
) -> EmailNotificationChannel:
    return EmailNotificationChannel(settings=settings)


def get_notification_repository(
    session: Session = Depends(get_session),
) -> NotificationRepository:
    return NotificationRepository(session=session)


def get_notification_service(
    repository: NotificationRepository = Depends(get_notification_repository),
    renderer: TemplateRenderer = Depends(get_template_renderer),
    email_channel: EmailNotificationChannel = Depends(get_email_channel),
    settings: NotificationSettings = Depends(get_notification_settings),
) -> NotificationOrchestratorService:
    return NotificationOrchestratorService(
        repository=repository,
        renderer=renderer,
        email_channel=email_channel,
        settings=settings,
    )


def get_academic_repository(
    session: Session = Depends(get_session),
) -> AcademicRepository:
    return AcademicRepository(session=session)


def get_academic_service(
    repository: AcademicRepository = Depends(get_academic_repository),
) -> AcademicService:
    return AcademicService(repository=repository)


def get_school_repository(
    session: Session = Depends(get_session),
) -> SchoolRepository:
    return SchoolRepository(session=session)


def get_school_service(
    repository: SchoolRepository = Depends(get_school_repository),
) -> SchoolService:
    return SchoolService(repository=repository)


def get_attendance_service(
    repository: SchoolRepository = Depends(get_school_repository),
) -> AttendanceService:
    return AttendanceService(repository=repository)


def get_grading_service(
    repository: SchoolRepository = Depends(get_school_repository),
) -> GradingService:
    return GradingService(repository=repository)


def get_finance_service(
    repository: SchoolRepository = Depends(get_school_repository),
) -> FinanceService:
    return FinanceService(repository=repository)


SchoolServiceDep = Annotated[SchoolService, Depends(get_school_service)]
AttendanceServiceDep = Annotated[AttendanceService, Depends(get_attendance_service)]
GradingServiceDep = Annotated[GradingService, Depends(get_grading_service)]
FinanceServiceDep = Annotated[FinanceService, Depends(get_finance_service)]


def get_db_session() -> Generator[Session, None, None]:
    yield from get_session()
