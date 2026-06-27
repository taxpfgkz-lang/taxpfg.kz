---
phase: 04-conversion-blocks-imagery
plan: 01
subsystem: conversion-blocks
tags: [pricing, cnv-02, services, whatsapp-cta, premium-layer]
requires:
  - "Phase-3 primitives: .pfg-card, .pfg-grid, .pbmit-btn"
  - "Phase-2 tokens: --pfg-* (space/fs/gold/ink/radius/shadow)"
provides:
  - "services.html pricing block (3 tiers, 1 gold highlight)"
  - ".pfg-pricing-* CSS rules (token-composed)"
affects:
  - services.html
  - css/custom.css
tech-stack:
  added: []
  patterns:
    - "direct-link WhatsApp CTA (wa.me) per tier — no form, no JS"
    - "gold highlight via border+badge, never full fill (AA body)"
key-files:
  created: []
  modified:
    - services.html
    - css/custom.css
decisions:
  - "Highlight = ТОО на общем режиме (middle tier) as the single popular gold accent"
  - "Prices kept indicative («от … ₸ / мес», «по запросу») — exact figures deferred to v2 (D CNV-02)"
  - "No net-new !important — pricing rules win by specificity (count stays 59)"
metrics:
  duration: "~20 min"
  completed: 2026-06-27
  tasks: 2
  files: 2
status: complete
---

# Phase 4 Plan 01: CNV-02 Pricing Block Summary

Net-new pricing block on services.html: three accounting-support tiers (ИП на упрощёнке / ТОО на общем режиме / Премиум) with exactly one gold «Популярный» highlight and a per-tier WhatsApp direct-link CTA, composed entirely from Phase-3 primitives and Phase-2 tokens.

## What was built

**Task 1 — services.html markup (commit de44b5f)**
Inserted a `<section class="pfg-section pfg-pricing-section">` in the gap between the closing «Получить консультацию» CTA section and the FAQ comment. Structure: `.pbmit-heading-subheading` («Тарифы» eyebrow + «Пакеты бухгалтерского сопровождения» headline), a `.pfg-lead` intro, then `.pfg-grid.pfg-pricing` with exactly 3 `.pfg-card.pfg-pricing-tier` cards. The middle tier carries `pfg-pricing-tier--popular` + a `<span class="pfg-pricing-badge">Популярный</span>` first child. Each tier has an `<h3>` name, a `.pfg-pricing-price` line, a `<ul>` of scope bullets, and a CTA. The popular tier CTA is the gold-fill primary (`.pbmit-btn`); the two siblings step down to `.pbmit-btn white` — exactly one prominent primary. Every CTA: `<a href="https://wa.me/77072370050" target="_blank" rel="noopener">` with the theme's nested-span button markup (direct-link arm, no form, no JS).

**Task 2 — css/custom.css styling (commit 3dc9a93)**
Appended stage block «ЭТАП 15 — CNV-02 тарифные карты». `.pfg-pricing-tier` is a flex column with `.pbmit-btn{margin-top:auto}` so CTAs pin to the bottom and align across the row. `.pfg-pricing-price` = `var(--pfg-fs-h4)`, weight 600, `var(--pfg-ink)`. `.pfg-pricing-tier--popular` = `border-color:var(--pfg-gold)` + `box-shadow:var(--pfg-shadow-md)` (gold in border, not fill — body stays AA-readable). `.pfg-pricing-badge` = gold plate, `#1b1b1b` text (AA on gold), `text-transform:none`. The `<ul>` gets a 4px-grid rhythm. All values from `--pfg-*` tokens (only established `#1b1b1b` text-on-gold hardcoded). No net-new `!important`. The card hover-lift is inherited from `.pfg-card`, already covered by the scoped `prefers-reduced-motion` block (line 378) — no new motion added, so no reduced-motion edit needed.

## Verification (real, Playwright)

Static server `python -m http.server 8099`; Playwright (chromium) at 5 viewports — 360, 414, 768, 1024, 1440. Every viewport PASS:

| Viewport | tiers | popular | badge | gold primary | CTA→wa.me | h-scroll | equal row-height |
|----------|-------|---------|-------|--------------|-----------|----------|------------------|
| 360 | 3 | 1 | 1 | 1 | ok | no | yes |
| 414 | 3 | 1 | 1 | 1 | ok | no | yes |
| 768 | 3 | 1 | 1 | 1 | ok | no | yes |
| 1024 | 3 | 1 | 1 | 1 | ok | no | yes (691/691/691) |
| 1440 | 3 | 1 | 1 | 1 | ok | no | yes (588/588/588) |

`ctaOk` confirms all 3 tier CTAs have `href="https://wa.me/77072370050"`, `target="_blank"`, `rel` containing `noopener`. On stacked mobile (360/414) cards are single-column so heights legitimately differ; side-by-side rows (1024/1440) are pixel-equal.

Static checks:
- `grep -c '!important' css/custom.css` = **59** (raw and filtered) — no net-new.
- `git diff HEAD~2 HEAD -- js/custom.js` = **0 lines** — JS byte-identical (VER-04).
- `git diff HEAD~2 HEAD --name-only` = only `services.html` + `css/custom.css`. No other HTML page touched; hero copy untouched.

## Deviations from Plan

None - plan executed exactly as written.

(Note: during execution the in-file Russian comments initially contained the literal class tokens `pfg-pricing-tier--popular` / `!important`, which inflated grep counts. Comments were reworded to avoid the tokens before commit so the verification greps reflect actual code, not prose. This is a wording adjustment, not a behavioral deviation.)

## Threat Surface

Per the plan's `<threat_model>`: T-04-01 (reverse-tabnabbing on `target="_blank"` CTAs) — mitigated, every pricing CTA carries `rel="noopener"` (Playwright-confirmed). No new network endpoints, auth paths, or dynamic interpolation introduced. No threat flags.

## Known Stubs

None. Indicative pricing («от … ₸ / мес», «по запросу») is an intentional content decision (D CNV-02 — exact figures deferred to v2 pending business confirmation), not a stub — the block is fully functional and converts via the live WhatsApp flow.

## Self-Check: PASSED
- services.html — FOUND (pricing section present, 3 tiers / 1 popular / 1 badge)
- css/custom.css — FOUND (.pfg-pricing-tier / --popular / -price / -badge defined)
- commit de44b5f — FOUND
- commit 3dc9a93 — FOUND
