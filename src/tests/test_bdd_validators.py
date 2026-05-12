from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domain.chapter.models import (
    ChapterDraft,
    ChapterEvent,
    KnowledgeTransfer,
    PerspectiveEventVersion,
)
from domain.character.models import CharacterProfile
from domain.graph.models import CausalChainStep, WorldGraph
from domain.knowledge.models import KnowledgeNode
from domain.rule.models import HardRule
from domain.skill.models import SkillCost, SkillDefinition
from validation.validators.chapter_validation import validate_chapter_draft
from validation.validators.cognitive_decay import validate_cognitive_decay
from validation.validators.dangerous_knowledge import validate_dangerous_knowledge
from validation.validators.hard_rules import validate_hard_rules
from validation.validators.perspective import (
    validate_perspective_information,
    validate_resource_consideration,
)
from validation.validators.resource_balance import validate_resource_balance
from validation.validators.skill_costs import validate_skill_costs
from validation.validators.strength_gap import validate_strength_gap
from validation.validators.multiperspective import validate_multiperspective_difference
from validation.validators.unknowable_layer import validate_unknowable_layer


def make_graph() -> WorldGraph:
    return WorldGraph(
        characters={
            "protagonist": CharacterProfile(
                id="protagonist",
                name="Xu Guanchao",
                core_desire="clear his brother's name",
                long_term_goal="trace the missing minutes",
                current_goal="audit the west dock clocks",
                resources={"silent_wax": 1, "salt_note": 2},
                known_information={"dock_gap", "wax_cost"},
                cognitive_layer=2,
                power_level=0,
                is_protagonist=True,
            ),
            "inspector": CharacterProfile(
                id="inspector",
                name="Liang Zhu",
                core_desire="preserve city order",
                long_term_goal="enter the inner bureau",
                current_goal="seal the dock incident",
                resources={"field_team": 1, "silent_wax": 3},
                known_information={"dock_gap", "cult_link"},
                cognitive_layer=3,
                power_level=2,
            ),
            "clockmaker": CharacterProfile(
                id="clockmaker",
                name="Pei Mu",
                core_desire="break false time",
                long_term_goal="desynchronize the public clocks",
                current_goal="recover the salt mirror",
                resources={"blind_chime": 1},
                known_information={"eleventh_chime"},
                cognitive_layer=4,
                power_level=3,
            ),
            "courier": CharacterProfile(
                id="courier",
                name="Xia Kui",
                core_desire="save her mother",
                long_term_goal="buy out the treatment contract",
                current_goal="deliver the salt mirror",
                resources={"future_minutes": 7, "salt_mirror": 1},
                known_information={"perpetual_rumor"},
                cognitive_layer=2,
                power_level=1,
            ),
        },
        knowledge={
            "dock_gap": KnowledgeNode(
                id="dock_gap",
                content="The west dock records are seven minutes short.",
                source="clock ledger",
                reliability="absolute",
                danger_level="safe",
                cognitive_layer=1,
                known_by={"protagonist", "inspector"},
            ),
            "cult_link": KnowledgeNode(
                id="cult_link",
                content="The missing minutes may involve the silent order.",
                source="field rumor",
                reliability="rumor",
                danger_level="safe",
                cognitive_layer=2,
                known_by={"inspector"},
            ),
            "wax_cost": KnowledgeNode(
                id="wax_cost",
                content="Burning silent wax erases one auditory memory.",
                source="bureau manual",
                reliability="absolute",
                danger_level="unsafe",
                cognitive_layer=2,
                known_by={"protagonist"},
            ),
            "eleventh_chime": KnowledgeNode(
                id="eleventh_chime",
                content="The impossible chime exists above the city clocks.",
                source="salt mirror",
                reliability="unknown",
                danger_level="fatal",
                cognitive_layer=5,
                known_by={"clockmaker"},
                expressible_in_lower_layers=False,
            ),
            "white_day_source": KnowledgeNode(
                id="white_day_source",
                content="The source of the daylight error is not knowable yet.",
                source="world layer",
                reliability="unknown",
                danger_level="fatal",
                cognitive_layer=6,
                known_by=set(),
                expressible_in_lower_layers=False,
                foreshadowing_evidence=["missing minutes"],
            ),
            "perpetual_rumor": KnowledgeNode(
                id="perpetual_rumor",
                content="A device can keep moving without visible fuel.",
                source="guild rumor",
                reliability="rumor",
                danger_level="unsafe",
                cognitive_layer=2,
                known_by={"courier"},
            ),
        },
        hard_rules={
            "silent_wax_cost": HardRule(
                id="silent_wax_cost",
                name="Silent wax consumes hearing memory",
                rule_type="resource_cost",
                condition="A character burns silent wax.",
                effect="The user loses one concrete auditory memory.",
                is_hard=True,
            )
        },
        skills={
            "perpetual_pendulum": SkillDefinition(
                id="perpetual_pendulum",
                name="Perpetual Pendulum",
                law_rank=7,
                description="Motion appears free but is paid by time debt.",
                activation_condition="Close a tidal-copper loop.",
                visible_effect="A mechanism moves without visible fuel.",
                costs=[
                    SkillCost(
                        resource_id="future_minutes",
                        quantity=7,
                        description="Seven future minutes are consumed.",
                        hidden_from_viewpoint=True,
                    )
                ],
                hard_rule_ids=["perpetual_motion_debt"],
                is_perpetual_motion_claim=True,
            ),
            "fake_perpetual_pendulum": SkillDefinition(
                id="fake_perpetual_pendulum",
                name="Fake Perpetual Pendulum",
                law_rank=7,
                description="Invalid free-energy claim.",
                activation_condition="None.",
                visible_effect="Free motion.",
                is_perpetual_motion_claim=True,
            ),
        },
    )


class BddValidatorTests(unittest.TestCase):
    def test_actor_cannot_use_unknown_information(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="unknown information",
            viewpoint_character_ids=["protagonist"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="protagonist",
                    actor_id="protagonist",
                    event_type="investigation",
                    description="Xu acts on a secret he has not learned.",
                    used_information=["cult_link"],
                )
            ],
        )

        result = validate_perspective_information(draft, graph)

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "A.1")

    def test_unreliable_information_must_remain_uncertain(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="rumor certainty",
            viewpoint_character_ids=["inspector"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="inspector",
                    actor_id="inspector",
                    event_type="investigation",
                    description="The inspector treats a rumor as a lead, not a fact.",
                    used_information=["cult_link"],
                    uncertain_information=["cult_link"],
                )
            ],
        )

        result = validate_perspective_information(draft, graph)

        self.assertTrue(result.passed)

    def test_dangerous_used_information_must_have_consequence(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="unsafe wax",
            viewpoint_character_ids=["protagonist"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="protagonist",
                    actor_id="protagonist",
                    event_type="ritual",
                    description="Xu uses a dangerous rule without any recorded consequence.",
                    used_information=["wax_cost"],
                )
            ],
        )

        result = validate_dangerous_knowledge(draft, graph)

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "F.1")

    def test_villain_must_consider_available_solution_resource(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="ignored resource",
            viewpoint_character_ids=["inspector"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="inspector",
                    actor_id="inspector",
                    event_type="containment",
                    description="The inspector ignores his field team for no reason.",
                    available_solution_resources=["field_team"],
                )
            ],
        )

        result = validate_resource_consideration(draft, graph)

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "A.2")

    def test_hard_rule_applies_to_protagonist(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="wax cost",
            viewpoint_character_ids=["protagonist"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="protagonist",
                    actor_id="protagonist",
                    event_type="ritual",
                    description="Xu burns silent wax but keeps all memories.",
                    triggered_hard_rule_ids=["silent_wax_cost"],
                )
            ],
        )

        result = validate_hard_rules(draft, graph)

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "E.1")

    def test_breakthrough_consumes_tracked_resource(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="resource balance",
            viewpoint_character_ids=["protagonist"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="protagonist",
                    actor_id="protagonist",
                    event_type="breakthrough",
                    description="Xu improves without cost.",
                    power_before=0,
                    power_after=1,
                )
            ],
        )

        result = validate_resource_balance(draft, graph)

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "D.1")

    def test_perpetual_motion_skill_requires_tracked_costs(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="fake perpetual motion",
            viewpoint_character_ids=["courier"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="courier",
                    actor_id="courier",
                    event_type="device_activation",
                    description="A fake engine moves forever without any tracked cost.",
                    used_skills=["fake_perpetual_pendulum"],
                )
            ],
        )

        result = validate_skill_costs(draft, graph)

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "D.1")

    def test_perpetual_pendulum_passes_when_hidden_cost_is_recorded(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="paid perpetual motion",
            viewpoint_character_ids=["courier"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="courier",
                    actor_id="courier",
                    event_type="device_activation",
                    description="The pendulum keeps the lock moving by consuming future minutes.",
                    used_skills=["perpetual_pendulum"],
                    consumed_resources={"future_minutes": 7},
                )
            ],
        )

        result = validate_skill_costs(draft, graph)

        self.assertTrue(result.passed)

    def test_knowledge_decays_across_cognitive_layers(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="forbidden transfer",
            viewpoint_character_ids=["clockmaker"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="clockmaker",
                    actor_id="clockmaker",
                    event_type="revelation",
                    description="The clockmaker fully explains an inexpressible chime.",
                    information_transfers=[
                        KnowledgeTransfer(
                            sender_id="clockmaker",
                            receiver_id="protagonist",
                            knowledge_id="eleventh_chime",
                            received_as_full=True,
                            failed=False,
                        )
                    ],
                )
            ],
        )

        result = validate_cognitive_decay(draft, graph)

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "F.2")

    def test_higher_level_victory_requires_causal_chain_and_cost(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="limited victory",
            viewpoint_character_ids=["protagonist"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="protagonist",
                    actor_id="protagonist",
                    target_id="clockmaker",
                    event_type="direct_conflict",
                    description="Xu survives by forcing bureau intervention, not by overpowering Pei.",
                    protagonist_power_level=0,
                    opponent_power_level=3,
                    outcome="protagonist_victory",
                    causal_chain=[
                        CausalChainStep(
                            id="s1",
                            description="The inspector's seal order makes Pei retreat.",
                            evidence=["inspector has seal authority"],
                            is_non_replicable=True,
                        )
                    ],
                    irreversible_costs=["Xu loses his mother's final remembered sentence."],
                )
            ],
        )

        result = validate_strength_gap(draft, graph)

        self.assertTrue(result.passed)

    def test_valid_chapter_report_passes_core_checks(self) -> None:
        graph = make_graph()
        draft = ChapterDraft(
            id="c1",
            title="The First Missing Seven Minutes",
            viewpoint_character_ids=["protagonist"],
            events=[
                ChapterEvent(
                    id="e1",
                    viewpoint_character_id="protagonist",
                    actor_id="protagonist",
                    event_type="ritual",
                    description="Xu burns silent wax to inspect the clock ledger.",
                    used_information=["dock_gap", "wax_cost"],
                    consumed_resources={"silent_wax": 1},
                    triggered_hard_rule_ids=["silent_wax_cost"],
                    hard_rule_effects_applied=["silent_wax_cost"],
                    information_gained=["wax_cost"],
                    dangerous_information_consequences=["wax_cost"],
                    time_spent=1,
                    minimum_time_required=1,
                ),
                ChapterEvent(
                    id="e2",
                    viewpoint_character_id="inspector",
                    actor_id="inspector",
                    event_type="containment",
                    description="The inspector considers field action and delays it to avoid public panic.",
                    used_information=["dock_gap", "cult_link"],
                    uncertain_information=["cult_link"],
                    available_solution_resources=["field_team"],
                    considered_resources=["field_team"],
                    omitted_resource_reasons={"field_team": "A visible raid would expose the incident."},
                ),
            ],
        )

        report = validate_chapter_draft(draft, graph)

        self.assertTrue(report.passed, report.failures())

    def test_full_novel_requires_unknowable_layer(self) -> None:
        graph = make_graph()

        result = validate_unknowable_layer(graph, ["protagonist", "inspector", "clockmaker"])

        self.assertTrue(result.passed)

    def test_full_novel_fails_without_unknowable_layer(self) -> None:
        graph = make_graph()
        graph.knowledge["white_day_source"].known_by.add("clockmaker")

        result = validate_unknowable_layer(graph, ["protagonist", "inspector", "clockmaker"])

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "F.4")

    def test_multi_perspective_versions_need_explained_difference(self) -> None:
        versions = [
            PerspectiveEventVersion(
                event_id="dock_trade",
                character_id="protagonist",
                claimed_facts={"a courier fled", "the bell rang late"},
                omitted_facts={"the inspector signaled first"},
                emotional_frame="confusion",
                distortion_sources=["limited line of sight"],
            ),
            PerspectiveEventVersion(
                event_id="dock_trade",
                character_id="inspector",
                claimed_facts={"a suspect fled", "the bell was deliberately muted"},
                omitted_facts={"the courier carried a mirror"},
                emotional_frame="containment",
                distortion_sources=["bureau secrecy"],
            ),
        ]

        result = validate_multiperspective_difference(versions)

        self.assertTrue(result.passed)

    def test_multi_perspective_versions_fail_when_only_rephrased(self) -> None:
        versions = [
            PerspectiveEventVersion(
                event_id="dock_trade",
                character_id="protagonist",
                claimed_facts={"a courier fled"},
                emotional_frame="confusion",
                distortion_sources=["limited line of sight"],
            ),
            PerspectiveEventVersion(
                event_id="dock_trade",
                character_id="inspector",
                claimed_facts={"a courier fled"},
                emotional_frame="confusion",
                distortion_sources=["bureau secrecy"],
            ),
        ]

        result = validate_multiperspective_difference(versions)

        self.assertFalse(result.passed)
        self.assertEqual(result.failures[0].scenario_id, "C.2")


if __name__ == "__main__":
    unittest.main()
