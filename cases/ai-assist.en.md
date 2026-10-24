# AI-Assist: a private AI gateway for Apple Watch and iPhone

<p align="right"><sub><a href="ai-assist.pt-BR.md">Português</a></sub></p>
## Context

AI-Assist is a personal project: an assistant for Apple Watch, with an iPhone companion, that reaches large language models only through a gateway I control. It follows a multi-wave roadmap. This case covers the first four waves (foundation, Apple clients, the gateway with persistence and sync, and the provider layer), which closed with a frozen test battery, a written reconciliation and an independent review.

## Challenge

- Let a watch use AI providers without any device ever holding a provider key.
- Keep spending bounded and stoppable by the owner.
- Route between models without hiding which model answered.
- Sync personal memory across devices while keeping some context away from external AI.

## My role

Owner, architect and engineer of the project: product scope, architecture, the 14 architecture decision records, Swift and TypeScript implementation, database schema and row-level security policies, test strategy, security tooling and the review process.

## Architecture

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/cases/ai-assist-architecture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/cases/ai-assist-architecture-light.svg">
  <img alt="AI-Assist architecture and real status: watch and phone clients, private AI gateway, model router without silent fallback, mock adapter active, Anthropic and OpenAI adapters ready but never called, infrastructure lab not merged." src="../assets/cases/ai-assist-architecture-dark.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/cases/ai-assist-flow-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/cases/ai-assist-flow-light.svg">
  <img alt="AI-Assist request and response sequence in seven steps from the device through the gateway, router and adapter to a simulated provider and back, with sanitized log events." src="../assets/cases/ai-assist-flow-dark.svg" width="100%">
</picture>


```
Apple Watch / iPhone
  → client apps (SwiftUI, shared Swift core, zero external Swift dependencies)
  → private AI gateway (TypeScript on Node.js, no web framework)
  → model router (catalog-based, lifecycle- and context-aware)
  → model adapters (mock, simulated, Anthropic, OpenAI)
  → providers (to date, only mock and simulated providers have answered)
```

A turn: the client authenticates with a device session; the gateway rejects unexpected origins and applies size limits, a per-device rate limit and a scope check; generation runs inside the device's row-level security context; the context policy is applied; the router resolves the model; memory and summaries enter the prompt as data, outside the system instruction; the ledger reserves budget; the adapter calls out through an exact-URL egress allowlist; deltas are persisted and streamed back; the reservation settles with recorded usage.

Cross-cutting concerns:

- **Device identity and pairing.** Per-device P-256 keys (Secure Enclave when available), signed owner approval for pairing, short hashed sessions, and revocation that also closes open streams.
- **Server-side secrets.** Provider keys exist only on the gateway; the client interface has no key parameter. The device credential stays in the Keychain, bound to that device.
- **Budget ledger and kill switch.** Durable reserve-then-settle ledger, daily caps, persistent owner kill switch. Costs are estimates from an owner-maintained price table.
- **Rate limiting.** Per-device limits plus a separate limiter for public routes.
- **Sanitized logging.** Field allowlist and secret redaction; conversation content is never logged.
- **Persistence with row-level security.** PostgreSQL with row-level security, audit triggers and versioned migrations.
- **Sync.** Change feed with signed cursors and idempotent import.

## Decisions and trade-offs

- **No silent fallback.** Fallback exists only as explicit catalog rules, only before the first token, and the shipped catalogs define none.
- **Keys only on the gateway.** An extra component to operate, in exchange for devices that never carry provider credentials.
- **Unknown cost is refused.** A model without a price entry cannot run. Real AI also requires two locks (activation policy and budget) plus catalog, price, cap and kill switch.
- **A single runtime dependency.** The gateway has no web framework and depends only on the PostgreSQL driver, keeping the supply-chain surface small.
- **Native Apple.** SwiftUI for watchOS and iOS, no cross-platform framework.
- **Consent split.** Sync and sending content to external AI are separate permissions. Third-party professional context is never sent to external AI.

## Engineering practices

- **14 ADRs**, from native Apple and the private gateway to credential policy, per-device identity, and provider activation and budget.
- **Test battery.** One local script runs every suite, with database tests on ephemeral PostgreSQL clusters. A network lock blocks outbound calls during tests.
- **Independent AI review.** A separate AI model reviewed the work over several rounds; the final, static re-verification returned "approved with non-blocking reservations".
- **Security tooling.** Secret scanning, static analysis with 22 tested custom rules, dependency audit and an offline supply-chain check.

## Results

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/cases/ai-assist-evidence-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="../assets/cases/ai-assist-evidence-light.png">
  <img alt="Simulator screenshots: Apple Watch and iPhone conversations whose answers are labelled simulated, and the budget screen with the kill switch and refusal of unknown costs." src="../assets/cases/ai-assist-evidence-dark.png" width="100%">
</picture>


Test results as recorded in the final battery:

| Suite | Result |
|---|---|
| Gateway unit | 187/187 passing |
| Database (ephemeral PostgreSQL) | 136/136 passing |
| Swift core | 128 tests, 14 skipped, 0 failures |
| Hosted iOS app | 9 passing |
| iPhone and Watch UI | passing on the final run (the Watch suite failed once on a test-side issue and passed on rerun) |
| Swift ↔ gateway | 5 integration + 7 end-to-end passing |

A joint UI journey also ran both simulators against a real local gateway and the mock provider, from pairing to conversation, budget and memory editing. The design is recorded in 14 ADRs.

## Current status

| Area | Status |
|---|---|
| watchOS app and iOS companion | Implemented; validated in simulator |
| Gateway, identity and pairing, budget ledger, kill switch, rate limiting, logging | Implemented; validated locally |
| Persistence with row-level security, sync, memory | Implemented; validated locally |
| Model router, mock and simulated adapters | Implemented; validated offline |
| Anthropic and OpenAI adapters | Implemented; blocked, never called |
| Keyless provider auth, circuit breaker, provider rate limiting, exact cost | Lab-only (unmerged branch) |
| Notifications, health data, widgets and complications, policy engine, developer tools | Planned |
| CI pipeline, cloud hosting | Planned (design and templates only, never applied) |

## Limitations

- Prototype. All provider responses so far came from mock or simulated providers; the real Anthropic and OpenAI adapters exist but have never been called.
- No App Store or TestFlight. Not deployed.
- No macOS app.
- No LLM evaluations; only deterministic, offline prompt-injection tests.
- No CI; the battery runs locally.
- Physical-device acceptance pending.
- The infra-lab work (keyless provider auth, circuit breaker, provider rate limiting, exact cost) is an unmerged lab branch with no recorded test run after those changes.
- Residual risks: a short revocation window, partial prompt-injection mitigation, a base image pinned by tag, and revoked sync keeping already-synced copies.

## Lessons learned

- Refusal as the default is testable: real activation is blocked by design, and the activation check is expected to fail.
- Offline validation is not live validation, so the provider wave is recorded as "offline validated, live API pending".
- Report the run, not only the result: the Watch UI rerun is recorded.
- A lab branch protected the main line, at the price of a pending reconciliation.

## What is intentionally not shown

Source code, configuration, endpoints, credentials, test fixtures, review transcripts, prompts, logs and environment details. Any screenshots use synthetic simulator data.

---
<sub>Sanitized case study. The source code is private; this page shows architecture, decisions and verifiable status only. · <a href="../README.md">Back to profile</a></sub>
