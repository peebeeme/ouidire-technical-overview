#!/usr/bin/env python3
"""Validate and report traceability in a synthetic OuiDire record."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PAGE_PATTERN = re.compile(r"\bp\.\s*(\d+)\b", re.IGNORECASE)


@dataclass(frozen=True)
class Trace:
    finding_id: str
    finding_summary: str
    card_id: str
    document_id: str
    document_title: str
    source_reference: str


@dataclass
class ValidationResult:
    record_id: str
    traces: list[Trace]
    errors: list[str]

    @property
    def valid(self) -> bool:
        return not self.errors


def _required_text(value: Any, path: str, errors: list[str]) -> str:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path} must be a non-empty string")
        return ""
    return value.strip()


def validate_record(data: Any) -> ValidationResult:
    errors: list[str] = []
    traces: list[Trace] = []

    if not isinstance(data, dict):
        return ValidationResult("unknown", [], ["record must be a JSON object"])

    record_id = _required_text(data.get("record_id"), "record_id", errors) or "unknown"
    documents = data.get("documents")
    findings = data.get("findings")
    if not isinstance(documents, list):
        documents = []
        errors.append("documents must be an array")
    if not isinstance(findings, list):
        findings = []
        errors.append("findings must be an array")

    document_ids: set[str] = set()
    cards: dict[str, tuple[str, str, int, str]] = {}

    for document_index, document in enumerate(documents):
        base = f"documents[{document_index}]"
        if not isinstance(document, dict):
            errors.append(f"{base} must be an object")
            continue
        document_id = _required_text(document.get("document_id"), f"{base}.document_id", errors)
        title = _required_text(document.get("title"), f"{base}.title", errors)
        pages = document.get("pages")
        if not isinstance(pages, int) or isinstance(pages, bool) or pages < 1:
            errors.append(f"{base}.pages must be a positive integer")
            pages = 0
        if document_id in document_ids:
            errors.append(f"duplicate document_id: {document_id}")
        document_ids.add(document_id)

        document_cards = document.get("cards")
        if not isinstance(document_cards, list):
            errors.append(f"{base}.cards must be an array")
            continue
        for card_index, card in enumerate(document_cards):
            card_path = f"{base}.cards[{card_index}]"
            if not isinstance(card, dict):
                errors.append(f"{card_path} must be an object")
                continue
            card_id = _required_text(card.get("card_id"), f"{card_path}.card_id", errors)
            reference = _required_text(
                card.get("source_reference"), f"{card_path}.source_reference", errors
            )
            _required_text(card.get("source_excerpt"), f"{card_path}.source_excerpt", errors)
            if card_id in cards:
                errors.append(f"duplicate card_id: {card_id}")
            cards[card_id] = (document_id, title, pages, reference)

            if reference and document_id and not reference.startswith(document_id):
                errors.append(f"{card_id} source_reference must begin with {document_id}")
            page_match = PAGE_PATTERN.search(reference)
            if not page_match:
                errors.append(f"{card_id} source_reference has no page number")
            elif pages and int(page_match.group(1)) > pages:
                errors.append(
                    f"{card_id} references page {page_match.group(1)}, "
                    f"but {document_id} has {pages} page(s)"
                )

    finding_ids: set[str] = set()
    for finding_index, finding in enumerate(findings):
        base = f"findings[{finding_index}]"
        if not isinstance(finding, dict):
            errors.append(f"{base} must be an object")
            continue
        finding_id = _required_text(finding.get("finding_id"), f"{base}.finding_id", errors)
        summary = _required_text(finding.get("summary"), f"{base}.summary", errors)
        if finding_id in finding_ids:
            errors.append(f"duplicate finding_id: {finding_id}")
        finding_ids.add(finding_id)
        card_ids = finding.get("card_ids")
        if not isinstance(card_ids, list) or not card_ids:
            errors.append(f"{base}.card_ids must be a non-empty array")
            continue
        for card_id in card_ids:
            if not isinstance(card_id, str) or not card_id:
                errors.append(f"{base}.card_ids contains an invalid identifier")
                continue
            card = cards.get(card_id)
            if card is None:
                errors.append(f"{finding_id} references unknown card: {card_id}")
                continue
            document_id, title, _pages, reference = card
            traces.append(Trace(finding_id, summary, card_id, document_id, title, reference))

    return ValidationResult(record_id, traces, errors)


def render_report(result: ValidationResult) -> str:
    status = "PASS" if result.valid else "FAIL"
    lines = [
        "# Traceability validation report",
        "",
        f"- Record: `{result.record_id}`",
        f"- Status: **{status}**",
        f"- Resolved evidence links: **{len(result.traces)}**",
        f"- Validation errors: **{len(result.errors)}**",
        "",
    ]
    if result.traces:
        lines.extend(
            [
                "## Resolved traceability",
                "",
                "| Finding | Supporting card | Document | Source reference |",
                "|---|---|---|---|",
            ]
        )
        for trace in result.traces:
            lines.append(
                f"| `{trace.finding_id}` — {trace.finding_summary} "
                f"| `{trace.card_id}` | `{trace.document_id}` — {trace.document_title} "
                f"| {trace.source_reference} |"
            )
        lines.append("")
    if result.errors:
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in result.errors)
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path, help="path to a synthetic record JSON file")
    parser.add_argument("--report", type=Path, help="write a Markdown validation report")
    args = parser.parse_args()

    try:
        data = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Unable to read record: {exc}", file=sys.stderr)
        return 2

    result = validate_record(data)
    report = render_report(result)
    if args.report:
        args.report.write_text(report + "\n", encoding="utf-8")
    print(report)
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
