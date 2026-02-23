"""Tests for intent_service — CRUD operations."""

import json
import pytest
from src.db.models import IntentSpace, Document
from src.services.intent_service import (
    list_intent_spaces, create_intent_space, update_intent_space,
    delete_intent_space, get_document_count,
)


class TestListIntentSpaces:
    def test_returns_seeded_defaults(self, db_session):
        spaces = list_intent_spaces(db_session)
        names = {s.name for s in spaces}
        assert names == {"HR", "Legal", "Finance"}


class TestCreateIntentSpace:
    def test_create_new_space(self, db_session):
        space = create_intent_space("Operations", "Ops stuff", ["SOP"], db_session)
        assert space.name == "Operations"
        assert not space.is_default

    def test_duplicate_name_raises(self, db_session):
        with pytest.raises(ValueError, match="already exists"):
            create_intent_space("HR", "duplicate", [], db_session)


class TestUpdateIntentSpace:
    def test_update_description(self, db_session):
        space = list_intent_spaces(db_session)[0]
        updated = update_intent_space(space.id, None, "Updated desc", None, db_session)
        assert updated.description == "Updated desc"

    def test_update_keywords(self, db_session):
        space = list_intent_spaces(db_session)[0]
        updated = update_intent_space(space.id, None, None, ["new", "keywords"], db_session)
        assert json.loads(updated.keywords) == ["new", "keywords"]

    def test_rename_to_existing_raises(self, db_session):
        space = list_intent_spaces(db_session)[0]
        with pytest.raises(ValueError, match="already exists"):
            update_intent_space(space.id, "Legal", None, None, db_session)


class TestDeleteIntentSpace:
    def test_cannot_delete_default(self, db_session):
        space = list_intent_spaces(db_session)[0]
        with pytest.raises(ValueError, match="Cannot delete default"):
            delete_intent_space(space.id, db_session)

    def test_delete_custom_space(self, db_session):
        space = create_intent_space("Custom", "", [], db_session)
        delete_intent_space(space.id, db_session)
        assert db_session.query(IntentSpace).filter_by(id=space.id).first() is None

    def test_cannot_delete_with_documents(self, db_session):
        space = create_intent_space("WithDocs", "", [], db_session)
        db_session.add(Document(
            filename="test.pdf", format="pdf", size_bytes=100,
            file_path="/tmp/test.pdf", intent_space_id=space.id,
        ))
        db_session.commit()
        with pytest.raises(ValueError, match="document"):
            delete_intent_space(space.id, db_session)


class TestGetDocumentCount:
    def test_zero_when_no_docs(self, db_session):
        space = list_intent_spaces(db_session)[0]
        assert get_document_count(space.id, db_session) == 0
