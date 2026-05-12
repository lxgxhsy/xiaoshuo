from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SkillCost:
    resource_id: str
    quantity: int
    description: str
    hidden_from_viewpoint: bool = False


@dataclass
class SkillDefinition:
    id: str
    name: str
    law_rank: int
    description: str
    activation_condition: str
    visible_effect: str
    costs: list[SkillCost] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)
    hard_rule_ids: list[str] = field(default_factory=list)
    is_perpetual_motion_claim: bool = False

    def has_tracked_cost(self) -> bool:
        return bool(self.costs)
