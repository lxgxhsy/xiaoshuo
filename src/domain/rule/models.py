from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class HardRule:
    id: str
    name: str
    rule_type: str
    condition: str
    effect: str
    is_hard: bool = True
    exceptions: list[str] = field(default_factory=list)
