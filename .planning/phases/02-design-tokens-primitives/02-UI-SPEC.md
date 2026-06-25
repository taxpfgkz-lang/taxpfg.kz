---
phase: 2
slug: design-tokens-primitives
status: approved
shadcn_initialized: false
preset: none
created: 2026-06-26
reviewed_at: 2026-06-25T21:23:43Z
master_contract: ../01-baseline-audit-ui-design-contract/01-UI-SPEC.md
---

# Phase 2 — UI Design Contract (phase-scoped slice)

> **This is NOT a new design system.** The milestone-wide design contract is
> **[01-UI-SPEC.md](../01-baseline-audit-ui-design-contract/01-UI-SPEC.md)** (status: approved).
> That document is the single source of truth for ALL tokens, scales, color/contrast,
> component states, and hard constraints binding on Phases 2–5.
>
> This file extracts the **Phase-2-relevant slice** — the tokens and scales that
> physically *land in code* this phase (TOK-01 token list, TOK-02 spacing scale,
> TOK-03 type scale, VIS-03 color/contrast) — plus the specific AUD-02 findings
> Phase 2 fixes. For anything not below, defer to the master contract. No new
> design decisions are made here; all choices are already locked in 01-UI-SPEC.md
> and 02-CONTEXT.md.

---

## Phase 2 Scope (what lands in code)

First code-touching phase. Edits **only** `css/custom.css` (and `css/base.css` only if a
`--pbmit-*` token must be surgically referenced/overridden). `js/custom.js` is **not touched**.
Establishes the token foundation everything downstream inherits:

| ID | Deliverable | File |
|----|-------------|------|
| TOK-01 | Consolidate ink+gold / radii / shadows / transitions / z-index into one `:root` `--pfg-*` list | `css/custom.css` (extends existing `:284-302`) |
| TOK-02 / VIS-02 | Declare `--pfg-space-*` 4px scale; snap section/block paddings to nearest token (point-fixes per AUD-02) | `css/custom.css` |
| TOK-03 | Declare fluid `clamp()` type scale (ratio ≈1.25) with line-height policy + Russian wrapping | `css/custom.css` (`:root`) |
| VIS-03 | Enforce contrast: gold-text only `--pfg-gold-ink`; gold-fill `#ecab23` untouched | `css/custom.css` |

Deferred (NOT this phase): component state styling (Phase 3), conversion blocks + imagery
(Phase 4), final a11y/cross-device verification (Phase 5).

---

## Design System

Inherited verbatim from [01-UI-SPEC.md › Design System](../01-baseline-audit-ui-design-contract/01-UI-SPEC.md#design-system). Unchanged this phase.

| Property | Value |
|----------|-------|
| Tool | none (no-build static site; no shadcn/registry) |
| Preset | not applicable |
| Component library | GudFin/PBMIT theme (`pbmit-*`) + Bootstrap 5.2 + project `pfg-*` primitives |
| Icon library | Font Awesome + Themify + Pbminfotech/Pbmit GudFin icon fonts (vendored, no new icons) |
| Font | Be Vietnam Pro (body, weight 400), Plus Jakarta Sans (headings + buttons, weight 600) |
| Override layer | `css/custom.css` (loaded last, wins by source-order) — the editable file this phase |

### Token Namespaces (source of truth)

| Namespace | Owner | Location | Rule |
|-----------|-------|----------|------|
| `--pbmit-*` | Vendor theme (brand values) | `css/base.css:21-49` | Source of truth; referenced via `var()`, never renamed/expanded |
| `--pfg-*` | Project premium layer | `css/custom.css:284-302` (consolidated/extended this phase) | Reuse hex from `--pbmit-*`; project-semantic names; palette NOT expanded |

---

## Spacing Scale — TOK-02 / VIS-02 (lands this phase)

Token-based 4px scale declared as `--pfg-space-*` in the `custom.css` `:root`. All multiples of 4.
**Snap-to-nearest**, not full recalculation — preserve the theme's existing visual rhythm.

| Token | Value | Usage |
|-------|-------|-------|
| `--pfg-space-1` | 4px | Icon gaps, inline hairline padding |
| `--pfg-space-2` | 8px | Compact element spacing, tight stacks |
| `--pfg-space-3` | 12px | Eyebrow gap (existing `gap:12px`), small control padding |
| `--pfg-space-4` | 16px | Default element spacing, form-field gaps |
| `--pfg-space-6` | 24px | Card padding, section inner padding |
| `--pfg-space-8` | 32px | Layout gaps, block separation |
| `--pfg-space-12` | 48px | Major section breaks |
| `--pfg-space-16` | 64px | Page-level section spacing |
| `--pfg-space-24` | 96px | Hero / large section vertical rhythm |

**Application rules (from 02-CONTEXT decisions):**
- Declare the full scale; then **point-replace** only the paddings flagged in AUD-02. Do NOT rewrite paddings that already read correctly.
- Replacement = snap existing value to nearest token, keeping the theme rhythm (not exact-scale everywhere).
- VIS-02: fix only the documented AUD-02 drift; do NOT restructure the vendor grid.

**Exceptions:**
- 44px minimum hit zone (WCAG 2.5.5) on interactive glyphs is a hit-area floor, not a spacing-scale value (`custom.css:164-170`, footer `:565-571`). Untouched this phase.

---

## Typography — TOK-03 (lands this phase)

Fluid `clamp()` scale, ratio ≈1.25 (major third), declared in the `custom.css` `:root` (NOT base.css).
Body base 16–18px (theme body = 17px, `base.css:37`). **Exactly two weights: 400 + 600.**

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Body | clamp(16px → 18px) | 400 | 1.6 (existing `--pbmit-body-typography-line-height`) |
| Label / UI | 15px (existing `--pbmit-btn-typography-font-size`) | 600 | 1.2 |
| Heading (h2–h4) | clamp(20px → ~34px), ratio 1.25 | 600 | 1.2 |
| Display (h1 / hero) | clamp(~34px → ~56px) | 600 | 1.15–1.2 |

**Claude's discretion (within locked bounds):** exact clamp() min/max per role, within ratio 1.25 and base body 16–18px.

**Wrapping & Russian-language rules (locked):**
- `text-wrap: balance` on headings; `text-wrap: pretty` on body — orphan/widow guard.
- Non-breaking handling for short Russian prepositions/conjunctions (`в`, `и`, `с`, `к`, `на`, `по`, `от`) so they never end a line.
- `text-transform: none` wherever the theme imposes `capitalize`/`uppercase` on Russian text (existing pattern `custom.css:215-218`, `:243-258`, `:865-873`).
- Markup is read-only — do NOT change heading levels; exactly one `<h1>` per page stays.

---

## Color — VIS-03 (enforced this phase)

Ink + gold palette. **Frozen — not expanded.** Brand hex reused from `--pbmit-*`; only *text*
color or *text-on-gold* is darkened for contrast, never the brand fill. Full table in master
[01-UI-SPEC.md › Color](../01-baseline-audit-ui-design-contract/01-UI-SPEC.md#color); Phase-2-binding subset:

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | `#f6f4ef` warm paper (`--pfg-paper-warm`) + `#ffffff` | Page background, surfaces |
| Secondary (30%) | `#16222d` ink (`--pfg-ink`), `#0f1820` (`--pfg-ink-deep`) | Footer, dark sections, headings |
| Accent (10%) | `#ecab23` gold (`--pfg-gold`) | CTA fill, eyebrow stroke, footer top-border, focus ring (reserved list in master) |
| Gold-as-text | `#7a560a` gold-ink (`--pfg-gold-ink`) | Gold-colored *text* on light surfaces only (AA ≥5.4:1) |

**Contrast floor (WCAG AA) — binding:**
- Body / normal text ≥ 4.5:1; large text & UI/graphics ≥ 3:1.
- Gold `#ecab23` is **forbidden as body text** on light backgrounds — use `--pfg-gold-ink` `#7a560a`. Gold fill stays `#ecab23`; only text color changes.
- AUD-01 baseline = **0 axe contrast violations**; this phase must not introduce any. No new contrast gap to close — VIS-03 is enforcement, not redesign.

**Destructive:** none exist on this site. Not applicable this phase.

---

## AUD-02 Findings Phase 2 Fixes

These are the specific, DOM-measured visual problems this phase lands (verify by DOM measurement, not CSS text):

| Finding | Problem | Phase-2 fix |
|---------|---------|-------------|
| HE1 / T2 / G2 | Heading line-height < font-size (hero 170/150px) | Normalize via `clamp()` type scale + line-height policy (TOK-03) |
| C1 | Card padding 28px (off-scale) | Snap to `--pfg-space-6`/`-8` (TOK-02) |
| F1 | Mobile input font-size 15px → iOS focus-zoom | Raise to ≥16px on mobile via scale/token (TOK-03) |
| P2 (partial) | Title-bar 550px persisting at 768px tablet | Partially spacing — review under TOK-02; do not restructure vendor grid |

---

## Copywriting Contract

No copy changes this phase (Phase 2 is a pure CSS token layer; markup/strings read-only).
Full string contract in master [01-UI-SPEC.md › Copywriting Contract](../01-baseline-audit-ui-design-contract/01-UI-SPEC.md#copywriting-contract). Strings stay byte-identical (VER-04).

| Element | Status |
|---------|--------|
| All site CTAs, labels, form states | Unchanged — styled by carriers only, never edited |
| Empty / destructive states | Not applicable (static marketing site, no data/destructive actions) |

---

## Hard Constraints (binding — full list in master)

Phase-2-critical guardrails (full table: [01-UI-SPEC.md › Hard Constraints](../01-baseline-audit-ui-design-contract/01-UI-SPEC.md#hard-constraints-binding-on-phases-25)):

| Constraint | Phase-2 rule |
|------------|--------------|
| visual-only | CSS tokens/scales only; no logic/form-flow/JSON-LD behavior change |
| vendor read-only | Edit only `css/custom.css` (and `base.css` only to reference/override `--pbmit-*`); `js/custom.js` NOT touched this phase |
| no `@layer` | FORBIDDEN — unlayered vendor beats layered. Win by source-order + targeted specificity |
| token discipline | One consolidated `:root` `--pfg-*` list; reuse `--pbmit-*` via `var()`; palette NOT expanded |
| `!important` budget | Net-new ≈ 0 (floor = 57 functional declarations, 01-CONFLICT-CATALOG). Each new one cites the beaten vendor rule in a Russian comment. 31/57 uncited — confirm actual beaten selector before relocate/drop |
| scoped-motion | Any new decorative motion goes in scoped `prefers-reduced-motion` block (`custom.css:332-345`); brand motion (Swiper/marquee/GSAP/AOS) untouched |
| off-canvas-safe | No `filter`/`backdrop-filter`/`transform` on ancestors of mobile off-canvas menu; glass-header gated `min-width:1201px` |
| load-order | `custom.css` stays the LAST stylesheet |
| comments-russian | New comments Russian, dense, justify *why* (vendor behavior, measured contrast, WCAG criterion) |

---

## Verification Channel (durable)

- Playwright DOM-measured @ 1440 / 1024 / 768 / 390 / 360 + axe against AUD-01 floor (a11y ≥95, axe contrast = 0). **Trust DOM measurement, not CSS text.**
- JS smoke (VER-04): menu / WhatsApp float / lead-form→WhatsApp / marquee / slider / reduced-motion must stay behavior-identical (no JS edits this phase).

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS — no copy change; strings byte-identical (VER-04)
- [ ] Dimension 2 Visuals: PASS — AUD-02 findings (HE1/T2/G2, C1, F1, P2) mapped to fixes
- [ ] Dimension 3 Color: PASS — ink+gold frozen, VIS-03 contrast floor enforced, 0 axe violations
- [ ] Dimension 4 Typography: PASS — fluid clamp() ratio 1.25, two-weight policy, Russian wrapping
- [ ] Dimension 5 Spacing: PASS — `--pfg-space-*` 4px scale, snap-to-nearest, 44px hit-zone exception
- [ ] Dimension 6 Registry Safety: PASS — no registry, vendored read-only stack

**Approval:** pending

**Source-of-truth note:** This is a phase-scoped slice. Where this document and
[01-UI-SPEC.md](../01-baseline-audit-ui-design-contract/01-UI-SPEC.md) appear to differ, the
master contract governs. No locked decision from 01-UI-SPEC.md or 02-CONTEXT.md is weakened here.
