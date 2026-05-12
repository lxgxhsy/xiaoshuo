from __future__ import annotations

from dataclasses import dataclass, field

from domain.character.models import CharacterProfile
from domain.knowledge.models import KnowledgeNode
from domain.rule.models import HardRule
from domain.skill.models import SkillDefinition


@dataclass(frozen=True)
class GraphRelation:
    source_id: str
    relation_type: str
    target_id: str
    evidence: str


@dataclass(frozen=True)
class CausalChainStep:
    id: str
    description: str
    evidence: list[str] = field(default_factory=list)
    is_non_replicable: bool = False


@dataclass
class ResourcePool:
    id: str
    total: int
    holders: dict[str, int] = field(default_factory=dict)

    def consumed_total(self) -> int:
        return sum(self.holders.values())


@dataclass
class WorldGraph:
    characters: dict[str, CharacterProfile] = field(default_factory=dict)
    knowledge: dict[str, KnowledgeNode] = field(default_factory=dict)
    hard_rules: dict[str, HardRule] = field(default_factory=dict)
    skills: dict[str, SkillDefinition] = field(default_factory=dict)
    relations: list[GraphRelation] = field(default_factory=list)
    shared_resources: dict[str, ResourcePool] = field(default_factory=dict)

    def character(self, character_id: str) -> CharacterProfile:
        return self.characters[character_id]

    def knowledge_node(self, knowledge_id: str) -> KnowledgeNode:
        return self.knowledge[knowledge_id]

    def hard_rule(self, rule_id: str) -> HardRule:
        return self.hard_rules[rule_id]

    def skill(self, skill_id: str) -> SkillDefinition:
        return self.skills[skill_id]

    def character_knows(self, character_id: str, knowledge_id: str) -> bool:
        character = self.character(character_id)
        node = self.knowledge_node(knowledge_id)
        return knowledge_id in character.known_information or character_id in node.known_by

    def relations_from(self, source_id: str, relation_type: str | None = None) -> list[GraphRelation]:
        return [
            relation
            for relation in self.relations
            if relation.source_id == source_id
            and (relation_type is None or relation.relation_type == relation_type)
        ]
