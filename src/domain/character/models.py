from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CharacterBelief:
    knowledge_id: str
    confidence: float
    reason: str
    uncertain: bool = True


@dataclass
class CharacterProfile:
    id: str
    name: str
    core_desire: str
    long_term_goal: str
    current_goal: str
    resources: dict[str, int] = field(default_factory=dict)
    known_information: set[str] = field(default_factory=set)
    beliefs: dict[str, CharacterBelief] = field(default_factory=dict)
    cognitive_layer: int = 1
    power_level: int = 0
    constraints: list[str] = field(default_factory=list)
    relationships: dict[str, str] = field(default_factory=dict)
    is_protagonist: bool = False

    def has_resource(self, resource_id: str, quantity: int = 1) -> bool:
        return self.resources.get(resource_id, 0) >= quantity
