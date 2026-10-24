# Engineering Platform: representing private work without falsifying it

<p align="right"><sub><a href="engineering-platform.pt-BR.md">Português</a></sub></p>
## Context

Most of my day-to-day engineering happens in private Azure DevOps repositories. A GitHub profile shows only what GitHub can see, so those commits, pull requests and reviews were invisible there. Copying code, rewriting history or re-authoring commits would misrepresent the work.

## Challenge

Represent engineering activity across providers so that:

- every number can be traced back to a real commit;
- nothing is rewritten, re-authored or attributed to the wrong person;
- no code, secret or confidential name reaches a public surface;
- the system keeps running unattended and says so when it cannot be sure.

## My role

Design and implementation of the platform end to end: inventory, security validation, mirroring, metrics, public aggregation, the authorization model and the operations runbook.

## Architecture

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/cases/engineering-platform-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/cases/engineering-platform-light.svg">
  <img alt="Engineering platform pipeline from Azure DevOps through inventory, security gate, private mirror, collector and public JSON to the profile, with cross-cutting controls." src="../assets/cases/engineering-platform-dark.svg" width="100%">
</picture>


```
Azure DevOps
  → historical inventory (Git DAG + REST, recovery by id)
  → security validation (secret scanning, sensitive-path policy, fail-closed)
  → private one-way mirror (fast-forward only)
  → metrics collector (dedup by SHA)
  → public aggregation (strict schema, aggregates only)
  → GitHub profile
```

**Historical inventory.** Two independent methods. The first walks the Git commit graph across every advertised ref and fetches by id the commits Azure DevOps still names but no ref contains, recovering work from deleted branches. The second reads the REST API: refs, the unfiltered commit listing and every pull request with its commits. Because the unfiltered listing is undocumented, it was checked against the graph walk; the sets became identical after a fix in recovery by id.

**Security validation.** Every range proposed for transfer is scanned with the full default secret-scanning rule set and a sensitive-path policy. Exceptions are exact-fingerprint records with classification, justification, evidence and reviewers, plus one narrowly scoped, reviewed rule. The scanner configuration is pinned by hash: any edit blocks mirroring until re-approved, and a validator rejects configurations that disable rules or use global or unanchored allowlists. Canary tests confirm real-looking secrets are still detected. A real credential is rotated first, or the repository stays unmirrored.

**Private mirror.** Azure DevOps remains the source of truth. A repository is mirrored only from an explicit allowlist that records authorization category, approver, date and basis; corporate or third-party code without redistribution authorization is never mirrored, and undetermined cases are blocked. Each push is one explicit fast-forward refspec: no force, no prune, no rewrite. Destination privacy is re-checked right before every push and the result verified afterwards. SHAs, authors and dates are preserved; reruns are idempotent.

**Metrics collector.** Commits from all platforms are de-duplicated by SHA and reported as separate measures with distinct meanings: engineering activity, where the work lives, sources, delivery, and official GitHub contributions. The official calendar total is never added to engineering activity, and third-party commits keep their authors and are never counted as mine.

**Public aggregation.** The public file is built field by field and validated against a strict schema that fails closed on unknown keys, strings or ranges. Only aggregates are published. A public-repository validator blocks confidential names by comparing truncated hashes, so the blocklist itself is never published.

## Cross-cutting controls

- **Least-privilege tokens per job.** Each job gets its own fine-grained, time-limited token restricted to what it needs. Tokens never appear in URLs, arguments, configuration or logs, and every log record is redacted.
- **Health checks and alerts.** Each mirror is classified (in sync, pending, stale, diverged, missing, not private). Any problem opens or updates a private alert; only a healthy run closes it. Inconclusive checks never close an alert.
- **Cost-aware scheduling.** Reconciliation runs on a fixed interval, with per-job timeouts that bound worst-case runner usage and separate kill switches for mirroring and metrics. Private code is cloned fresh per run, with no shared cache.
- **Independent AI audit.** Secret-scanning exceptions were reviewed by an independent AI reviewer. Changing the pinned scanner-configuration hash is the approval act and must be accompanied by an independent review.

## Decisions and trade-offs

- **Representation over appearance.** With squash merges, feature-branch commits never reach the default branch, so they cannot appear on the GitHub calendar. They are counted on the dashboard instead, separate from official contributions.
- **No history rewrite.** Rewriting would change every SHA. The cost: a finding blocks a repository until triaged.
- **Private destination is not authorization.** Mirroring privately does not replace the code owner's permission.
- **Fail closed.** Missing authorization, a non-private destination, divergence, a scanner block or an unknown public field all stop the pipeline rather than degrade it.

## Results

- **3,414** commits inventoried, **0** unrecoverable.
- **More than 4,300** unique owner-authored commits consolidated across platforms (all history to October 2026, de-duplicated by SHA; the live figure is on the dashboard).
- **235** eligible default-branch commits for official GitHub contributions.
- **149** automated tests.

## Current status and residual state

- Approved repositories are mirrored, and their commit sets are verified against Azure DevOps by SHA, with policy exclusions enforced.
- An early configuration gap let mirrored CI configuration run once; it was contained, audited and turned into permanent controls.
- Dependabot-style automation on mirrors is contained and monitored; the definitive prevention is pending an owner decision.
- The official calendar is compared day by day with the eligible commits: the dashboard shows the most it can be displaying and how many it provably does not show yet. The gap is reported, not rounded.
- The latest metrics reconciliation was a local run; the scheduled hosted run is waiting on a credential permission fix.

## Lessons learned

- Two independent inventory methods were worth the extra work: they only matched after a bug in recovery by id was fixed.
- Numbers that measure different populations are not comparable without an explicit reconciliation table.
- A mirror replicates more than code. Repository automation travels with it, so mirrors need their own controls.
- Inconclusive is its own state: a check that cannot verify must never report recovery.

## What is intentionally not shown

Repository and organization names (other than Azure DevOps), client names, e-mail addresses, token names and scopes, scanning fingerprints, excluded commits, incident details, source code and screenshots.

---
<sub>Sanitized case study. The source code is private; this page shows architecture, decisions and verifiable status only. · <a href="../README.md">Back to profile</a></sub>
