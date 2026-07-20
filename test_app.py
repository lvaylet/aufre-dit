import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Configure environment variables and mock external services before importing app.py
os.environ.setdefault("GEMINI_API_KEY", "dummy_api_key")
os.environ.setdefault("FAQ_DOC_URL", "https://docs.google.com/document/d/dummy_doc_id")

mock_response = MagicMock()
mock_response.text = "Contenu FAQ de test"
mock_response.status_code = 200

with patch("requests.get", return_value=mock_response), patch("google.genai.Client"):
    from app import format_export_url, load_static_documents

DOC_ID = "1PtDzEbEDFFKPgl_T8rz3PCiLrU8X2Fh2qqsZQqEOgt0"
EXPECTED_URL = f"https://docs.google.com/document/d/{DOC_ID}/export?format=txt"


@pytest.mark.parametrize(
    ("raw_url", "expected_url"),
    [
        (f"https://docs.google.com/document/d/{DOC_ID}", EXPECTED_URL),
        (f"https://docs.google.com/document/d/{DOC_ID}/", EXPECTED_URL),
        (f"https://docs.google.com/document/d/{DOC_ID}/edit", EXPECTED_URL),
        (
            f"https://docs.google.com/document/d/{DOC_ID}/export?format=txt",
            EXPECTED_URL,
        ),
        (f"https://docs.google.com/document/d/{DOC_ID}/export", EXPECTED_URL),
        (f"   https://docs.google.com/document/d/{DOC_ID}/edit   ", EXPECTED_URL),
    ],
    ids=[
        "readme_example_1_standard_url",
        "readme_example_2_trailing_slash",
        "readme_example_3_edit_url",
        "readme_example_4_already_formatted_export_url",
        "export_without_format_txt",
        "whitespace_trimming",
    ],
)
def test_format_export_url(raw_url: str, expected_url: str) -> None:
    """Tests unitaires pour la fonction format_export_url basés sur les exemples du README.md."""
    assert format_export_url(raw_url) == expected_url


def test_load_static_documents(tmp_path: Path) -> None:
    """Test le chargement des fichiers .txt du dossier static."""
    doc1 = tmp_path / "guide.txt"
    doc1.write_text("Contenu du guide", encoding="utf-8")
    non_txt = tmp_path / "file.pdf"
    non_txt.write_text("fake pdf", encoding="utf-8")

    result = load_static_documents(str(tmp_path))
    assert "=== DOCUMENT : guide.txt ===" in result
    assert "Contenu du guide" in result
    assert "fake pdf" not in result
