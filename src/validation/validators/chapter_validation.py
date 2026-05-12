from __future__ import annotations

from domain.chapter.models import ChapterDraft
from domain.graph.models import WorldGraph
from validation.reports.models import ValidationReport
from validation.validators.cognitive_decay import validate_cognitive_decay
from validation.validators.dangerous_knowledge import validate_dangerous_knowledge
from validation.validators.hard_rules import validate_hard_rules
from validation.validators.perspective import (
    validate_goal_alignment,
    validate_perspective_information,
    validate_resource_consideration,
)
from validation.validators.resource_balance import validate_resource_balance
from validation.validators.skill_costs import validate_skill_costs
from validation.validators.strength_gap import validate_strength_gap


def validate_chapter_draft(draft: ChapterDraft, graph: WorldGraph) -> ValidationReport:
    return ValidationReport(
        results=[
            validate_perspective_information(draft, graph),
            validate_resource_consideration(draft, graph),
            validate_goal_alignment(draft, graph),
            validate_strength_gap(draft, graph),
            validate_hard_rules(draft, graph),
            validate_skill_costs(draft, graph),
            validate_resource_balance(draft, graph),
            validate_cognitive_decay(draft, graph),
            validate_dangerous_knowledge(draft, graph),
        ]
    )
