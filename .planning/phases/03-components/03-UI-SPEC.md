---
phase: 3
slug: components
status: draft
shadcn_initialized: false
preset: none
created: 2026-06-26
master_contract: ../01-baseline-audit-ui-design-contract/01-UI-SPEC.md
---

# Phase 3 — UI Design Contract (Components)

> **Phase-scoped slice. The master contract is the source of truth.**
> Tokens, spacing scale, type scale, color+contrast floor, copywriting strings, and Hard
> Constraints are **already approved** in
> [`01-UI-SPEC.md`](../01-baseline-audit-ui-design-contract/01-UI-SPEC.md) (the master).
> This document does **not** redefine them — it extracts the Phase-3-relevant component-state
> slice (CMP-01..06 + VIS-01) and pins the net-new FAQ spec and the two a11y tap-target fixes.
> When a value is not restated here, the master governs.

**Inherits from Phase 2** (`02-VERIFICATION.md`, all 5/5 verified): components are styled with
the landed tokens (`--pfg-space-*`, `--pfg-fs-*`/`--pfg-lh-*`, `--pfg-z-float`, ink+gold palette,
shadows `--pfg-shadow-btn`/`-btn-h`, radii, `--pfg-tf-fast`/`--pfg-tf`) — **never hardcoded values**.
F1 (input 16px) and C1 (card padding 24px) already landed in Phase 2; do not redo them.

---

## Design System

Unchanged from master. No new tooling, no registry, no shadcn — vendored GudFin/PBMIT theme +
Bootstrap 5.2 + `pfg-*` override layer; `css/custom.css` (last stylesheet) and `js/custom.js`
(last script) are the only editable code files this phase, plus **HTML markup** (scope expanded
by Юрий 2026-06-26 — vendor JS/CSS files stay read-only). See master "Design System" table.

| Property | Value |
|----------|-------|
| Tool | none (no-build static site; not applicable) |
| Component library | GudFin/PBMIT theme (`pbmit-*`) + Bootstrap 5.2 + project `pfg-*` primitives |
| Editable this phase | `css/custom.css` (primary), `js/custom.js` (a11y/ARIA layer only), `*.html` markup |

---

## Component State Contract — Phase 3 slice

Reproduces the master "Component State Contract" rows that this phase implements. **All
interactive elements declare hover / focus-visible / active / disabled.** Focus is always
visible — reference ring `outline: 2px solid var(--pfg-gold); outline-offset: 3px`
(`custom.css:351-358`, already present). No bare `outline:none` (A11Y-01).

| ID | Component | Hook (do NOT rename) | Required states | Phase-3 implementation notes |
|----|-----------|----------------------|-----------------|------------------------------|
| **CMP-01** | Buttons | `.pbmit-btn` (override via cascade) | primary / secondary / ghost × hover / focus-visible / active / disabled | **Primary** = gold fill `#ecab23` + ink text holding AA, shadow `--pfg-shadow-btn` → hover `--pfg-shadow-btn-h` + `--pfg-gold-deep` (text `#1b1b1b` holds AA). **Secondary** = outline/ink (e.g. `.pbmit-btn white` on dark sections). **Ghost** = text-weight, minimal chrome, `--pfg-gold-ink` on hover. Disabled = reduced-opacity + `cursor:not-allowed`, no shadow. Keep `text-transform:none` (Russian, `custom.css:256-264`). |
| **CMP-02** | Forms / inputs | `.pfg-form .form-control`, `.pfg-form-status` | rest / focus / error / success | Soft gold focus-ring already at `custom.css:572-576` (`box-shadow 0 0 0 3px rgba(236,171,35,.18)`). Error/success surfaced via `.pfg-form-status.is-error` (`#d33`) / `.is-ok` (`#1a9e57`) — text + message, never color-only (master "Destructive"). **Form→WhatsApp behavior byte-identical (VER-04)** — `js/custom.js` validation/flow untouched. |
| **CMP-03** | Service cards | `.pfg-card` / service-box | rest / hover (lift) | Hover-lift is **decorative** → goes in the scoped `prefers-reduced-motion` block (`custom.css:332-345`), never a universal killer. Resolve **C2 height-jitter** (283px@1024 vs 256px@768): equalize via consistent min-height / flex so adjacent cards in a row align. Padding already token-snapped (24px, Phase 2). |
| **CMP-04** | Nav (sticky header + off-canvas) | `#site-navigation`, theme menu | rest / hover (underline-grow) / active / focus-visible | Desktop horizontal nav + glass-header effects gated **`min-width:1201px`** (N1: 1025–1200px gets the burger). Underline-grow is **decorative motion** → reduced-motion block. **Off-canvas-safe: no `filter`/`backdrop-filter`/`transform` on ancestors of the mobile off-canvas menu** (collapses `height:100%`, `custom.css:382-390`). N1/N2 tap targets already healthy (≥44px) — document the ≥1201 scope, no fix. Theme menu JS not broken. |
| **CMP-05** | FAQ accordion | `.accordion` (net-new markup) | collapsed / expanded / focus | **NET-NEW — built in full.** See dedicated spec below. |
| **CMP-06** | Modals (Magnific Popup) | — | — | **DESCOPED.** See descope note below. |

---

## CMP-05 — FAQ Accordion (NET-NEW, full build)

The theme handler exists (`js/scripts.js:309`) but **no page instantiates it**. Build it
completely — no "placeholder / static-for-now" framing.

**Placement:** `services.html` (questions about services) and `contacts.html` (before the lead
form). FAQ is **not shared chrome** — content differs per page, so it is a single shared *style*
without a change-all-11 content edit. Question count/wording is Claude's Discretion (reasonable
minimum for the services on each page).

**Markup (Claude's Discretion on exact skeleton — pick best a11y + theme-handler compatibility):**
- Either semantic `<details>/<summary>` or `button[aria-expanded] + region[role]` — choose by
  best accessibility and compatibility with the existing theme `.accordion` handler.
- Each item: a trigger (the question) and a collapsible panel (the answer).
- Russian copy, correct sentence casing; `text-transform:none` if the theme imposes a transform.

**States (required):**
- **collapsed** — panel hidden, trigger shows closed affordance (chevron/+ via existing icon font, `aria-hidden` on the decorative glyph).
- **expanded** — panel visible, trigger reflects open state.
- **focus** — `:focus-visible` ring per the reference ring (gold, offset 3px). Hover may add a subtle gold-ink/underline cue.

**ARIA + keyboard (a11y layer in `js/custom.js`, layered over the theme handler):**
- `aria-expanded` toggles true/false on the trigger; panel `id` referenced by trigger
  (`aria-controls`); panel hidden when collapsed (`hidden`/`aria-hidden` consistent with chosen markup).
- Keyboard: Enter/Space toggles; native semantics preferred if `<details>` is used. If
  button-based, ensure roving/standard focus order works.
- Follow the existing `initX()` pattern: file-scoped IIFE, `DOMContentLoaded`, **guard +
  early-return** when no `.accordion` on the page, **idempotent** patches (check before writing,
  like `initSvgAria`/`initSearchA11y`). Layer **over** the theme handler — do not duplicate or
  fight its open/close.

**Tokens:** spacing via `--pfg-space-*`, type via `--pfg-fs-*`/`--pfg-lh-*`, borders via
`--pfg-hairline`/`-2`, radius `--pfg-radius`/`-sm`, motion via `--pfg-tf`/`-fast` with any
expand/collapse decorative transition added to the reduced-motion block.

---

## CMP-06 — Modals — DESCOPED (honest)

Magnific Popup is loaded on all 11 pages but **zero markup triggers it**
(`.pbmin-lightbox-video` / `a.pbmit-lightbox` = 0 occurrences, confirmed AUD-02 "Absent
features"). The master gates modal rules to "**only if Magnific Popup is actually
instantiated**" — it is not. **No modal markup, CSS, or focus-trap is fabricated this phase.**
If a modal is instantiated in a future milestone, CMP-06 becomes a separate task.

---

## VIS-01 — Single Visual Language

Bring heading / subheading / CTA / blocks / cards to **one visual language across all 11 pages**
using the Phase-2 token layer — no per-page divergence in component appearance. The eyebrow
"ledger stroke" gold mark, button hierarchy, card treatment, and focus ring read identically
site-wide. This is enforcement/consistency, not new tokens; the palette stays **frozen** (master
"Color"), gold reserved-for list unchanged.

---

## a11y Tap-Target Fixes (AUD-02 P1) — Phase 3 lands

CSS-only where it reaches (these are padding/min-height hit-zone fixes); markup only if CSS
cannot reach. WCAG 2.5.5 = 44×44px floor.

| ID | Finding (DOM-measured) | Target | Approach |
|----|------------------------|--------|----------|
| **FT1** | Footer menu links **26px tall** (`.site-footer a`, 15 links @390/360). The documented 44px rule (`custom.css:565-571`) **does not apply to this link group** — DOM-vs-CSS discrepancy. | ≥44px hit zone | Diagnose why the existing selector misses this group (selector reach vs override), then fix the hit-zone via CSS `padding`/`min-height` on the footer nav-links. **Footer = shared chrome → if markup is touched, change-all-11 atomically (grep returns 11), one commit.** Trust DOM measurement, not CSS source text. |
| **F2** | Consent label hit area **36px tall** (`label.pfg-consent`, 330×36px @390/360). Checkbox 18×18px; label widens horizontally but height < floor. | ≥44px hit area | Raise hit-area to ≥44px via CSS `padding`/`min-height` on `.pfg-consent label` (existing rules at `custom.css:43`, `:87`, `:648`). CSS-only — markup not required. |

**Accepted standing exception (NOT work):** mobile header search target-size (H2) — theme-owned,
measured 44×44px, maps to WCAG 2.2 SC 2.5.8 (outside scanned tag set). Do not schedule.

---

## Hard Constraints (inherited from master — binding)

Full table in master "Hard Constraints". Phase-3-critical reminders:

- **vendor read-only** — edit only `css/custom.css`, `css/base.css`, `js/custom.js` (+ HTML markup, scope-expanded). Never rename/remove `swiper-*`, `data-aos*`, `pbmit-*` hooks; vendor JS/CSS files untouched.
- **VER-04 behavior-identity** — form→WhatsApp (same number `77072370050` + message), menu, marquee, slider, reduced-motion all byte/behavior-identical.
- **change-all-11** — any shared-chrome markup edit (header/footer/nav) applies to all 11 HTML in one atomic commit (grep returns 11). FAQ content is *not* shared.
- **`!important` budget** — net-new ≈ **0** (floor **59**); each new one cites the beaten vendor rule in a Russian comment.
- **no `@layer`** — win by source-order + targeted specificity only.
- **scoped-motion** — new decorative motion (card lift, nav underline-grow, FAQ expand) goes in the scoped `prefers-reduced-motion` block (`custom.css:332-345`); brand motion (Swiper/marquee/GSAP/AOS) floor intact — never a universal `*` killer.
- **off-canvas-safe** — no `filter`/`backdrop-filter`/`transform` on off-canvas-menu ancestors; glass-header effects gated `min-width:1201px`.
- **load-order** — `custom.css` last stylesheet, `custom.js` last script.
- **comments-russian** — new CSS/JS comments in Russian, dense, justify *why* (vendor behavior, measured contrast, WCAG criterion).

**Verify (per-phase gate):** Playwright DOM-measured @ 1440/1024/768/390/360 (no horizontal
scroll, ≥44px targets, headings not clipped) + axe = 0 + Lighthouse a11y ≥ 95 (AUD-01 floor) +
VER-04 JS smoke. Trust the rendered box, not `custom.css` source text.

---

## Color / Typography / Spacing / Copywriting

**Unchanged — governed by master.** Components consume the frozen ink+gold palette, the fluid
`clamp()` type scale (ratio 1.25, two weights 400/600), the 4px `--pfg-space-*` scale, and the
byte-identical Russian copy strings recorded in the master "Copywriting Contract". This phase
adds **no new tokens, no palette expansion, no copy rewrites** — it styles the carriers. New FAQ
question/answer copy is the only net-new Russian text (CMP-05, Claude's Discretion).

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none — vendored theme + Bootstrap only; no remote fetching | not applicable |

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS — master strings byte-identical; FAQ copy is net-new Russian (CMP-05).
- [ ] Dimension 2 Visuals: PASS — CMP-01..04 states + CMP-05 net-new + CMP-06 descope + VIS-01 single language.
- [ ] Dimension 3 Color: PASS — inherits frozen ink+gold palette; no expansion.
- [ ] Dimension 4 Typography: PASS — inherits Phase-2 clamp scale, two weights.
- [ ] Dimension 5 Spacing: PASS — inherits `--pfg-space-*`; 44px hit-zone fixes FT1/F2.
- [ ] Dimension 6 Registry Safety: PASS — no registry, vendored read-only.

**Approval:** pending
