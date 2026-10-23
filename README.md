<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banners/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banners/hero-light.svg">
  <img alt="Célio Crisólogo — Software Architecture / Backend / Applied AI" src="assets/banners/hero-dark.svg" width="100%">
</picture>

<p align="right"><sub><a href="README.pt-BR.md">Português</a></sub></p>

**Software Architect** focused on backend engineering, distributed systems, cloud infrastructure and applied AI.

For 7+ years I have designed, modernized and operated critical systems in banking, telecom, public-sector tax and enterprise platforms — hands-on in Java, Go and Node.js/TypeScript, and as a technical lead setting engineering standards, quality gates and delivery practices for multidisciplinary teams. Today I lead technical delivery on client engagements and build products at [Includlab](https://includlab.com.br), my software house.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/sections/01-engineering-focus-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/sections/01-engineering-focus-light.svg">
  <img alt="01 — Engineering focus" src="assets/sections/01-engineering-focus-dark.svg" width="520">
</picture>

- **Software Architecture** — Domain-driven boundaries, event-driven integration and legacy modernization (Strangler Fig), documented as decisions that can be reviewed.
- **Backend & Distributed Systems** — Transactional services for regulated, high-volume domains: payments, credit, tax, telecom.
- **Cloud & Platform Engineering** — AWS and Azure, Kubernetes, infrastructure as code, multi-environment promotion.
- **DevOps & CI/CD** — Pipelines with quality gates, preflight checks and traceable promotion from branch to production.
- **Applied AI & Automation** — LLM integration and agent-assisted engineering workflows, with humans owning the decisions.
- **Engineering Leadership** — Standards, reviews, sprint governance, mentoring and hiring.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/sections/02-technology-stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/sections/02-technology-stack-light.svg">
  <img alt="02 — Technology stack" src="assets/sections/02-technology-stack-dark.svg" width="520">
</picture>

| | |
|---|---|
| **Languages** | `Java` `Go` `TypeScript` `Node.js` `Python` `C#` |
| **Backend** | `Spring Boot` `Spring Cloud` `Quarkus` `NestJS` `Express` `Prisma` `Hibernate/JPA` |
| **Cloud & Infra** | `AWS` `Azure` `Kubernetes` `Docker` `Helm` `Terraform` |
| **Data & Messaging** | `PostgreSQL` `Oracle` `MongoDB` `Redis` `Kafka` `RabbitMQ` |
| **DevOps & Quality** | `Azure DevOps` `GitHub Actions` `GitLab CI` `SonarQube` `OAuth2/OIDC` |
| **AI & Agents** | `LLM integration` `LangChain` `Claude Code` `Codex` `Agent workflows` |

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/sections/03-engineering-activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/sections/03-engineering-activity-light.svg">
  <img alt="03 — Engineering activity" src="assets/sections/03-engineering-activity-dark.svg" width="520">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/engineering-activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/engineering-activity-light.svg">
  <img alt="Engineering activity over the last 12 months: commits, pull requests and code reviews across GitHub and Azure DevOps" src="assets/metrics/engineering-activity-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/monthly-commits-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/monthly-commits-light.svg">
  <img alt="Monthly commits for the last 12 months, split by platform" src="assets/metrics/monthly-commits-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/code-by-language-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/code-by-language-light.svg">
  <img alt="Share of code by language across owned repositories" src="assets/metrics/code-by-language-dark.svg" width="100%">
</picture>

<details>
<summary><sub>How these numbers are produced</sub></summary>

<br>

- **Sources:** GitHub REST/GraphQL API and Azure DevOps REST API (official APIs only), collected in a private pipeline. Raw data never leaves it; this page receives aggregated counts only ([`data/public-metrics.json`](data/public-metrics.json)).
- **Commits:** commits I authored on the default branch of each repository, last 12 months. A commit that exists on both platforms (same SHA, e.g. a private mirror) is **counted once**.
- **Pull requests / reviews:** PRs I opened; reviews are PRs by others where I cast a vote or submitted a review.
- **Azure DevOps:** private repositories, shown as aggregates without names.
- **Languages:** bytes per language reported by GitHub Linguist on repositories I own. It describes code volume, not proficiency.
- Commit counts describe activity, not productivity or quality.

</details>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/sections/04-selected-work-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/sections/04-selected-work-light.svg">
  <img alt="04 — Selected work" src="assets/sections/04-selected-work-dark.svg" width="520">
</picture>

#### Athrya &nbsp;<sub><code>PRIVATE</code> · <code>ACTIVE DEVELOPMENT</code></sub>
Multi-tenant platform for martial-arts academies: one universal app for students, web dashboards for staff.
**Decision:** a single TypeScript monorepo where the domain, use cases and contracts live in shared packages that every app depends on — business rules are written once and enforced the same way on mobile, web and API. Tenants are configuration, not forks.
`TypeScript` `Turborepo` `NestJS` `Prisma` `PostgreSQL` `Expo / React Native` `Next.js` `Zod` `Azure DevOps`

#### Includlab &nbsp;<sub><code>COMPANY</code> · <a href="https://includlab.com.br">includlab.com.br</a></sub>
My software house: product engineering, integrations and AI-assisted automation for clients and for our own products such as Athrya.

#### Engineering Activity pipeline &nbsp;<sub><code>PRIVATE</code> · <code>NEW</code></sub>
The system behind section 03. **Problem:** most of my work happens in private Azure DevOps repositories that GitHub cannot see. **Decision:** a one-way, fast-forward-only mirror of explicitly approved repositories into private GitHub repositories — original SHAs, authors and dates preserved, secret scanning before any push, visibility re-checked before every push — plus a collector that deduplicates by SHA and publishes only a validated, aggregate-only JSON schema.
`Python` `GitHub API` `Azure DevOps REST` `gitleaks` `GitHub Actions`

<sub>Earlier public work: <a href="https://github.com/CelioGuimaraes117/NoteApp-master">NoteApp</a> (React, Redux, Material UI) · <a href="https://github.com/CelioGuimaraes117/themesDiscord">themesDiscord</a> (CSS).</sub>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/sections/05-principles-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/sections/05-principles-light.svg">
  <img alt="05 — Principles" src="assets/sections/05-principles-dark.svg" width="520">
</picture>

1. **Simple first.** The best architecture is the smallest one that survives the next two years of requirements.
2. **Decisions are verifiable.** Every significant choice has a record, a reason and a way to tell if it was wrong.
3. **Scale is designed, not hoped for.** Boundaries, back-pressure and data ownership come before infrastructure.
4. **Observable by default.** If it cannot be measured in production, it is not finished.
5. **Secure by construction.** Least privilege, secrets out of code, threat models in the design review.
6. **Maintainability is a feature.** Code is read by the next engineer far more often than it is written.
7. **Clarity over cleverness.** In code, in documents and in conversations with the business.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/sections/06-contact-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/sections/06-contact-light.svg">
  <img alt="06 — Contact" src="assets/sections/06-contact-dark.svg" width="520">
</picture>

[LinkedIn](https://www.linkedin.com/in/celioguimaraes117) · [celio@includlab.com.br](mailto:celio@includlab.com.br) · [Includlab](https://includlab.com.br) · [Links](https://linktr.ee/celio_rguimaraes)

Based in Brazil · working remotely · Portuguese, English, Spanish.

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/signature-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/brand/signature-light.svg">
  <img alt="Célio Crisólogo / Software Architecture / Backend / Applied AI" src="assets/brand/signature-dark.svg" width="380">
</picture>
