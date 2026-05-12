from __future__ import annotations

from domain.chapter.models import ChapterDraft
from domain.graph.models import WorldGraph
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_resource_balance(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="D.1")
    for event in draft.events:
        actor = graph.character(event.actor_id)
        for resource_id, quantity in event.consumed_resources.items():
            if not actor.has_resource(resource_id, quantity):
                result.failures.append(
                    ValidationFailure(
                        "D.1",
                        event.id,
                        f"{event.actor_id} consumed {quantity} {resource_id} but only has {actor.resources.get(resource_id, 0)}.",
                        "Add the resource to the actor or reduce the consumption.",
                    )
                )
            else:
                result.evidence.append(
                    Evidence("D.1", event.id, f"{event.actor_id} consumed tracked resource {resource_id}.")
                )

        if event.power_before is not None and event.power_after is not None:
            if event.power_after > event.power_before and not event.consumed_resources:
                result.failures.append(
                    ValidationFailure(
                        "D.1",
                        event.id,
                        "Power increased without resource consumption.",
                        "Record CONSUMES/COSTS evidence for the breakthrough.",
                    )
                )
            else:
                result.evidence.append(
                    Evidence("D.1", event.id, "Power change has resource evidence or no increase.")
                )

        if event.minimum_time_required is None or event.time_spent is None:
            continue
        if event.time_spent < event.minimum_time_required and not event.time_compression_reason:
            result.failures.append(
                ValidationFailure(
                    "D.2",
                    event.id,
                    "Required time was compressed without a valid reason.",
                    "Increase time_spent or record a rule-backed compression factor.",
                )
            )
        else:
            result.evidence.append(
                Evidence("D.2", event.id, "Time cost is satisfied or explained.")
            )
    return result
