<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banners/hero-animated-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banners/hero-animated-light.svg">
  <img alt="Célio Crisólogo — Software Architect, Tech Lead, Applied AI Engineering. I architect systems. I build products. I engineer intelligence." src="assets/banners/hero-animated-dark.svg" width="100%">
</picture>

<p align="right"><b>English</b> | <a href="README.pt-BR.md">Português (Brasil)</a></p>

**Software Architect · Tech Lead · Applied AI Engineering.** I design platforms, take them to production and build AI systems with the guardrails they need. 7+ years in banking, telecom, public-sector tax and enterprise platforms; today I lead technical delivery on client engagements and build products at [Includlab](https://includlab.com.br), my software house.

<sub>The source code of the systems below is private. What is shown here are sanitized architecture views, verifiable status and aggregate metrics, never the implementation.</sub>

## Featured engineering

### 01 · Athrya — platform architecture &nbsp;<sub><code>PRODUCTION</code></sub>

A multi-tenant SaaS for jiu-jitsu academies: schedules, check-in, attendance, belt progression, guardians and supervised minors. One mobile app (App Store and Google Play), web portals and an API, live since October 2026.
**Decision:** the domain, use cases and contracts live in shared TypeScript packages that every surface depends on, so business rules are written once; the API is the single authorization authority and tenant scope is enforced in the data layer. **Delivery:** one mandatory PR gate, additive migrations through a dedicated pipeline, staged deploys with rollback. I own the architecture, the engineering controls, every merge and the go-live sign-offs. → [Read the case](cases/athrya.en.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cases/athrya-architecture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cases/athrya-architecture-light.svg">
  <img alt="Athrya architecture: mobile app, portal, platform admin and invite landing in production, dashboard in development; shared packages; API as the single authorization authority; managed PostgreSQL; delivery pipeline from PR gate to promote or rollback." src="assets/cases/athrya-architecture-dark.svg" width="100%">
</picture>

### 02 · AI-Assist — applied AI engineering &nbsp;<sub><code>PROTOTYPE</code></sub>

Apple Watch and iPhone clients talk to a private AI gateway that owns device identity, budget and kill switch, rate limits and provider keys; a model router with **no silent fallback** chooses an adapter.
**Honest status:** validated in simulators with 187/187 gateway and 136/136 database tests; every response so far comes from a mock or simulated provider; the Anthropic and OpenAI adapters are ready but have never been called; not deployed and not on the App Store. → [Read the case](cases/ai-assist.en.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cases/ai-assist-architecture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cases/ai-assist-architecture-light.svg">
  <img alt="AI-Assist architecture and real status: watch and phone clients, private AI gateway, model router without silent fallback, mock adapter active, Anthropic and OpenAI adapters ready but never called, infrastructure lab kept in a separate copy." src="assets/cases/ai-assist-architecture-dark.svg" width="100%">
</picture>

### 03 · Engineering platform — DevOps intelligence &nbsp;<sub><code>OPERATIONAL</code></sub>

Most of my work lives in private Azure DevOps repositories. This platform makes it visible **without falsifying anything**: a full-history inventory, a fail-closed secret-scanning gate, a one-way fast-forward-only private mirror that keeps the SHA, author and date of every authorized commit it mirrors (security-excluded commits are never mirrored), and a collector that deduplicates by SHA and publishes only aggregates through a strict schema. It produces the numbers below. → [Read the case](cases/engineering-platform.en.md)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cases/engineering-platform-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/cases/engineering-platform-light.svg">
  <img alt="Engineering platform pipeline: Azure DevOps, inventory, security gate, private mirror, collector, public JSON, profile; with least privilege, health and alerts, cost-aware scheduling and independent audit." src="assets/cases/engineering-platform-dark.svg" width="100%">
</picture>

## Engineering proof

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/031-activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/031-activity-light.svg">
  <img alt="Engineering activity across all branches: unique commits attributed to my Git identities in the last 7 days, 30 days, 12 months and all history, with the split between default branch, other live branches and deleted branches recovered by id." src="assets/metrics/v2/031-activity-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/034-delivery-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/034-delivery-light.svg">
  <img alt="Delivery over 12 months: pull requests opened, completed after the mandatory gate, open and abandoned, reviews and squash merges." src="assets/metrics/v2/034-delivery-dark.svg" width="100%">
</picture>

<details>
<summary><b>Where the work lives · sources · GitHub contributions · how the numbers are produced</b></summary>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/032-monthly-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/032-monthly-light.svg">
  <img alt="Monthly unique commits over 12 months, split between default branch and other refs." src="assets/metrics/v2/032-monthly-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/033-sources-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/033-sources-light.svg">
  <img alt="Sources over 12 months: commits only in Azure DevOps, on both platforms with the same SHA (counted once), and only on GitHub." src="assets/metrics/v2/033-sources-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/metrics/v2/035-contributions-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/metrics/v2/035-contributions-light.svg">
  <img alt="GitHub contributions over 12 months: official calendar total, eligible mirrored commits and how many of them the calendar provably does not show yet." src="assets/metrics/v2/035-contributions-dark.svg" width="100%">
</picture>

- Commit counts are based on verified Git author identities, deduplicated by SHA across GitHub and Azure DevOps. They measure repository activity, not manually written lines of code or individual productivity.
- **Four meanings, never added together:** engineering activity (any branch), where it lives, delivery (pull requests and reviews) and GitHub contributions (what GitHub itself recognizes, under its own rules).
- **Sources:** Azure DevOps REST and Git history plus the GitHub API, collected in a private pipeline; this page receives aggregates only ([`data/public-metrics-v2.json`](data/public-metrics-v2.json)). No history was rewritten and no commit was created to fill the calendar.

</details>

## Technology & leadership

- **Architecture** domain-driven boundaries · event-driven integration · legacy modernization · decision records
- **Backend** Java · Go · TypeScript/Node.js (NestJS) · Python · PostgreSQL · Kafka · Redis
- **Platform** Azure · AWS · Kubernetes · Docker · Bicep/Terraform · Azure DevOps · GitHub Actions
- **Applied AI** LLM gateways · multi-provider routing · cost and safety guardrails · evaluation design
- **Leadership** engineering standards · quality gates · release governance · mentoring and hiring

## Contact

[Portfolio](https://www.celiocrisologo.com.br/en) · [LinkedIn](https://www.linkedin.com/in/celioguimaraes117) · [celio@includlab.com.br](mailto:celio@includlab.com.br) · [Includlab](https://includlab.com.br) · [Links](https://linktr.ee/celio_rguimaraes)

Based in Brazil · working remotely · Portuguese, English, Spanish.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/signature-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/brand/signature-light.svg">
  <img alt="Célio Crisólogo / Software Architecture / Backend / Applied AI" src="assets/brand/signature-dark.svg" width="380">
</picture>
