# Profile architecture

```
Azure DevOps (source of truth, private)        GitHub
  includlab/* ──┐                                ┌── CelioGuimaraes117/<mirror> (PRIVATE, fast-forward only)
                │   private repository           │
                ├── celio-engineering-activity ──┤
GitHub API ─────┘   (collector, mirror,          └── CelioGuimaraes117/CelioGuimaraes117 (PUBLIC, this repo)
                     renderer, tests)                  receives: assets/**/*.svg + data/public-metrics.json
```

## Two repositories, two trust levels

| | `CelioGuimaraes117` (this repo) | `celio-engineering-activity` |
|---|---|---|
| Visibility | Public | Private |
| Holds | README, rendered SVGs, aggregate JSON, validator | Collector, mirror, renderer, tests, configuration, private reports |
| Secrets | None | Azure DevOps and GitHub tokens (Actions secrets) |
| Workflow permissions | `contents: read` | Least privilege per job |

The public repository never runs code with access to private data. It only receives files that were
generated and validated on the private side.

## Data flow

1. **Collect** (private): official APIs only; pagination, retries with backoff, `Retry-After` and GitHub
   rate-limit headers, timeouts, UTC normalization.
2. **Deduplicate**: commits are keyed by SHA. A commit present on GitHub and Azure DevOps counts once.
3. **Split**: a private report (per repository) and a public report built field by field from an explicit
   schema. A validator rejects any unexpected key, string or value before anything is written.
4. **Render**: SVG components with text outlined from the brand fonts. Input from APIs never becomes
   markup — numbers are formatted, names pass an allowlist regex and become glyph outlines.
5. **Publish**: only changed files are committed; no empty commits.

## Rendering on GitHub

- SVGs are served through GitHub's image proxy: no scripts, no external references, no web fonts.
- `<picture>` with `prefers-color-scheme` selects dark or light variants.
- Section headers render at a fixed width (520 px) so they stay legible on phones; data cards scale
  to the column, and every chart has a text description (`<desc>` + `alt`).
