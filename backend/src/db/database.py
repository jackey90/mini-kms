import json
import os
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from src.db.models import Base, IntentSpace, Integration
from src.config import settings


engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

# Enable WAL mode for better concurrent reads
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, _connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    os.makedirs(settings.data_dir, exist_ok=True)
    os.makedirs(os.path.join(settings.data_dir, "faiss"), exist_ok=True)
    os.makedirs(os.path.join(settings.data_dir, "uploads"), exist_ok=True)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        _seed_intent_spaces(db)
        _seed_integrations(db)
        db.commit()
    finally:
        db.close()


def _seed_intent_spaces(db: Session) -> None:
    defaults = [
        {
            "name": "HR",
            "description": "Human resources policies, employee handbook, attendance, compensation, leave",
            "keywords": ["HR", "employee", "leave", "salary", "policy", "attendance", "handbook"],
            "is_default": True,
        },
        {
            "name": "Legal",
            "description": "Contract templates, legal terms, compliance policies, NDAs",
            "keywords": ["contract", "compliance", "legal", "NDA", "policy", "terms"],
            "is_default": True,
        },
        {
            "name": "Finance",
            "description": "Expense reimbursement, budget policy, financial reports, procurement",
            "keywords": ["budget", "expense", "reimbursement", "finance", "invoice", "procurement"],
            "is_default": True,
        },
    ]
    for d in defaults:
        existing = db.query(IntentSpace).filter_by(name=d["name"]).first()
        if not existing:
            db.add(IntentSpace(
                name=d["name"],
                description=d["description"],
                keywords=json.dumps(d["keywords"]),
                is_default=d["is_default"],
            ))


def _seed_integrations(db: Session) -> None:
    env_credentials = {
        "telegram": {
            "token": settings.telegram_bot_token,
            "last4": settings.telegram_bot_token[-4:] if settings.telegram_bot_token else None,
        },
        "teams": {
            "token": settings.teams_app_id,
            "last4": settings.teams_app_id[-4:] if settings.teams_app_id else None,
        },
    }
    for channel, name in [("telegram", "Telegram"), ("teams", "Microsoft Teams")]:
        existing = db.query(Integration).filter_by(channel=channel).first()
        creds = env_credentials[channel]
        if not existing:
            db.add(Integration(
                channel=channel,
                name=name,
                status="connected" if creds["token"] else "disconnected",
                token_last4=creds["last4"],
            ))
        elif existing.status == "disconnected" and creds["token"]:
            existing.status = "connected"
            existing.token_last4 = creds["last4"]
