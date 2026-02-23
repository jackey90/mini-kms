"""Shared fixtures for all backend tests."""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("DATA_DIR", "/tmp/intelliknow_test")
os.environ.setdefault("OPENAI_API_KEY", "test-key")

from src.db.models import Base, IntentSpace
import json


@pytest.fixture()
def db_session():
    """Create a fresh in-memory SQLite database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed default intent spaces
    for name, desc, kw in [
        ("HR", "Human resources", ["HR", "employee", "leave", "salary"]),
        ("Legal", "Legal and compliance", ["contract", "compliance", "legal"]),
        ("Finance", "Financial operations", ["budget", "expense", "finance"]),
    ]:
        session.add(IntentSpace(
            name=name, description=desc,
            keywords=json.dumps(kw), is_default=True,
        ))
    session.commit()

    yield session

    session.close()
    engine.dispose()
