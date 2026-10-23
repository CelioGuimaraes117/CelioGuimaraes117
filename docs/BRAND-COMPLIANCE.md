# Brand compliance — Brand System v1.1

Source of truth: *Identidade Visual Célio Crisólogo — Brand System v1.1*, Brand Board v1.1 and
`brand-tokens.json` from the Brand Kit. This page records how the profile applies them and where a
judgment call was made.

## Logo

| Rule | Application |
|---|---|
| Use the original symbol; never redraw or distort | The glasses symbol is the official path data from `03-Logos/01-Symbol/SVG`, embedded verbatim with uniform scaling (automated test asserts the path is byte-identical). |
| Clear space = chevron height; minimum A1 ≥ 24 px | Hero symbol renders at ~85 px tall at native size; ≥ 19 px on a 360 px phone. |
| Official signatures only | Signature 2 — *Célio Crisólogo / Software Architecture / Backend / Applied AI* — in the hero and footer. |
| Wordmark: Inter 600, tracking −0.035 em | Rendered from Inter 600 with the same tracking as the official lockup SVGs. |

The Kit's lockups use live `<text>` elements. GitHub serves README images through a proxy where web
fonts cannot load, so those files would fall back to Arial/Helvetica. The profile therefore renders the
**same specification** (font, weight, size ratio, tracking, colors) as vector outlines. Nothing about the
logo is altered.

## Color

| Role | Token | Where |
|---|---|---|
| Dark builds | Tech Black `#080B12`, Surface 01 `#111722` | Hero base, cards |
| Royal identifies | Royal `#014BAE` | Level 2 hero field (≈58%), card rules, eyebrow rules. Never body text, never chart data. |
| Gold signs | Gold `#C8A35F` (dark) / Vintage Gold `#A5803F` (light) | Eyebrow numbers and KPI numbers on dark; on light, gold is used only for rules and slashes — numbers fall back to Tech Black (*gold never on white*). |
| White informs | White `#F5F7FA`, Secondary `#8C97A8` | Text |
| Technical palette = information only | system `#4CC9F0`, link `#6F9BFF`, success `#5BD6A0`, ai `#A78BFA`, human `#FFA94D` (`-deep` variants on light) | Charts and the hero's system sketch only. |

Contrast (WCAG AA, ≥ 4.5:1) is asserted in automated tests for every text color against its card,
the brand background and GitHub's own backgrounds (`#0d1117`, `#ffffff`). White on Royal: 8.2:1.

## Typography

Inter (explains) and IBM Plex Mono (names: eyebrows, labels, numbers on axes). No other family.

## Graphic system

- One macro-diagonal per composition: the 8° slash that closes the Royal field in the hero.
- Eyebrow pattern `NN —— LABEL` (gold number, Royal rule, mono label) on every section.
- Level 2 opens (hero), Level 1 sustains (all sections and cards).
- No gradients, glows, glassmorphism or animation.

## Decisions

- **`Fundo Tech com Código e Arquitetura IA.png` was not used.** It already contains the logo and
  signature, is 16:9 (a banner needs ~4:1) and relies on orange/blue glows the system asks to avoid. The
  hero keeps its idea — code, layered architecture — as a restrained technical-palette sketch.
- **Stack as code spans, not icon badges.** One consistent element instead of dozens of third-party
  logos with uneven styles and licenses; it also reflows on mobile.
- **Light theme** variants exist for every image and are selected with `<picture>` +
  `prefers-color-scheme`.
