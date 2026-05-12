from __future__ import annotations

from domain.graph.models import WorldGraph
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_unknowable_layer(graph: WorldGraph, viewpoint_character_ids: list[str]) -> ValidationResult:
    result = ValidationResult(scenario_id="F.4")
    if not viewpoint_character_ids:
        result.failures.append(
            ValidationFailure(
                "F.4",
                "world_graph",
                "No viewpoint characters were supplied.",
                "Provide at least one viewpoint character for full-novel validation.",
            )
        )
        return result

    max_view_layer = max(graph.character(character_id).cognitive_layer for character_id in viewpoint_character_ids)
    viewpoint_set = set(viewpoint_character_ids)
    candidates = [
        node
        for node in graph.knowledge.values()
        if node.cognitive_layer > max_view_layer
        and not (node.known_by & viewpoint_set)
        and node.foreshadowing_evidence
    ]
    if not candidates:
        result.failures.append(
            ValidationFailure(
                "F.4",
                "world_graph",
                "No unknowable knowledge node exists above every viewpoint character with foreshadowing evidence.",
                "Add a higher-layer KnowledgeNode that no viewpoint character KNOWS, plus reader-visible clues.",
            )
        )
    else:
        for node in candidates:
            result.evidence.append(
                Evidence(
                    "F.4",
                    node.id,
                    f"{node.id} is above layer {max_view_layer} and only appears through clues.",
                )
            )
    return result
