# Security and privacy

## Scope of this repository

This repository contains public documentation and synthetic examples only. Do not submit real records, personal information, credentials, internal URLs, production logs, private prompts, or proprietary datasets in issues or pull requests.

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue. Report it privately to [contact@studiorium.ai](mailto:contact@studiorium.ai) with the subject line `Security — OuiDire`. Do not include personal records or unnecessary sensitive data in the initial message.

## Production principles

The production system is designed around the following principles:

- least-privilege access to infrastructure and providers;
- server-side handling of secrets;
- explicit separation of source, machine-generated, and human-authored data;
- controlled retention and deletion;
- logging that avoids document contents and credentials;
- provider and subprocess isolation where practical;
- reviewable exports and provenance;
- synthetic or formally authorized material for testing.

These principles describe design intent, not a certification. Specific deployment controls must be verified during security diligence.

## Before making this repository public

Run the checks in [`docs/release-checklist.md`](docs/release-checklist.md). Never copy files from the private product repository without reviewing both their current contents and Git history.
