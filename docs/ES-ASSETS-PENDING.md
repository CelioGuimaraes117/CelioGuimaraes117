# Spanish assets pending

`README.es.md` and `cases/*.es.md` currently reuse the **English** images (closest to the market
practice for Latin American recruiters). Every `alt` text is in Spanish and says the text inside the
image is in English. No `-es-` image was created, on purpose.

## Why nothing was drawn by hand

Every SVG under `assets/` has **no `<text>` elements**: all lettering is vector outlines produced by
the private renderer (`celio-engineering-activity`, see `PROFILE-ARCHITECTURE.md`). A Spanish variant
cannot be made by editing text, and a hand-drawn copy would drift from the brand specification and be
overwritten by the next metrics run. The PNG screenshots (`athrya-demo`, `ai-assist-evidence`) are
raster captures of localized builds and need new captures, not edits.

## Needed from the collector / renderer front

Naming convention (same as Portuguese): `<name>-es-dark.<ext>` and `<name>-es-light.<ext>`, same
dimensions, text described in `<title>` and `<desc>` in Spanish, with the **same numbers** as the
English file.

| Asset (dark and light) | Used in | Kind |
|---|---|---|
| `assets/banners/hero-animated` (and static `hero`) | README.es.md | hero, generated |
| `assets/cases/athrya-architecture` | README.es.md, cases/athrya.es.md | diagram, generated |
| `assets/cases/ai-assist-architecture` | README.es.md, cases/ai-assist.es.md | diagram, generated |
| `assets/cases/ai-assist-flow` | cases/ai-assist.es.md | diagram, generated |
| `assets/cases/engineering-platform` | README.es.md, cases/engineering-platform.es.md | diagram, generated |
| `assets/metrics/v2/031-activity`, `032-monthly`, `033-sources`, `034-delivery`, `035-contributions` | README.es.md | dashboards from the metrics workflow |
| `assets/cases/athrya-demo`, `assets/cases/ai-assist-evidence` | cases/athrya.es.md, cases/ai-assist.es.md | PNG screenshots, new captures |

Not referenced by any README today (no Spanish variant needed): `assets/sections/*`,
`assets/metrics/*.svg` (v1) and `assets/brand/signature-*` (the signature is language-neutral).

## When variants land

1. Add the files; swap the `srcset`/`src` in `README.es.md` and `cases/*.es.md` to the `-es-` names.
2. `scripts/validate_profile.py` already fails if a Spanish page keeps using an English image while an
   `-es-` variant exists, so a forgotten swap is caught.
3. Extend the dashboard parity rule (`check_i18n`, `<desc>` numbers) to the `-es-` files.

## Other pending item

The site `https://www.celiocrisologo.com.br/es` answers 404 (checked on 14 Nov 2026), so the Spanish
README links the English portfolio page. Switch to `/es` when it exists.
