from __future__ import annotations

from domain.chapter.models import ChapterDraft
from domain.graph.models import WorldGraph
from validation.reports.models import Evidence, ValidationFailure, ValidationResult


def validate_skill_costs(draft: ChapterDraft, graph: WorldGraph) -> ValidationResult:
    result = ValidationResult(scenario_id="D.1")
    for event in draft.events:
        for skill_id in event.used_skills:
            skill = graph.skill(skill_id)
            if skill.is_perpetual_motion_claim and not skill.has_tracked_cost():
                result.failures.append(
                    ValidationFailure(
                        "D.1",
                        event.id,
                        f"{skill_id} claims perpetual motion without tracked costs.",
                        "Add hidden or visible costs to the SkillDefinition.",
                    )
                )
                continue

            for cost in skill.costs:
                consumed = event.consumed_resources.get(cost.resource_id, 0)
                if consumed < cost.quantity:
                    result.failures.append(
                        ValidationFailure(
                            "D.1",
                            event.id,
                            f"{skill_id} requires {cost.quantity} {cost.resource_id} but event records {consumed}.",
                            "Record the skill cost in event.consumed_resources.",
                        )
                    )
                else:
                    result.evidence.append(
                        Evidence(
                            "D.1",
                            event.id,
                            f"{skill_id} cost {cost.resource_id} is tracked.",
                        )
                    )
    return result
