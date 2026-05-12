from __future__ import annotations

from dataclasses import dataclass, field

from domain.graph.models import CausalChainStep


@dataclass(frozen=True)
class KnowledgeTransfer:
    sender_id: str
    receiver_id: str
    knowledge_id: str
    received_as_full: bool = False
    failed: bool = False


@dataclass
class ChapterEvent:
    id: str
    viewpoint_character_id: str
    actor_id: str
    description: str
    event_type: str
    target_id: str | None = None
    used_information: list[str] = field(default_factory=list)
    uncertain_information: list[str] = field(default_factory=list)
    information_gained: list[str] = field(default_factory=list)
    information_transfers: list[KnowledgeTransfer] = field(default_factory=list)
    used_skills: list[str] = field(default_factory=list)
    consumed_resources: dict[str, int] = field(default_factory=dict)
    available_solution_resources: list[str] = field(default_factory=list)
    considered_resources: list[str] = field(default_factory=list)
    omitted_resource_reasons: dict[str, str] = field(default_factory=dict)
    supports_actor_goal: bool = True
    goal_deviation_reason: str | None = None
    triggered_hard_rule_ids: list[str] = field(default_factory=list)
    hard_rule_effects_applied: list[str] = field(default_factory=list)
    protagonist_power_level: int | None = None
    opponent_power_level: int | None = None
    outcome: str | None = None
    causal_chain: list[CausalChainStep] = field(default_factory=list)
    irreversible_costs: list[str] = field(default_factory=list)
    dangerous_information_consequences: list[str] = field(default_factory=list)
    power_before: int | None = None
    power_after: int | None = None
    time_spent: int | None = None
    minimum_time_required: int | None = None
    time_compression_reason: str | None = None


@dataclass
class ChapterDraft:
    id: str
    title: str
    viewpoint_character_ids: list[str]
    events: list[ChapterEvent]
    text: str = ""


@dataclass(frozen=True)
class PerspectiveEventVersion:
    event_id: str
    character_id: str
    claimed_facts: set[str] = field(default_factory=set)
    omitted_facts: set[str] = field(default_factory=set)
    emotional_frame: str = ""
    distortion_sources: list[str] = field(default_factory=list)
