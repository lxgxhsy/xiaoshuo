from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generation.chapter.chapter_one import build_chapter_one_draft
from generation.graph.sample_world import build_fog_clock_world
from validation.reports.render import render_validation_report
from validation.validators.chapter_validation import validate_chapter_draft


class ChapterOneTests(unittest.TestCase):
    def test_chapter_one_structured_events_pass_validation(self) -> None:
        graph = build_fog_clock_world()
        draft = build_chapter_one_draft()

        report = validate_chapter_draft(draft, graph)

        self.assertTrue(report.passed, render_validation_report(report))


if __name__ == "__main__":
    unittest.main()
