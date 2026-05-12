from __future__ import annotations

from domain.chapter.models import ChapterDraft
from domain.graph.models import WorldGraph
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_dangerous_knowledge(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="F.1")
    consequences = {
        knowledge_id
        for event in draft.events
        for knowledge_id in event.dangerous_information_consequences
    }
    for event in draft.events:
        checked_knowledge_ids = set(event.information_gained) | set(event.used_information)
        for knowledge_id in checked_knowledge_ids:
            node = graph.knowledge_node(knowledge_id)
            if not node.is_dangerous():
                continue
            if knowledge_id not in consequences:
                result.failures.append(
                    ValidationFailure(
                        "F.1",
                        event.id,
                        f"{knowledge_id} is dangerous but has no consequence in the draft.",
                        "Add a concrete consequence or delay marker tied to this information.",
                    )
                )
            else:
                result.evidence.append(
                    Evidence("F.1", event.id, f"{knowledge_id} has a recorded consequence.")
                )
    return result
