from __future__ import annotations

from dataclasses import dataclass

from domain.graph.models import WorldGraph
from domain.knowledge.models import KnowledgeNode


@dataclass(frozen=True)
class PerspectiveKnowledge:
    id: str
    content: str
    reliability: str
    danger_level: str
    cognitive_layer: int
    uncertain: bool
    distorted: bool


@dataclass(frozen=True)
class PerspectiveView:
    character_id: str
    resources: dict[str, int]
    known_information: dict[str, PerspectiveKnowledge]
    cognitive_layer: int
    core_desire: str
    long_term_goal: str
    current_goal: str


def apply_cognitive_decay(node: KnowledgeNode, receiver_layer: int) -> PerspectiveKnowledge | None:
    if node.cognitive_layer <= receiver_layer:
        return PerspectiveKnowledge(
            id=node.id,
            content=node.content,
            reliability=node.reliability,
            danger_level=node.danger_level,
            cognitive_layer=node.cognitive_layer,
            uncertain=not node.is_absolute(),
            distorted=False,
        )
    if not node.expressible_in_lower_layers:
        return None
    return PerspectiveKnowledge(
        id=node.id,
        content=f"decayed:{node.id}",
        reliability=node.reliability,
        danger_level=node.danger_level,
        cognitive_layer=receiver_layer,
        uncertain=True,
        distorted=True,
    )


def build_perspective_view(graph: WorldGraph, character_id: str) -> PerspectiveView:
    character = graph.character(character_id)
    visible: dict[str, PerspectiveKnowledge] = {}
    for knowledge_id, node in graph.knowledge.items():
        if not graph.character_knows(character_id, knowledge_id):
            continue
        perspective_node = apply_cognitive_decay(node, character.cognitive_layer)
        if perspective_node is not None:
            visible[knowledge_id] = perspective_node

    return PerspectiveView(
        character_id=character.id,
        resources=dict(character.resources),
        known_information=visible,
        cognitive_layer=character.cognitive_layer,
        core_desire=character.core_desire,
        long_term_goal=character.long_term_goal,
        current_goal=character.current_goal,
    )
