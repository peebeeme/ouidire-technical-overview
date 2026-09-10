# Benchmarks and evaluation

This page defines what OuiDire intends to measure. It deliberately contains no unverified production claims.

## Evaluation dimensions

| Dimension | Example measure | Why it matters |
|---|---|---|
| Extraction | character/word error on controlled samples | downstream reasoning cannot repair missing evidence reliably |
| Structure | correct page and paragraph association | reviewers need faithful documentary context |
| Segmentation | complete, non-mutilated assertion rate | cards must remain intelligible and checkable |
| Grounding | findings with valid supporting references | limits unsupported synthesis |
| Suggestions | precision, recall, reviewer acceptance | measures analytical usefulness |
| Synthesis | coverage and unsupported-claim rate | tests higher-level reliability |
| Operations | median and tail latency by stage | reveals practical workflow cost |
| Economics | provider cost per page/document/corpus | supports sustainable deployment |

## Minimum publication standard

A public benchmark should include:

- a versioned, synthetic or properly licensed test corpus;
- the exact task and success criteria;
- model and configuration identifiers where disclosure is permitted;
- sample size and date;
- median plus tail latency, not only the best run;
- human-review procedure and disagreement handling;
- known limitations and failed cases.

## Planned public artefacts

- synthetic extraction and segmentation fixture;
- citation-preservation test set;
- card-level suggestion evaluation protocol;
- document/corpus synthesis rubric;
- cost and latency report with reproducible methodology.

Until these artefacts exist, performance numbers belong in private operational reporting, not public claims.
