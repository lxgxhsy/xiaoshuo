from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from generation.chapter.chapter_one import build_chapter_one_draft
from generation.chapter.chapter_three import build_chapter_three_draft
from generation.chapter.chapter_two import build_chapter_two_draft
from generation.graph.sample_world import build_fog_clock_world
from validation.reports.models import ValidationReport
from validation.reports.render import render_validation_report
from validation.validators.chapter_validation import validate_chapter_draft
from validation.validators.unknowable_layer import validate_unknowable_layer


def main() -> int:
    graph = build_fog_clock_world()
    chapter_report = validate_chapter_draft(build_chapter_one_draft(), graph)
    chapter_two_report = validate_chapter_draft(build_chapter_two_draft(), graph)
    chapter_three_report = validate_chapter_draft(build_chapter_three_draft(), graph)
    world_report = ValidationReport(
        [
            validate_unknowable_layer(
                graph,
                ["xu_guanchao", "xia_kui", "liang_zhu", "pei_mu"],
            )
        ]
    )

    print("## Chapter 001")
    print(render_validation_report(chapter_report))
    print("## Chapter 002")
    print(render_validation_report(chapter_two_report))
    print("## Chapter 003")
    print(render_validation_report(chapter_three_report))
    print("## World Graph")
    print(render_validation_report(world_report))
    return (
        0
        if chapter_report.passed
        and chapter_two_report.passed
        and chapter_three_report.passed
        and world_report.passed
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
