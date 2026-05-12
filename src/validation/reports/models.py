from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Evidence:
    scenario_id: str
    object_id: str
    description: str


@dataclass(frozen=True)
class ValidationFailure:
    scenario_id: str
    object_id: str
    reason: str
    required_evidence: str
    needs_rewrite: bool = True


@dataclass
class ValidationResult:
    scenario_id: str
    failures: list[ValidationFailure] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures


@dataclass
class ValidationReport:
    results: list[ValidationResult]

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    def failures(self) -> list[ValidationFailure]:
        return [failure for result in self.results for failure in result.failures]
