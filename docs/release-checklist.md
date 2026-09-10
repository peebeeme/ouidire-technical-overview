# Public-release checklist

## Content

- [x] Replace contact placeholders with the approved public address.
- [ ] Confirm all claims with the product owner.
- [ ] Confirm every example is synthetic or has explicit publication rights.
- [ ] Remove client, patient, partner, investor, and internal project names.
- [ ] Remove private prompts, taxonomies, weights, and provider-routing rules.
- [ ] Review screenshots for names, URLs, tokens, account identifiers, and browser chrome.
- [ ] Decide whether public issue tracking should be enabled.

## Repository hygiene

- [ ] Create this as a new repository; do not preserve history from the private monorepo.
- [ ] Run a secret scanner against files and full Git history.
- [ ] Review large files and generated artefacts.
- [ ] Verify `.gitignore` before the first commit.
- [ ] Confirm author emails in Git metadata are suitable for publication.
- [ ] Add branch protection and require review for the default branch.
- [ ] Enable dependency and secret alerts if executable code is later added.

Suggested local checks:

```bash
gitleaks detect --source . --no-git
git grep -nEi '(api[_-]?key|secret|token|password|private[_-]?key)'
git log --format='%an <%ae>' | sort -u
```

Scanner output still requires human review; absence of a match is not proof that content is safe.

## Legal and positioning

- [ ] Confirm the repository licence.
- [x] Add the correct company/entity copyright holder (Studiorium Inc.).
- [ ] Verify third-party names and trademarks are used accurately.
- [ ] Add appropriate medical/legal decision-support disclaimers.
- [ ] Document a private technical-diligence process.

## Final verification

- [ ] Clone the candidate repository into an empty directory.
- [ ] Inspect the complete file list and rendered Markdown.
- [ ] Ask a reviewer unfamiliar with OuiDire what the repository communicates.
- [ ] Publish only after product, privacy, security, and legal approval.
