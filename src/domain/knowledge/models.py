from __future__ import annotations

from dataclasses import dataclass, field


SAFE = "safe"
ABSOLUTE = "absolute"


@dataclass
class KnowledgeNode:
    id: str
    content: str
    source: str
    reliability: str
    danger_level: str = SAFE
    cognitive_layer: int = 1
    known_by: set[str] = field(default_factory=set)
    distortion_rules: list[str] = field(default_factory=list)
    expressible_in_lower_layers: bool = True
    foreshadowing_evidence: list[str] = field(default_factory=list)

    def is_dangerous(self) -> bool:
        return self.danger_level != SAFE

    def is_absolute(self) -> bool:
        return self.reliability == ABSOLUTE
