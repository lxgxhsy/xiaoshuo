from __future__ import annotations

from domain.chapter.models import ChapterDraft
from domain.graph.models import WorldGraph
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_cognitive_decay(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="F.2")
    for event in draft.events:
        for transfer in event.information_transfers:
            receiver = graph.character(transfer.receiver_id)
            node = graph.knowledge_node(transfer.knowledge_id)
            if node.cognitive_layer <= receiver.cognitive_layer:
                result.evidence.append(
                    Evidence("F.2", event.id, f"{transfer.knowledge_id} is within receiver layer.")
                )
                continue
            if not node.expressible_in_lower_layers and not transfer.failed:
                result.failures.append(
                    ValidationFailure(
                        "F.2",
                        event.id,
                        f"{transfer.knowledge_id} cannot be expressed in lower layers but did not fail.",
                        "Mark the transfer as failed or remove the full knowledge gain.",
                    )
                )
            elif node.expressible_in_lower_layers and transfer.received_as_full:
                result.failures.append(
                    ValidationFailure(
                        "F.2",
                        event.id,
                        f"{transfer.knowledge_id} crossed cognitive layers without decay.",
                        "Record a distorted or uncertain lower-layer version.",
                    )
                )
            else:
                result.evidence.append(
                    Evidence("F.2", event.id, f"{transfer.knowledge_id} decayed or failed correctly.")
                )
    return result
