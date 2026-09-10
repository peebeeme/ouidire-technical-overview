# Traceability demo

A zero-dependency Python demonstration of one core OuiDire property:

```text
finding → card → document → source reference
```

The validator reads the repository's synthetic record, resolves every finding to its supporting cards, confirms that each card belongs to a document, and checks that its documentary reference names that document and points to a valid page.

This is intentionally small. It demonstrates a public data contract and traceability invariant, not OuiDire's proprietary analysis, prompts, taxonomy, or scoring.

## Run

Python 3.10 or newer is recommended. No packages are required.

```bash
cd examples/traceability-demo
python validate_traceability.py ../synthetic-record.json --report report.md
```

A successful run exits with status `0`. Validation errors produce a non-zero exit status and are listed in the report.

## Test

```bash
python -m unittest discover -s tests -v
```

## Demonstrated invariants

- identifiers are present and unique;
- a finding references at least one existing card;
- every card belongs to exactly one known document;
- a source reference begins with its document identifier;
- referenced page numbers fall within the declared document page count;
- source excerpts are not empty.

## Licence

This directory is licensed under the MIT License. See [`LICENSE`](LICENSE). The licence applies only to this demonstration utility, not to OuiDire's production code or to the rest of this repository.
