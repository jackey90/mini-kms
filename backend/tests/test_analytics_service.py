"""Tests for analytics_service — DB operations with in-memory SQLite."""

import json
import pytest
from src.db.models import QueryLog, IntentSpace
from src.services.analytics_service import (
    get_query_logs, get_kb_stats, reclassify_query, export_csv,
)


def _add_query_log(db, intent="HR", confidence=0.85, channel="api", ms=1200):
    log = QueryLog(
        user_query="What is the leave policy?",
        detected_intent=intent,
        confidence_score=confidence,
        source_documents=json.dumps(["handbook.pdf"]),
        response_status="success",
        channel=channel,
        response_time_ms=ms,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


class TestGetQueryLogs:
    def test_returns_empty_when_no_logs(self, db_session):
        total, items = get_query_logs(db_session)
        assert total == 0
        assert items == []

    def test_returns_logs_and_total(self, db_session):
        _add_query_log(db_session)
        _add_query_log(db_session, intent="Legal")
        total, items = get_query_logs(db_session, limit=10)
        assert total == 2
        assert len(items) == 2

    def test_filter_by_intent(self, db_session):
        _add_query_log(db_session, intent="HR")
        _add_query_log(db_session, intent="Legal")
        total, items = get_query_logs(db_session, intent="HR")
        assert total == 1
        assert items[0].detected_intent == "HR"

    def test_filter_by_channel(self, db_session):
        _add_query_log(db_session, channel="telegram")
        _add_query_log(db_session, channel="teams")
        total, items = get_query_logs(db_session, channel="telegram")
        assert total == 1


class TestGetKbStats:
    def test_stats_with_no_data(self, db_session):
        stats = get_kb_stats(db_session)
        assert stats["total_documents"] == 0
        assert stats["total_queries"] == 0
        assert stats["avg_latency_ms"] == 0

    def test_avg_latency_calculated(self, db_session):
        _add_query_log(db_session, ms=1000)
        _add_query_log(db_session, ms=2000)
        stats = get_kb_stats(db_session)
        assert stats["avg_latency_ms"] == 1500


class TestReclassifyQuery:
    def test_reclassify_updates_intent(self, db_session):
        log = _add_query_log(db_session, intent="HR")
        reclassify_query(log.id, "Legal", db_session)
        db_session.refresh(log)
        assert log.detected_intent == "Legal"
        assert log.response_status == "reclassified"

    def test_reclassify_nonexistent_query_raises(self, db_session):
        with pytest.raises(ValueError, match="not found"):
            reclassify_query(9999, "HR", db_session)

    def test_reclassify_to_nonexistent_intent_raises(self, db_session):
        log = _add_query_log(db_session)
        with pytest.raises(ValueError, match="not found"):
            reclassify_query(log.id, "NonExistent", db_session)


class TestExportCsv:
    def test_export_csv_header(self, db_session):
        csv_content = export_csv(db_session)
        assert "id,timestamp,user_query" in csv_content

    def test_export_csv_includes_data(self, db_session):
        _add_query_log(db_session)
        csv_content = export_csv(db_session)
        assert "leave policy" in csv_content
