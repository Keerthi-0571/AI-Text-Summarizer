"""Tests that run without downloading the model (model calls are mocked)."""
import unittest
from unittest import mock

from summarizer import core
from summarizer import summarize, auto_check


class FakeTokenizer:
    def encode(self, text, add_special_tokens=False):
        return text.split()


class ValidationTests(unittest.TestCase):
    def test_empty_rejected(self):
        for bad in ["", "   \n ", None]:
            with self.assertRaises(ValueError):
                summarize(bad)

    def test_too_long_rejected(self):
        with self.assertRaises(ValueError):
            summarize("word " * (core.MAX_INPUT_WORDS + 5))

    def test_bad_length_rejected(self):
        with self.assertRaises(ValueError):
            summarize("This is some text. " * 20, length="huge")

    def test_short_input_returned_unchanged(self):
        self.assertEqual(summarize("The meeting is at 3 PM tomorrow."),
                         "The meeting is at 3 PM tomorrow.")


class LengthTests(unittest.TestCase):
    def test_presets_and_int(self):
        self.assertEqual(core.resolve_length("short"), 30)
        self.assertEqual(core.resolve_length("long"), 100)
        self.assertEqual(core.resolve_length(45), 45)
        self.assertEqual(core.resolve_length(3), 15)   # floor


class ChunkingTests(unittest.TestCase):
    def setUp(self):
        p = mock.patch.object(core, "_get_tokenizer", return_value=FakeTokenizer())
        p.start()
        self.addCleanup(p.stop)

    def test_chunks_respect_limit(self):
        text = " ".join(f"Sentence number {i} has seven words here." for i in range(200))
        chunks = core.split_chunks(text, max_tokens=100)
        self.assertGreater(len(chunks), 1)
        for c in chunks:
            self.assertLessEqual(len(c.split()), 100)

    def test_long_input_uses_map_reduce(self):
        text = " ".join(f"Sentence number {i} has seven words here." for i in range(400))
        with mock.patch.object(core, "_run_model", return_value="partial summary") as run:
            out = summarize(text, "short")
        self.assertEqual(out, "partial summary")
        self.assertGreater(run.call_count, 2)   # several chunks + one final pass


class CleanSummaryTests(unittest.TestCase):
    def test_spacing_fixed(self):
        self.assertEqual(core.clean_summary("Sales rose in 2016 ."), "Sales rose in 2016.")

    def test_trailing_fragment_removed(self):
        self.assertEqual(core.clean_summary("First done. Second is cut off and"), "First done.")

    def test_single_fragment_kept(self):
        self.assertEqual(core.clean_summary("Only one fragment"), "Only one fragment")

    def test_decimal_not_a_sentence_end(self):
        self.assertEqual(core.clean_summary("Growth was 3.5 percent and"), "Growth was 3.5 percent and")


class AutoCheckTests(unittest.TestCase):
    def test_supported_summary_ok(self):
        src = "Dr. Rao surveyed 40 sites in Indonesia in March."
        self.assertEqual(auto_check(src, "Rao surveyed 40 sites in Indonesia."), [])

    def test_invented_number_flagged(self):
        src = "The company will close 25 stores."
        self.assertIn("30", auto_check(src, "The company will close 30 stores."))


if __name__ == "__main__":
    unittest.main()
