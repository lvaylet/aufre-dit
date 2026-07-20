import os
import unittest
from unittest.mock import MagicMock, patch

# Configure environment variables and mock external services before importing app.py
os.environ.setdefault("GEMINI_API_KEY", "dummy_api_key")
os.environ.setdefault("FAQ_DOC_URL", "https://docs.google.com/document/d/dummy_doc_id")

mock_response = MagicMock()
mock_response.text = "Contenu FAQ de test"
mock_response.status_code = 200

with patch("requests.get", return_value=mock_response), patch("google.genai.Client"):
    from app import format_export_url


class TestFormatExportUrl(unittest.TestCase):
    """Tests unitaires pour la fonction format_export_url basés sur les exemples du README.md."""

    DOC_ID = "1PtDzEbEDFFKPgl_T8rz3PCiLrU8X2Fh2qqsZQqEOgt0"
    EXPECTED_URL = f"https://docs.google.com/document/d/{DOC_ID}/export?format=txt"

    def test_readme_example_1_standard_url(self):
        """Forme 1 dans README: https://docs.google.com/document/d/<ID>"""
        raw_url = f"https://docs.google.com/document/d/{self.DOC_ID}"
        self.assertEqual(format_export_url(raw_url), self.EXPECTED_URL)

    def test_readme_example_2_trailing_slash(self):
        """Forme 2 dans README: https://docs.google.com/document/d/<ID>/"""
        raw_url = f"https://docs.google.com/document/d/{self.DOC_ID}/"
        self.assertEqual(format_export_url(raw_url), self.EXPECTED_URL)

    def test_readme_example_3_edit_url(self):
        """Forme 3 dans README: https://docs.google.com/document/d/<ID>/edit"""
        raw_url = f"https://docs.google.com/document/d/{self.DOC_ID}/edit"
        self.assertEqual(format_export_url(raw_url), self.EXPECTED_URL)

    def test_readme_example_4_already_formatted_export_url(self):
        """Forme 4 dans README: https://docs.google.com/document/d/<ID>/export?format=txt"""
        raw_url = f"https://docs.google.com/document/d/{self.DOC_ID}/export?format=txt"
        self.assertEqual(format_export_url(raw_url), self.EXPECTED_URL)

    def test_export_without_format_txt(self):
        """Cas limite: URL /export sans format=txt"""
        raw_url = f"https://docs.google.com/document/d/{self.DOC_ID}/export"
        self.assertEqual(format_export_url(raw_url), self.EXPECTED_URL)

    def test_whitespace_trimming(self):
        """Cas limite: URL contenant des espaces au début et à la fin"""
        raw_url = f"   https://docs.google.com/document/d/{self.DOC_ID}/edit   "
        self.assertEqual(format_export_url(raw_url), self.EXPECTED_URL)


if __name__ == "__main__":
    unittest.main()
