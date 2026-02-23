"""Tests for channel-specific formatting in rag_engine.

These tests target the pure-logic formatting functions which don't
need OpenAI or any external config to run.
"""

import sys
from unittest.mock import MagicMock

# Stub out pydantic_settings before importing the module under test,
# so we don't depend on a specific pydantic version in CI.
if "pydantic_settings" not in sys.modules:
    _stub = MagicMock()
    _stub.BaseSettings = type("BaseSettings", (), {"model_config": {}})
    sys.modules["pydantic_settings"] = _stub

from src.ml.rag_engine import _format_for_channel, _enforce_telegram_limit


class TestFormatForChannel:
    def test_telegram_adds_emoji_source(self):
        result = _format_for_channel("Hello world", ["doc.pdf"], "telegram", fallback=False)
        assert "📄 Sources:" in result
        assert "doc.pdf" in result

    def test_teams_adds_bold_sources(self):
        result = _format_for_channel("Hello world", ["doc.pdf"], "teams", fallback=False)
        assert "**Sources:**" in result
        assert "---" in result

    def test_api_plain_sources(self):
        result = _format_for_channel("Answer here", ["a.pdf", "b.docx"], "api", fallback=False)
        assert "Sources:" in result
        assert "a.pdf" in result and "b.docx" in result

    def test_fallback_returns_answer_directly(self):
        result = _format_for_channel("No info found.", [], "teams", fallback=True)
        assert result == "No info found."

    def test_telegram_fallback_still_enforces_limit(self):
        long_text = "A" * 5000
        result = _format_for_channel(long_text, [], "telegram", fallback=True)
        assert len(result) <= 4096


class TestEnforceTelegramLimit:
    def test_short_text_unchanged(self):
        text = "Short text"
        assert _enforce_telegram_limit(text) == text

    def test_long_text_truncated(self):
        text = "A" * 5000
        result = _enforce_telegram_limit(text)
        assert len(result) <= 4096
        assert "truncated" in result.lower()

    def test_truncation_at_sentence_boundary(self):
        text = "First sentence. " * 300
        result = _enforce_telegram_limit(text)
        assert len(result) <= 4096
        assert result.rstrip().endswith("truncated due to length.")

    def test_exact_limit_not_truncated(self):
        text = "A" * 4096
        assert _enforce_telegram_limit(text) == text
