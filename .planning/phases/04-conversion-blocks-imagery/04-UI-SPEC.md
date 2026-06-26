---
phase: 4
slug: conversion-blocks-imagery
status: approved
shadcn_initialized: false
preset: none
created: 2026-06-27
reviewed_at: 2026-06-26T23:51:38Z
master_contract: ../01-baseline-audit-ui-design-contract/01-UI-SPEC.md
---

# Phase 4 — UI Design Contract (phase-scoped slice)

> **Phase-scoped contract.** This document does NOT redefine the design system.
> The single source of truth is the **master contract**, approved in Phase 1:
> [`01-UI-SPEC.md`](../01-baseline-audit-ui-design-contract/01-UI-SPEC.md) (status: approved 2026-06-25).
>
> Tokens, spacing scale, type scale, color palette + contrast floor, component-state
> contract, and Hard Constraints all live in the master and are **inherited unchanged**.
> This slice only extracts what Phase 4 implements (CNV-01..04, IMG-01) and the
> phase-specific decisions locked in
> [`04-CONTEXT.md`](./04-CONTEXT.md). Where this file is silent, the master governs.

---

## Inheritance — do not re-specify

These are LOCKED by the master contract. Phase 4 composes from them, never re-invents:

| Concern | Inherited from master | Phase-4 rule |
|---------|----------------------|--------------|
| Spacing | `--pfg-space-*` 4px scale (master §Spacing) | Pricing/hero/footer styled with tokens; no hardcoded px |
| Typography | fluid `clamp()` scale, ratio 1.25, 2 weights (400/600), Russian wrapping (master §Typography) | Tier names/prices/CTA use scale; `text-transform:none` on Russian |
| Color | ink+gold palette frozen; gold `#ecab23` accent (master §Color) | Gold reserved-for list **already includes** "single популярный pricing-tier highlight" |
| Components | `.pbmit-btn` (4 states + primary/secondary/ghost), `.pfg-card`, `.pfg-form`, `.pfg-faq` — verified in [03-VERIFICATION.md](../03-components/03-VERIFICATION.md) (18/18) | Pricing block is a **composite** of these; not net component primitives |
| Component states | hover/focus-visible/active/disabled; gold focus ring `outline:2px solid var(--pfg-gold)` (master §Component State Contract) | Per-tier CTA + tier card inherit these states |
| Hard constraints | vendor read-only, no `@layer`, scoped-motion, load-order, off-canvas-safe, change-all-11, `!important` floor 59, comments-russian, VER-04 behavior-identity (master §Hard Constraints) | All binding on this phase — see §Phase-4 Hard-Constraint Deltas |

---

## Phase-4 Scope Slice

### CNV-01 — Hero polish (existing block, NOT a redesign)

Polish the existing index slider (`.pbmit-slider-one .pbmit-slider-title`, 3 slides) — do not rebuild it.

| Aspect | Contract |
|--------|----------|
| Value-prop | Keep the existing slide headlines (Russian, byte-identical — VER-04); ensure value-prop reads above the fold |
| Primary CTA | **Exactly one** primary CTA in the hero — «Получить консультацию» (gold-fill `.pbmit-btn`). No competing primary CTA above the fold |
| Trust signals | Surface existing trust content (from current page copy — see Claude's Discretion) above the fold; do not invent new copy |
| HE1 / G2 line-height | Heading `line-height ≥ font-size` (lh ≥ 1.0). Fixes the desktop 170px fs / 150px lh clip. Already partly handled by the Phase-2 lh policy (`custom.css:523-527`) — confirm lh ≥ fs holds at 1440/1024 |
| HE2 height/LCP | Hero height is a **visual** note only. Perf (LCP/CLS) is **not a regression gate** this milestone — do not chase perf, just don't make height worse |
| Motion | Hero Swiper/GSAP appearance animation is **brand motion** — leave the reduced-motion floor intact, do NOT add it to the scoped killer |

### CNV-02 — Pricing block (NET-NEW, build in full)

Zero `pricing`/`тариф`/`price-table` markup exists today (confirmed master Open-Q + 01-IMPL). Build it completely — no "v1/placeholder/static-for-now" framing.

| Aspect | Contract |
|--------|----------|
| Location | **services.html only** — after hero/services, before the existing `.pfg-faq` FAQ. Page-specific → **NOT shared chrome → NOT change-all-11** |
| Structure | Exactly **3 tiers** (e.g. ИП-старт / ТОО-стандарт / Премиум — names at Claude's discretion, Russian sentence case, meaningful for accounting/tax services) |
| Highlight | **Exactly one** "популярный" tier highlighted with the **gold accent** — this is the sanctioned use from the master accent reserved-for list (master §Color). The other two tiers carry no gold fill. One highlight, never two |
| Price content | **No exact figures.** Use scope-of-service wording + «от X ₸» or «по запросу» → CTA. (Business has not confirmed tariffs; exact prices deferred to v2 per 04-CONTEXT deferred.) |
| Per-tier CTA | Each tier has its own CTA → routes through the **existing** WhatsApp flow (`initLeadForm` / `wa.me/77072370050` pattern, `js/custom.js:72-111`). **Reuse the existing mechanism — NOT new logic** (VER-04). No JS edit required |
| Composition | Compose from Phase-3 primitives: tier card = `.pfg-card` variant, CTA = `.pbmit-btn` (primary on highlight tier, secondary/ghost on others per master button hierarchy), spacing/type via Phase-2 tokens. **No hardcoded hex/px** |
| Card equal-height | Same-row tiers visually equal-height (inherit `.pfg-card{height:100%}` + grid `align-items:stretch`, master C2 pattern) |
| Hover motion | Tier-card hover lift is **decorative** → add to the scoped `prefers-reduced-motion` block (`custom.css:~378-389`), never universal |
| CTA hierarchy | One prominent primary per screen — the highlight-tier CTA is primary; sibling tier CTAs step down (secondary/ghost) so the screen keeps a single dominant action |

### CNV-03 — CTA hierarchy + sticky/floating (resolution by documented absence)

**There is NO sticky mobile CTA on the site** (grep-confirmed, 04-CONTEXT). The collision the original plan anticipated (sticky-CTA ↔ `.pfg-whatsapp-float`) **physically does not exist.**

| Aspect | Contract |
|--------|----------|
| Sticky CTA | **Do NOT create** a net-new sticky mobile CTA. CNV-03 is satisfied by documenting the absence of conflict, honestly — not by building then resolving a fabricated collision |
| Floating element | `.pfg-whatsapp-float` (`css/custom.css:24-40`, init `js/custom.js:58-60`) is the **only** floating/sticky element. It overlaps nothing. Record this as the resolution |
| JS | **No `js/custom.js` edit in this phase.** CNV-03 was the sole JS candidate; with no sticky-CTA, the JS stays byte-identical (VER-04). The 01-IMPL "JS spike" line is superseded by this documented-absence finding |
| Site-wide hierarchy | One prominent primary CTA per screen, expressed through Phase-2 tokens + Phase-3 button hierarchy — not a new component |

### CNV-04 — Footer parity (shared chrome → change-all-11)

| Aspect | Contract |
|--------|----------|
| Parity | Footer appearance unified across **11/11** pages (`.site-footer` present on all 11). Gold 3px top-border is already correct everywhere (FT2 positive) — preserve it |
| FT3 | Footer is tall on mobile when columns stack (1732px @390). **Low-priority** vertical-density review — tighten stacked-column spacing via tokens; not a defect, do not over-engineer |
| change-all-11 | If footer **markup** is touched, edit all 11 HTML files atomically in one commit (grep must return 11). CSS-only footer polish does not require markup edits |
| FT1/F2 | Footer-link and consent 44px tap-zones were root-cause fixed in Phase 3 — **do not regress** them |

### IMG-01 — Imagery sizing (presentation only)

| Aspect | Contract |
|--------|----------|
| Scope | **Presentation/sizing ONLY** — `object-fit`, correct proportions, no distortion/visual junk — on the existing 12 `<img>` + CSS backgrounds. Exact `object-fit`/sizing values at Claude's discretion |
| I1 | `about-01.jpg` serves a 900×1000 asset into a ~300px box. Aspect ratio is already preserved (no distortion) → sizing/box note only. **Bulk WebP/AVIF/srcset re-encode = v2/PERF-01, OUT OF SCOPE** — do not re-encode |
| I2 | `about-02.png` / `infobox-img.png` already render at sensible sizes (positive finding) — leave unless a distortion surfaces |

### T1 — Title-bar min-height tier

| Aspect | Contract |
|--------|----------|
| Fix | `.pbmit-title-bar-wrapper` is a fixed 550px band down to 768 (disproportionate for a one-line heading on tablet). Add a **smaller min-height tier between 768 and 390** so the band shrinks on tablet. CSS-only, token-driven, must not regress the ≥390 collapse already in place (`custom.css:991+`) |

---

## Phase-4 Hard-Constraint Deltas

All master Hard Constraints apply. Phase-specific emphasis:

- **JS untouched** — `js/custom.js` is **not edited** this phase (CNV-03 resolved by documented absence). Expect `git diff HEAD js/custom.js` empty (VER-04).
- **`!important` budget** — floor is **59** (master + 03-VERIFICATION confirmed 59). Net-new ≈ 0; each new one (if unavoidable) cites the beaten vendor rule in a **Russian** comment.
- **Pricing is page-specific** — services.html only; do NOT propagate to the other 10 pages.
- **Footer is shared chrome** — markup edits are change-all-11 (grep = 11), one atomic commit.
- **WhatsApp flow reuse** — per-tier pricing CTA uses the existing `wa.me/77072370050` + `encodeURIComponent` flow; behavior byte-identical (VER-04). No new logic, no new number.
- **off-canvas-safe / no `@layer` / load-order** — unchanged from master.

---

## Copywriting Contract (phase-scoped additions)

Site copy is read-only (VER-04). Phase 4 introduces **net-new** pricing strings only (no existing copy is rewritten).

| Element | Copy |
|---------|------|
| Hero primary CTA | «Получить консультацию» (existing, byte-identical) |
| Pricing eyebrow | Russian sentence case, e.g. «Тарифы» / «Пакеты услуг» (Claude's discretion) |
| Pricing tier names | 3 names, Russian sentence case, meaningful for accounting/tax (Claude's discretion) |
| Pricing price line | «от X ₸» or «по запросу» — **no exact figures** |
| Pricing per-tier CTA | «Получить консультацию» (or close variant) → existing WhatsApp flow |
| Highlight label | One tier marked «популярный» (or close) — exactly one |

All net-new pricing copy is Russian sentence case; existing strings (CTA, form, consent, JSON-LD) stay byte-identical.

---

## Registry Safety

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none — no shadcn/registry; vendored theme + Bootstrap only (inherited from master) | not applicable |

No third-party registries. No remote component fetching. Inherited unchanged from master §Registry Safety.

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS — net-new pricing strings Russian sentence case; existing copy byte-identical (VER-04)
- [ ] Dimension 2 Visuals: PASS — CNV-01..04 + IMG-01 + T1 mapped to AUD findings; pricing composes Phase-3 primitives
- [ ] Dimension 3 Color: PASS — gold accent on single pricing highlight is the sanctioned master reserved-for use; palette frozen
- [ ] Dimension 4 Typography: PASS — inherits master clamp() scale; hero lh ≥ fs (HE1/G2)
- [ ] Dimension 5 Spacing: PASS — pricing/footer/title-bar use `--pfg-space-*` tokens; no hardcoded px
- [ ] Dimension 6 Registry Safety: PASS — no registry, inherited from master

**Approval:** pending
