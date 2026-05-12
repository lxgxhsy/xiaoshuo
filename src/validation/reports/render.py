from __future__ import annotations

from validation.reports.models import ValidationReport


def render_validation_report(report: ValidationReport) -> str:
    lines = ["# Validation Report", "", f"passed: {str(report.passed).lower()}", ""]
    for result in report.results:
        lines.append(f"## {result.scenario_id}")
        lines.append("")
        lines.append(f"passed: {str(result.passed).lower()}")
        if result.failures:
            lines.append("")
            lines.append("failures:")
            for failure in result.failures:
                lines.append(
                    f"- {failure.object_id}: {failure.reason} Required: {failure.required_evidence}"
                )
        if result.evidence:
            lines.append("")
            lines.append("evidence:")
            for evidence in result.evidence:
                lines.append(f"- {evidence.object_id}: {evidence.description}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
