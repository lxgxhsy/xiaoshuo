from __future__ import annotations

from domain.chapter.models import ChapterDraft
from domain.graph.models import WorldGraph
from generation.perspective.build_perspective import build_perspective_view
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_perspective_information(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="A.1")
    for event in draft.events:
        view = build_perspective_view(graph, event.actor_id)
        for knowledge_id in event.used_information:
            perspective_node = view.known_information.get(knowledge_id)
            if perspective_node is None:
                result.failures.append(
                    ValidationFailure(
                        "A.1",
                        event.id,
                        f"{event.actor_id} used {knowledge_id} without knowing it.",
                        "Add a KNOWS/BELIEVES relation or remove the information from the decision.",
                    )
                )
                continue
            if perspective_node.uncertain and knowledge_id not in event.uncertain_information:
                result.failures.append(
                    ValidationFailure(
                        "F.3",
                        event.id,
                        f"{event.actor_id} treated unreliable {knowledge_id} as certain.",
                        "Mark the information as uncertain in the event.",
                    )
                )
            else:
                result.evidence.append(
                    Evidence("A.1", event.id, f"{event.actor_id} used visible knowledge {knowledge_id}.")
                )
    return result


def validate_resource_consideration(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="A.2")
    protagonist_ids = {
        character_id for character_id, character in graph.characters.items() if character.is_protagonist
    }
    for event in draft.events:
        if event.actor_id in protagonist_ids:
            continue
        actor = graph.character(event.actor_id)
        for resource_id in event.available_solution_resources:
            if not actor.has_resource(resource_id):
                continue
            if (
                resource_id not in event.considered_resources
                and resource_id not in event.omitted_resource_reasons
            ):
                result.failures.append(
                    ValidationFailure(
                        "A.2",
                        event.id,
                        f"{event.actor_id} had available resource {resource_id} but did not consider it.",
                        "Consider the resource or record an internal reason for not using it.",
                    )
                )
            else:
                result.evidence.append(
                    Evidence("A.2", event.id, f"{event.actor_id} considered {resource_id}.")
                )
    return result


def validate_goal_alignment(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="A.3")
    for event in draft.events:
        if event.supports_actor_goal or event.goal_deviation_reason:
            result.evidence.append(
                Evidence("A.3", event.id, f"{event.actor_id} action has goal support or reason.")
            )
            continue
        character = graph.character(event.actor_id)
        result.failures.append(
            ValidationFailure(
                "A.3",
                event.id,
                f"{event.actor_id} action does not serve long-term goal: {character.long_term_goal}.",
                "Add an internal motive or change the decision.",
            )
        )
    return result
