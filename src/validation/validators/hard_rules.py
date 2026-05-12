from __future__ import annotations

from domain.chapter.models import ChapterDraft
from domain.graph.models import WorldGraph
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_hard_rules(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="E.1")
    for event in draft.events:
        for rule_id in event.triggered_hard_rule_ids:
            rule = graph.hard_rule(rule_id)
            if not rule.is_hard:
                continue
            if rule_id not in event.hard_rule_effects_applied:
                result.failures.append(
                    ValidationFailure(
                        "E.1",
                        event.id,
                        f"Hard rule {rule_id} was triggered but its effect was not applied.",
                        f"Apply effect: {rule.effect}",
                    )
                )
            else:
                result.evidence.append(
                    Evidence("E.1", event.id, f"Hard rule {rule_id} effect applied.")
                )
    return result
