"""Tests for document_parser — file validation and text chunking."""

import pytest
from src.ml.document_parser import parse_document


class TestParseDocument:
    def test_unsupported_format_raises(self):
        with pytest.raises(ValueError, match="Unsupported file format"):
            parse_document(b"dummy", "file.txt")

    def test_unsupported_xlsx_raises(self):
        with pytest.raises(ValueError, match="Unsupported file format"):
            parse_document(b"dummy", "data.xlsx")

    def test_empty_pdf_raises(self):
        # An empty byte string isn't a valid PDF
        with pytest.raises(Exception):
            parse_document(b"", "empty.pdf")

    def test_empty_docx_raises(self):
        with pytest.raises(Exception):
            parse_document(b"", "empty.docx")
