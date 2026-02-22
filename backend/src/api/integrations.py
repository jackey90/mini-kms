import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db.models import Integration
from src.services.integration_service import (
    list_integrations, configure_telegram, configure_teams,
    test_telegram, test_teams,
)

router = APIRouter(prefix="/integrations", tags=["integrations"])


class IntegrationResponse(BaseModel):
    id: int
    name: str
    channel: str
    status: str
    token_last4: str | None
    last_active_at: datetime.datetime | None
    error_message: str | None

    model_config = {"from_attributes": True}


class TelegramConfig(BaseModel):
    bot_token: str


class TeamsConfig(BaseModel):
    app_id: str
    app_password: str


class TestResult(BaseModel):
    success: bool
    response_time_ms: int | None
    message: str


@router.get("")
def get_integrations(db: Session = Depends(get_db)) -> list[IntegrationResponse]:
    return list_integrations(db)


@router.put("/telegram")
def configure_telegram_integration(
    body: TelegramConfig, db: Session = Depends(get_db)
) -> dict:
    try:
        configure_telegram(body.bot_token, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"message": "Integration configured successfully", "status": "connected"}


@router.put("/teams")
def configure_teams_integration(
    body: TeamsConfig, db: Session = Depends(get_db)
) -> dict:
    configure_teams(body.app_id, body.app_password, db)
    return {"message": "Integration configured successfully", "status": "connected"}


@router.post("/telegram/test")
def test_telegram_integration(db: Session = Depends(get_db)) -> TestResult:
    result = test_telegram(db)
    return TestResult(**result)


@router.post("/teams/test")
def test_teams_integration(db: Session = Depends(get_db)) -> TestResult:
    result = test_teams(db)
    return TestResult(**result)


@router.post("/teams/messages")
async def teams_webhook(request: Request, db: Session = Depends(get_db)):
    """Teams Bot Framework webhook endpoint."""
    from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings
    from botbuilder.schema import Activity
    from src.config import settings
    from src.services.orchestrator import process_query
    import json

    adapter_settings = BotFrameworkAdapterSettings(
        app_id=settings.teams_app_id,
        app_password=settings.teams_app_password,
    )
    adapter = BotFrameworkAdapter(adapter_settings)

    body = await request.json()
    activity = Activity().deserialize(body)

    if activity.service_url and "://localhost" in activity.service_url:
        activity.service_url = activity.service_url.replace("://localhost", "://host.docker.internal")

    async def turn_handler(turn_context):
        query = turn_context.activity.text or ""
        if query.strip():
            result = process_query(query, "teams", str(turn_context.activity.from_property.id), db)
            await turn_context.send_activity(result.channel_formatted)

    auth_header = request.headers.get("Authorization", "")
    await adapter.process_activity(activity, auth_header, turn_handler)
    return {}
