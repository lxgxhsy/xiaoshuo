from __future__ import annotations

from collections import defaultdict

from domain.chapter.models import PerspectiveEventVersion
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_multiperspective_difference(
    versions: list[PerspectiveEventVersion],
    min_difference: int = 2,
) -> ValidationResult:
    result = ValidationResult(scenario_id="C.2")
    grouped: dict[str, list[PerspectiveEventVersion]] = defaultdict(list)
    for version in versions:
        grouped[version.event_id].append(version)

    for event_id, event_versions in grouped.items():
        if len(event_versions) < 2:
            result.failures.append(
                ValidationFailure(
                    "C.2",
                    event_id,
                    "Multi-perspective validation needs at least two versions of the same event.",
                    "Add another viewpoint version.",
                )
            )
            continue

        has_explained_difference = False
        for index, left in enumerate(event_versions):
            for right in event_versions[index + 1 :]:
                fact_delta = left.claimed_facts ^ right.claimed_facts
                omission_delta = left.omitted_facts ^ right.omitted_facts
                frame_delta = 1 if left.emotional_frame != right.emotional_frame else 0
                difference_score = len(fact_delta) + len(omission_delta) + frame_delta
                has_internal_reason = bool(left.distortion_sources and right.distortion_sources)
                if difference_score >= min_difference and has_internal_reason:
                    has_explained_difference = True
                    result.evidence.append(
                        Evidence(
                            "C.2",
                            event_id,
                            f"{left.character_id} and {right.character_id} differ for role-based reasons.",
                        )
                    )

        if not has_explained_difference:
            result.failures.append(
                ValidationFailure(
                    "C.2",
                    event_id,
                    "Versions are too similar or lack internal reasons for contradiction.",
                    "Add fact/omission/frame differences grounded in character perspective.",
                )
            )
    return result
