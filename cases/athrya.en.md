# Athrya — a multi-tenant platform for martial-arts academies

<p align="right"><sub><a href="athrya.pt-BR.md">Português</a></sub></p>

## Context

Jiu-jitsu academies run on recurring classes, attendance, belt progression and families, since many students are minors. They often operate as networks, so one person may train at one unit and teach or manage at another. Athrya is a multi-tenant SaaS for this setting. It covers schedules, check-in, attendance and corrections to it, graduation tracking, curriculum, invitations, guardians and supervised minors (ages 13–17), and academy billing administration.

## Challenge

- **Many roles, one dataset.** Students, professors, managers, reception staff and platform operators each need different access. That access depends on which unit they are acting in.
- **Minors' data.** Guardianship, supervised accounts and the transition to adulthood have to be modelled explicitly and handled with care.
- **One engineer.** The safety net had to be automated and enforced, not left to convention.
- **A real launch.** Store review, production infrastructure, migrations and hypercare all had to work on a fixed go-live date in October 2026.

## My role

I was the lead architect and engineer, accountable for the product's architecture, implementation, quality and release.
About 99% of the commits in the product repository between August and October 2026 are attributed to my Git identities;
the remainder comes from three other contributors and an automation identity.

- I defined the domain model, the architecture decisions (13 ADRs, a 22-entry decision log) and the acceptance criteria.
- I set the engineering controls that every change had to pass: one mandatory PR gate, migration policy, security-boundary tests.
- Development used AI-assisted tooling under my specification, review and merge control; every change was independently reviewed before merge.
- I owned every merge and signed off the technical, product and operations go-live approvals.

## Architecture

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="../assets/cases/athrya-architecture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="../assets/cases/athrya-architecture-light.svg">
  <img alt="Athrya architecture: mobile app, portal, platform admin and invite landing in production, dashboard in development; shared packages; API as the single authorization authority; managed PostgreSQL; delivery from PR gate to promote or rollback." src="../assets/cases/athrya-architecture-dark.svg" width="100%">
</picture>


A TypeScript monorepo (npm workspaces and Turborepo) holds **6 apps and 16 shared packages**:

- **Mobile app.** One universal Expo / React Native app for iOS, Android and web, with a separate area for each role. It is the default experience for everyone.
- **API.** NestJS with Prisma on PostgreSQL. It is the single authorization authority.
- **Portal and Platform Admin.** Next.js apps for academy operations and for the SaaS operator, respectively.
- **Invite landing.** Sends invited people to the right app store or to the Portal.
- **Dashboard.** A large-screen companion to the app. It has not been deployed.

**Layering.** The domain and application packages are pure TypeScript, and a lint rule keeps UI frameworks out of them. Contracts were written from the domain outward. Screens switched from mock repositories to the real API one domain at a time.

**Multi-tenancy.** Access is modelled as *role at unit*, so one person can hold several roles across several academies. Every route is protected by default. Tenant scoping is enforced in the data layer and checked again explicitly. Platform roles and academy roles are kept separate.

**Data.** There are **129 data models and 233 migrations**. Migrations are additive and follow an expand/contract pattern. A single deployment step runs them; the API never migrates itself.

**Infrastructure.** The backend runs in managed containers on Azure, with managed PostgreSQL in a private network. Infrastructure is defined as code in Bicep, and CI deploys through keyless OIDC federation. Feature flags come from managed configuration, and logs are centralized with alerting. The web apps run on a managed hosting platform. Mobile builds and over-the-air (OTA) updates ship through Expo's services. Design tokens are generated from Figma Variables, and a test fails the build on any hard-coded colour or geometry value.

## Decisions & trade-offs

Decisions are recorded in **13 ADRs and a 22-entry decision log**. The main ones:

- **One universal app instead of three.** This gives one store presence and one release train. The cost is more careful role-based navigation.
- **NestJS over bare Express.** Its guards and providers map onto tenant isolation.
- **Prisma.** Chosen for file-based, reviewable migrations.
- **Server state in TanStack Query.** There is no global client store. Money is stored as integer cents.
- **The front end is never a security boundary.** The API re-checks everything.
- **No online payment processing in the MVP.** Billing is administrative: payment-key settings, charges and manual payment proofs. This avoided a large compliance burden. The billing modules are built and sit behind feature flags.
- **"No invented data."** Undecided business values appear as explicit *not configured* states, not plausible defaults.
- **"Merged is not homologated."** Partner integrations are merged in an inert state and are enabled only after partner certification.
- **A small environment topology** sized to a fixed monthly budget.
- **One PR gate instead of four.** Partly driven by limited CI concurrency.
- **No mandatory second human reviewer.** This is a conscious choice while there is one engineer. The gate and the independent AI review compensate.

## Engineering practices

- **A single mandatory PR gate.** It runs:
  - a dependency audit, lint, typecheck and secret scanning;
  - unit tests with coverage;
  - migrations from zero;
  - security boundary tests for cross-tenant access and role escalation;
  - integration tests against an ephemeral PostgreSQL;
  - Playwright end-to-end tests;
  - mobile dependency checks.
- **Test suite.** About **880 automated test files** across apps and packages, 406 of them in the API.
- **Release governance.** Squash merges, approval-gated production, a guard against stale release runs, an OTA compatibility gate, and a rollback decision tree for each layer.
- **Staged API deploys.** Each revision is smoke-tested and promoted, with automatic rollback.
- **Pre-launch security audit.** It produced **42 findings**, which were addressed in prioritized waves.
- **Observability.** Correlation IDs and release telemetry in every API log, and the build version is reported by each running instance.

## Results

- Went live in **October 2026** with five surfaces in production.
- The mobile app is published on the **App Store and Google Play**.
- **8 OTA updates** shipped during hypercare, all through the same gate. The automated API rollback was never needed.
- After launch, the guardian and supervised-minor flows were merged. Billing and the partner groundwork were merged behind flags that are off by default.

I do not publish usage, revenue or growth figures. When this was written, the formal review to close hypercare was still open.

## Current status

| Component | Status | Evidence type |
|---|---|---|
| Mobile app (iOS / Android) | Production | App Store and Google Play listings |
| API | Production | Deploy pipeline with staged revision and promotion |
| Portal | Production | Live host and deploy pipeline |
| Platform Admin | Production | Approval-gated deploy pipeline |
| Invite landing | Production | Deploy pipeline |
| Dashboard | In development | Repository only; not deployed |
| Academy billing | In development (built, behind feature flags) | Merged code; production enablement not verified |
| Benefits-partner integrations | In development | Merged inert; not homologated |
| Separate training-platform prototype | In development (paused) | Earlier repository; no deploy evidence |

## Lessons learned

- **An enforced gate beats conventions.** With a small team, the quality bar has to live in automation, not in memory.
- **Parallel work needs isolation and one integrator.** A "one writer at a time" rule keeps reconciliation from eating the speed gain.
- **Domain-first contracts pay off.** Combined with mock-to-API switching, they let product work run ahead of the backend without rework.
- **Merged, released and enabled are different states.** Flags let unfinished work land without being exposed.
- **Give migrations one authority.** That takes the riskiest step of a release out of the application.
- **Instrument every platform before launch.** Mobile crash telemetry was not equally complete on both platforms at launch.
- **State the bus factor openly.** A one-engineer model depends on written decisions and runbooks.

## What is intentionally not shown

- **Source code.** It is private and stays private.
- **Customer identity.** No academy, location or person is named. Screenshots will only appear once they have been re-captured on neutral data.
- **Infrastructure identifiers.** Hosts, resources, project IDs and app identifiers are all left out.
- **Security internals.** Control design, audit findings and remaining hardening work are not described beyond the level of this page.
- **Business figures.** No users, revenue, adoption or budget numbers are published.

---
<sub>Sanitized case study. The source code is private; this page shows architecture, decisions and verifiable status only. · <a href="../README.md">Back to profile</a></sub>
