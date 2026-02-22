import datetime
import httpx
from sqlalchemy.orm import Session
from src.db.models import Integration
from src.config import settings


def list_integrations(db: Session) -> list[Integration]:
    return db.query(Integration).all()


def configure_telegram(bot_token: str, db: Session) -> Integration:
    # Verify token with Telegram API
    try:
        resp = httpx.get(
            f"https://api.telegram.org/bot{bot_token}/getMe",
            timeout=10,
        )
        resp.raise_for_status()
    except Exception as exc:
        raise ValueError(f"Invalid Telegram token: {exc}")

    # Persist token to environment (in-memory for current process)
    settings.telegram_bot_token = bot_token

    integration = db.query(Integration).filter_by(channel="telegram").first()
    integration.token_last4 = bot_token[-4:]
    integration.status = "connected"
    integration.updated_at = datetime.datetime.utcnow()
    integration.error_message = None
    db.commit()
    db.refresh(integration)
    return integration


def configure_teams(app_id: str, app_password: str, db: Session) -> Integration:
    settings.teams_app_id = app_id
    settings.teams_app_password = app_password

    integration = db.query(Integration).filter_by(channel="teams").first()
    integration.token_last4 = app_id[-4:] if len(app_id) >= 4 else app_id
    integration.status = "connected"
    integration.updated_at = datetime.datetime.utcnow()
    integration.error_message = None
    db.commit()
    db.refresh(integration)
    return integration


def test_telegram(db: Session) -> dict:
    import time
    token = settings.telegram_bot_token
    if not token:
        return {"success": False, "response_time_ms": None, "message": "Telegram not configured"}

    start = time.time()
    try:
        resp = httpx.get(
            f"https://api.telegram.org/bot{token}/getMe",
            timeout=5,
        )
        resp.raise_for_status()
        elapsed = int((time.time() - start) * 1000)

        integration = db.query(Integration).filter_by(channel="telegram").first()
        if integration:
            integration.last_active_at = datetime.datetime.utcnow()
            db.commit()

        return {"success": True, "response_time_ms": elapsed, "message": "Connection verified successfully"}
    except Exception as exc:
        return {"success": False, "response_time_ms": None, "message": str(exc)}


def test_teams(db: Session) -> dict:
    if not settings.teams_app_id:
        return {"success": False, "response_time_ms": None, "message": "Teams not configured"}
    # For local demo, just verify credentials exist
    return {"success": True, "response_time_ms": 0,
            "message": "Teams configuration present. Use Bot Framework Emulator to test locally."}
