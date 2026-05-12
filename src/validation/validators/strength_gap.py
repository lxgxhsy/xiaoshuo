from __future__ import annotations

from domain.chapter.models import ChapterDraft
from domain.graph.models import WorldGraph
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_strength_gap(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="B.1")
    for event in draft.events:
        if event.event_type != "direct_conflict" or event.outcome != "protagonist_victory":
            continue
        if event.protagonist_power_level is None or event.opponent_power_level is None:
            result.failures.append(
                ValidationFailure(
                    "B.1",
                    event.id,
                    "Direct victory is missing power-level evidence.",
                    "Record protagonist_power_level and opponent_power_level.",
                )
            )
            continue
        if event.opponent_power_level <= event.protagonist_power_level + 1:
            result.evidence.append(
                Evidence("B.1", event.id, "No overwhelming strength gap.")
            )
            continue
        has_causal_evidence = all(step.evidence for step in event.causal_chain) and event.causal_chain
        has_non_replicable_factor = any(step.is_non_replicable for step in event.causal_chain)
        has_cost = bool(event.irreversible_costs)
        if not has_causal_evidence or not (has_non_replicable_factor or has_cost):
            result.failures.append(
                ValidationFailure(
                    "B.1",
                    event.id,
                    "Protagonist defeated a higher-level opponent without sufficient causal-chain evidence.",
                    "Add evidence, a non-replicable factor, or an irreversible cost.",
                )
            )
        else:
            result.evidence.append(
                Evidence("B.1", event.id, "Victory has causal chain and limiting factor.")
            )
    return result
