import logging
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.database import init_db
from src.api import documents, intents, query, integrations, analytics, health

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    init_db()

    # Start Telegram polling in a background thread
    from src.integrations.telegram_bot import run_polling
    tg_thread = threading.Thread(target=run_polling, daemon=True, name="telegram-polling")
    tg_thread.start()

    logger.info("IntelliKnow KMS backend started")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="IntelliKnow KMS API",
    version="1.0.0",
    description="Gen AI-powered Knowledge Management System",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://frontend:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers under /api prefix
for router_module in [documents, intents, query, integrations, analytics, health]:
    app.include_router(router_module.router, prefix="/api")
