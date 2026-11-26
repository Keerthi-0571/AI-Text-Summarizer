"""Web API tests (model call mocked, so nothing is downloaded)."""
import unittest
from unittest import mock

try:
    import web
except ImportError:          # Flask not installed
    web = None


@unittest.skipIf(web is None, "Flask not installed")
class WebTests(unittest.TestCase):
    def setUp(self):
        self.client = web.app.test_client()

    def test_index_loads(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"AI Text Summarizer", r.data)

    def test_examples_endpoint(self):
        r = self.client.get("/api/examples")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.get_json()), 5)

    def test_empty_text_is_400(self):
        r = self.client.post("/api/summarize", json={"text": "  ", "length": "short"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("empty", r.get_json()["error"].lower())

    def test_bad_custom_length_is_400(self):
        r = self.client.post("/api/summarize", json={"text": "word " * 100, "length": 5})
        self.assertEqual(r.status_code, 400)

    def test_success(self):
        with mock.patch.object(web, "summarize", return_value="A short summary."):
            r = self.client.post("/api/summarize", json={"text": "word " * 100, "length": "short"})
        body = r.get_json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(body["summary"], "A short summary.")
        self.assertEqual(body["input_words"], 100)

    def test_model_failure_is_500(self):
        with mock.patch.object(web, "summarize", side_effect=RuntimeError("boom")):
            r = self.client.post("/api/summarize", json={"text": "word " * 100})
        self.assertEqual(r.status_code, 500)


if __name__ == "__main__":
    unittest.main()
