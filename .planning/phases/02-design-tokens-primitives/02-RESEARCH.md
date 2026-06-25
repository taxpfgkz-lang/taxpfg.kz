# Phase 2: Design Tokens + Primitives - Research

**Researched:** 2026-06-25
**Domain:** CSS design-token consolidation on a frozen no-build vendored-theme static site (GudFin/PBMIT + Bootstrap 5.2, `custom.css` override layer)
**Confidence:** HIGH (codebase is the source of truth; every claim below is grep/read-verified against live `css/custom.css` / `css/base.css` / `css/style.css`)

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Стратегия применения spacing scale (TOK-02, VIS-02)**
- Объявить `--pfg-space-*` (4/8/12/16/24/32/48/64/96) + точечно заменить отступы по AUD-02-находкам (card 28px → `--pfg-space-6`/`-8`, rhythm-snap по section paddings). НЕ переписывать корректно читающиеся отступы.
- Замена существующих значений = snap к ближайшему токену, сохраняя визуальный ритм темы (не точные значения шкалы везде).
- VIS-02 (выравнивание/сетка): чинить только задокументированный в AUD-02 дрейф; НЕ реструктурировать vendor-grid.

**Fluid type scale + переносы (TOK-03)**
- `clamp()` по ролям UI-SPEC (body / label / heading / display), ratio ≈1.25; чинит AUD-02 HE1/T2/G2 (heading line-height < font-size).
- Русские переносы: `text-wrap: balance` на заголовках, `pretty` на body + non-breaking для коротких предлогов/союзов (в, и, с, к, на, по, от).
- iOS focus-zoom (AUD-02 F1): mobile input font-size 15px → ≥16px через scale/токен.
- Объявление scale в `:root` слоя `custom.css` (грузится последним, побеждает), НЕ через base.css.

**Дисциплина токенов и !important-бюджет (TOK-01, VIS-03)**
- Свести ink+gold/radii/shadows/transitions/z-index в один `:root`-лист, переиспользуя `--pbmit-*` через `var()` (палитра НЕ расширяется новыми цветами).
- `!important`-бюджет: net-new ≈ 0 (floor = 57 функциональных деклараций из 01-CONFLICT-CATALOG). Каждый новый `!important` — с русским комментарием о перебиваемом vendor-правиле. 31 из 57 существующих uncited — подтвердить фактический beaten-селектор перед relocate/drop.
- VIS-03: gold-текст только `--pfg-gold-ink` (#7a560a, ≥5.4:1); gold-fill #ecab23 не трогать.
- `base.css` правки только если необходимо сослаться/хирургически переопределить `--pbmit-*` (namespace base.css:21-49); по умолчанию читать vendor-токен через `var()` из custom.css.
- Никакого `@layer` (unlayered vendor всегда бьёт layered) — побеждать source-order + точечной специфичностью.

### Claude's Discretion
- Точная организация/порядок токенов внутри `:root`-листа.
- Конкретные clamp() min/max значения для каждой роли (в рамках ratio 1.25, base body 16–18px).

### Deferred Ideas (OUT OF SCOPE)
- Компоненты (кнопки/формы/карточки состояния) — Phase 3, после приземления токенов.
- Conversion-блоки + imagery — Phase 4.
- Финальная a11y + cross-device verification против floor — Phase 5.
- PERF-01/02/03, MNT-01 — v2.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TOK-01 | Консолидировать дизайн-токены (палитра, радиусы, тени, transitions, z-index) в `:root` слоя `custom.css` | Q1 — карта существующих `--pfg-*` (`custom.css:284-302`) + пробелы (нет `--pfg-space-*`, нет fluid type, нет z-index, нет `--pfg-gold` text-token дублей). План = дополнение, не пересоздание |
| TOK-02 | Единый spacing scale на токенах, применённый к отступам секций/блоков | Q2 — фактическая карта paddings: что уже кратно 4 (оставить) vs дрейф (28px→24/32, 34px→32). Привязка к C1 |
| TOK-03 | Type scale на `clamp()`, корректный line-height, нет грубых переносов | Q3 — реальные heading fs/lh (base.css h1-h6, hero 170/150), body 17px; Q6 — `text-wrap` поддержка; F1 input 15px |
| VIS-02 | Выравнивания/сетка к единому spacing scale; нет дрейфа | Q2 — только задокументированный AUD-02 дрейф (C1, P2 partial); vendor-grid не трогаем |
| VIS-03 | Контраст WCAG AA; золото не как body-текст | Q1 — `--pfg-gold-ink` уже существует и применён; VIS-03 = enforcement, не redesign (axe baseline = 0) |
</phase_requirements>

## Summary

Phase 2 — первая фаза с правками кода — это **консолидация и дополнение** уже существующего токен-слоя, а не его пересоздание. Реальный `css/custom.css` уже содержит зрелый `:root`-блок `--pfg-*` на строках 284-302 (ink+gold палитра, hairlines, paper-warm, shadow-шкала из 4 уровней, 2 radii, easing-кривая, 2 transition-пресета). Чего там **нет** и что Phase 2 добавляет: `--pfg-space-*` 4px-шкалы, fluid `clamp()` type-токенов, и (опционально) `--pfg-z-*` z-index-токенов. VIS-03 (контраст) — это **enforcement существующего**, а не новая работа: `--pfg-gold-ink #7a560a` уже объявлен (строка 289) и применён к eyebrow-надзаголовкам (359), body-цвет уже затемнён до AA (`#525d62`, строка 122), axe baseline = 0 нарушений.

Главные технические факты для planner-а: (1) тема задаёт заголовки фиксированными px в `base.css:223-249` (h1 58/65, h2 48/53 ... h6 22/?), а hero-заголовок — `font-size:170px` в `shortcode.css` (HE1: lh 150 < fs 170 на 1440 → клиппинг). (2) F1 iOS focus-zoom исходит из `style.css:2635-2641` `.form-control{font-size:15px}` — vendor-правило; чинится override в `.pfg-form .form-control` (уже есть селектор на 496-498, нужно добавить `font-size`). (3) Card padding 28px живёт в **двух** местах: `.pfg-card` (`custom.css:66`) и сервис-бокс (`custom.css:839`) — оба off-scale, snap к 24/32. (4) Из 57 функциональных `!important` в зоне Phase 2 (spacing/type) находятся ~26 section-padding деклараций; 18 из них уже cited (`responsive.css`/`base.css`), а ~8 uncited (ihbox-section, dark-section) — их beaten-селектор надо подтвердить только если реально relocate/snap.

**Primary recommendation:** Дополнить существующий `:root`-блок (`custom.css:284-302`) тремя группами токенов (`--pfg-space-*`, fluid type `--pfg-fs-*`/`--pfg-lh-*`, опц. `--pfg-z-*`), затем точечно применить их к ровно четырём AUD-02-находкам (HE1/T2/G2 heading lh, C1 card padding ×2, F1 input font-size, P2 title-bar) через snap-to-nearest. НЕ переписывать корректно читающиеся отступы, НЕ трогать vendor-grid, НЕ растить `!important`-счётчик.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Token declaration (`:root --pfg-*`) | Browser / Client (CSS custom properties) | — | Pure CSS cascade; no server, no build. `custom.css` `:root` loaded last → wins by source-order |
| Spacing-scale application | Browser / Client (CSS) | — | Override of theme/Bootstrap paddings via `.pfg-*` rules + targeted `pbmit-*` overrides |
| Fluid type scale (`clamp()`) | Browser / Client (CSS) | — | `clamp(min, vw, max)` resolved by browser at render; no JS, no media-query churn |
| Russian non-breaking words | Browser / Client (CSS only — partial) | Markup / JS (deferred) | CSS `text-wrap` handles orphan/widow; true preposition-`&nbsp;` needs HTML — see Open Question 1 (deferred, markup read-only) |
| Contrast enforcement (VIS-03) | Browser / Client (CSS color tokens) | — | Already landed; this phase only guards no regression vs axe baseline = 0 |

**All capabilities live in the single Browser/CSS tier.** There is no server, build, API, or storage tier on this site (confirmed: no `package.json`, no bundler, files served static). The only cross-tier concern is the *deferred* preposition-non-breaking, which would need a markup or JS tier that is out-of-bounds this phase.

## Standard Stack

**No package installation. No build. No new dependencies.** This is a frozen, vendored, no-build static site. The "stack" is the existing authoring surface and the verification toolchain already proven in Phase 1.

### Core (authoring surface — already present)
| Asset | Version/Location | Purpose | Why Standard |
|-------|------------------|---------|--------------|
| `css/custom.css` | live, ~951 lines, loaded last (`index.html:54`) | The ONLY file Phase 2 edits for tokens/scales | Loaded last → wins by source-order; project's bespoke override layer |
| `css/base.css` | `:21-49` token block | Vendor `--pbmit-*` source of truth | Read via `var()`; edit only to surgically reference/override a brand token |
| CSS Custom Properties | native browser | Token mechanism | Already the project's token pattern (`--pfg-*`, `--pbmit-*`) |
| `clamp()` | native CSS (Baseline, universal) | Fluid type scale | No JS, no media-query ladder; `clamp(MIN, PREFERRED, MAX)` |
| `text-wrap: balance` | native CSS | Heading orphan/widow guard | ~88% support, graceful degrade [CITED: caniuse.com/css-text-wrap-balance] |

### Supporting (verification toolchain — already used in Phase 1)
| Tool | Version (verified) | Purpose | When to Use |
|------|-------------------|---------|-------------|
| Python http.server | Python 3.14.0 `[VERIFIED: python --version]` | Serve site over HTTP so font/CSS relative paths resolve | `python -m http.server 8080` before every Playwright run |
| Node | v24.11.1 `[VERIFIED: node --version]` | Runtime for npx Playwright/axe | — |
| npx | 11.16.0 `[VERIFIED: npx --version]` | Run Playwright + axe without install | DOM-measure + a11y scan @ 1440/1024/768/390/360 |

**Installation:** none. No `npm install`. Playwright/axe invoked via `npx` on demand (the Phase-1 durable verify channel). No `node_modules/.bin/axe` present `[VERIFIED: ls]` — axe is pulled transiently via npx or the Playwright `@axe-core/playwright` pattern at run time.

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `clamp()` fluid type | Media-query breakpoint ladder | More rules, more `!important` risk against theme media queries, less smooth; rejected by UI-SPEC (fluid locked) |
| `text-wrap: balance` | JS-based balancer (e.g. wrap-balancer) | Adds JS dependency, violates "no JS edit Phase 2" + no-build; rejected |
| `@layer` for override isolation | — | FORBIDDEN (hard constraint): unlayered vendor always beats layered → breaks cascade |

## Package Legitimacy Audit

**Not applicable.** Phase 2 installs **zero** external packages. No `package.json`, no lockfile, no registry use. All libraries are vendored and read-only. The only externally-invoked tools (Playwright, axe via `npx`) are part of the pre-existing, user-confirmed Phase-1 verification channel and are not added to the project.

## Architecture Patterns

### System Architecture Diagram

```
                  Phase 2 = edit ONE file (custom.css :root + targeted rules)
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │  css/custom.css  (loaded LAST — wins by source-order)             │
   │                                                                   │
   │  :root  ───►  EXISTING --pfg-* (284-302)   ──┐                    │
   │               + NEW --pfg-space-*           ──┤                   │
   │               + NEW --pfg-fs-*/--pfg-lh-*   ──┤ token foundation  │
   │               + NEW --pfg-z-* (optional)    ──┘                   │
   │                          │                                        │
   │                          ▼  consumed via var() by                 │
   │   .pfg-card / .pfg-section / heading overrides / .pfg-form input  │
   └──────────────────────────┬────────────────────────────────────────┘
                              │ cascade override (no @layer, source-order)
                              ▼
   ┌─────────────────────────────────────────────────────────────────┐
   │  VENDOR (READ-ONLY): base.css --pbmit-* (21-49), style.css,       │
   │  responsive.css, shortcode.css  — brand source of truth, var()    │
   └─────────────────────────────────────────────────────────────────┘
                              │
                              ▼  rendered DOM
   ┌─────────────────────────────────────────────────────────────────┐
   │  Browser @ 1440/1024/768/390/360  ──►  Playwright DOM-measure     │
   │  (trust rendered box, NOT CSS text)  + axe (floor = 0 violations) │
   └─────────────────────────────────────────────────────────────────┘
```

### Recommended `:root` Structure (extend existing block at custom.css:284-302)
```
:root{
  /* --- existing palette + ink+gold (KEEP verbatim, 285-292) --- */
  --pfg-ink / --pfg-ink-deep / --pfg-gold / --pfg-gold-deep / --pfg-gold-ink
  --pfg-hairline / --pfg-hairline-2 / --pfg-paper-warm
  /* --- existing shadow/radius/motion (KEEP verbatim, 293-301) --- */
  --pfg-shadow-sm/-md/-btn/-btn-h / --pfg-radius / --pfg-radius-sm
  --pfg-ease / --pfg-tf-fast / --pfg-tf

  /* === NEW: spacing scale (TOK-02), all multiples of 4 === */
  --pfg-space-1:4px; -2:8px; -3:12px; -4:16px; -6:24px; -8:32px;
  --pfg-space-12:48px; -16:64px; -24:96px;

  /* === NEW: fluid type scale (TOK-03), ratio ~1.25, base 16-18 === */
  --pfg-fs-body / -label / -h4 / -h3 / -h2 / -display  (clamp())
  --pfg-lh-tight:1.2 / --pfg-lh-body:1.6 / --pfg-lh-display:1.15

  /* === NEW (optional, TOK-01): z-index tokens if any are hardcoded === */
  --pfg-z-*  (only if discovered — see Open Question 2)
}
```

### Pattern 1: Snap-to-nearest (TOK-02 application)
**What:** Replace only AUD-02-flagged drifting paddings with the nearest scale token; leave correct values alone.
**When to use:** Card padding 28px (off-scale) → `var(--pfg-space-6)` (24) or `-8` (32). ihbox-section 34px → `-8` (32).
**Example:**
```css
/* BEFORE (custom.css:66) */
.pfg-card{ ... padding:28px; ... }
/* AFTER — snap to 24, preserves rhythm; comment cites AUD-02 C1 */
.pfg-card{ ... padding: var(--pfg-space-6); ... }  /* 28→24, AUD-02 C1 */
```

### Pattern 2: Fluid heading with line-height floor (TOK-03, fixes HE1/T2/G2)
**What:** Headings use `clamp()` font-size + a line-height that is never below ~1.05 (no lh < fs).
**Example:**
```css
/* fixes G2: normalize lh policy so no heading sits below 1.0 */
:root{ --pfg-fs-display: clamp(34px, 4vw + 1rem, 56px); --pfg-lh-display:1.15; }
/* applied where the theme sets the offending fixed px (hero/title-bar) */
```

### Anti-Patterns to Avoid
- **Universal `*` motion/transition killer:** already removed once (documented `custom.css:315-331`). Never reintroduce — it kills brand Swiper/marquee/GSAP.
- **`@layer` for overrides:** FORBIDDEN — unlayered vendor beats layered.
- **`filter`/`backdrop-filter`/`transform` on off-canvas-menu ancestors (≤1200px):** collapses `height:100%` of the fixed menu. Keep any such effect gated `min-width:1201px` (pattern at `custom.css:390`).
- **Editing `base.css` heading px directly:** prefer overriding from `custom.css` via higher source-order. Edit `base.css` only to reference a `--pbmit-*` token.
- **Growing the `!important` count:** net-new ≈ 0.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Fluid sizing | JS resize listener / breakpoint ladder | native `clamp()` | Browser-native, zero JS, smooth, no media-query `!important` fights |
| Heading orphan/widow | Manual `<br>` or JS line-balancer | `text-wrap: balance` (headings), `pretty` (body) | Native, graceful degrade, no markup edit (markup read-only) |
| `<select>` arrow | external arrow image | inline SVG data-URI (already done `custom.css:85-89`) | No 404, no network request, vendor file untouched |
| Reduced-motion | universal `*` killer | scoped block (`custom.css:332-345`) | Preserves brand motion; the universal version already broke the site once |

**Key insight:** Every "hand-roll" temptation here re-creates a vendor or browser-native capability and risks the cascade/animation contract. The premium layer wins by *cascade + native CSS features*, never by JS or build tooling.

## Runtime State Inventory

Phase 2 is a **pure CSS token-layer edit** — not a rename, refactor, migration, or string-replacement of any persisted identifier. There is no datastore, service config, OS registration, secret, or build artifact that embeds a token name in a way that survives the edit. Explicitly, per category:

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| Stored data | None — static site, no database/datastore. `--pfg-*` token names live only in CSS source, never persisted | None |
| Live service config | None — no external service references CSS token names | None |
| OS-registered state | None — no OS registration embeds tokens | None |
| Secrets/env vars | None — no secret or env var references a `--pfg-*`/`--pbmit-*` name | None |
| Build artifacts | None — **no build step exists** (no `package.json`, no bundler verified). CSS is shipped as-authored; nothing to rebuild or reinstall | None |

**Token-name caveat (not runtime state, but cascade state):** if any existing `--pfg-*` token were *renamed*, every `var(--pfg-...)` reference in `custom.css` would break silently (computed value falls to initial/inherit). Phase 2 decision is **extend, do not rename** — existing tokens (`custom.css:285-301`) stay byte-identical; new tokens are additive. Verified consumers of existing tokens are internal to `custom.css` only (grep `var(--pfg-` stays within the one file).

## Common Pitfalls

### Pitfall 1: F1 input font-size override missing the cascade target
**What goes wrong:** Bumping input font-size to 16px in the wrong selector and the vendor `.form-control{font-size:15px}` (`style.css:2641`) still wins.
**Why it happens:** Vendor rule is plain `.form-control` (specificity 0,1,0); the project's `.pfg-form .form-control` (0,2,0) already exists at `custom.css:496-498` but currently sets only border/radius/transition — **no font-size**. Adding `font-size:16px` there wins by specificity AND source-order, no `!important` needed.
**How to avoid:** Add `font-size:16px` to the existing `.pfg-form .form-control,.pfg-form .form-select,.pfg-form textarea.form-control` block (496-498). 16px globally is safe (desktop unaffected visually; only iOS<16 auto-zoom is suppressed). Confirm contacts.html form fields carry `.pfg-form` ancestor (they do — UI-SPEC Copywriting cites `.pfg-form`).
**Warning signs:** Playwright DOM-measure of `.form-control` font-size still reports 15px at 390/360.

### Pitfall 2: Touching cited section-padding `!important` and miscounting the budget
**What goes wrong:** Relocating section-padding declarations into token form accidentally adds or drops an `!important`, breaking the net-new ≈ 0 floor (57 functional).
**Why it happens:** 26 of the 57 functional `!important` are section paddings (`custom.css:655-779`); 18 cite an exact vendor `file:line` (`responsive.css:145/234/310`, `base.css:528`), but 8 (ihbox-section 720-732, dark-section 765-779) are **uncited**.
**How to avoid:** If a section-padding value is NOT in the AUD-02 fix list, **leave it untouched** (it already reads correctly). Only the C1 card (28px, no `!important`, `custom.css:66`+`:839`) and possibly the ihbox-section 34px are in scope. Snapping the card needs **no** `!important` (it's a `.pfg-*` own rule). Re-run `grep -c '!important' css/custom.css` after edits → must stay ≤ 59.
**Warning signs:** `grep -c '!important'` returns > 59.

### Pitfall 3: clamp() heading override defeated by vendor specificity
**What goes wrong:** Setting `h2{font-size:clamp(...)}` in `custom.css` but the theme's slider/title-bar uses higher-specificity selectors (`.pbmit-slider-title`, `.pbmit-tbar-title`) that keep the fixed px.
**Why it happens:** Hero `font-size:170px` is on `.pbmit-slider-title` (shortcode.css), not bare `h2`. There's already a precedent override at `custom.css:182` (`@max-575 .pbmit-slider-one .pbmit-slider-title{font-size:clamp(34px,11vw,52px)!important}`) and `:929` (title-bar 32px). The desktop hero (1440) is NOT yet clamped — that's the HE1 gap.
**How to avoid:** Target the same vendor selectors the existing overrides use; for desktop hero add a clamp at the matching specificity. Decide with planner whether HE1 desktop hero normalization lands here (TOK-03) or is hero-polish (Phase 4 HE1/HE2) — UI-SPEC maps HE1 to BOTH; 02-UI-SPEC lists HE1/T2/G2 as Phase-2 line-height normalization. Recommendation: Phase 2 owns the **line-height policy** (no lh<fs) via tokens; Phase 4 owns hero height/LCP.
**Warning signs:** DOM-measure hero lh still < fs at 1440 after Phase 2.

### Pitfall 4: text-wrap: pretty on body silently does little / Russian prepositions still orphan
**What goes wrong:** Expectation that `text-wrap: pretty` + CSS alone prevents short Russian prepositions ("в", "и", "с") from ending a line. It does not — CSS cannot insert non-breaking behavior between specific words without markup.
**Why it happens:** `text-wrap: pretty/balance` optimize overall line breaking (orphans/widows) but have no per-word preposition rule. True "preposition never ends a line" requires `&nbsp;` in HTML — markup is read-only this milestone.
**How to avoid:** Be honest in the plan: `text-wrap: balance` (headings) + `pretty` (body) is the deliverable; preposition-level non-breaking degrades to "balance/pretty handles most orphans" and the per-word `&nbsp;` rule is **deferred** (needs markup or JS). See Open Question 1.
**Warning signs:** Reviewer expects zero orphaned prepositions from CSS alone.

## Code Examples

### Q1 — Existing `--pfg-*` token block (verbatim, custom.css:284-302) — the consolidation base
```css
:root{
	--pfg-ink:            #16222d;
	--pfg-ink-deep:       #0f1820;
	--pfg-gold:           #ecab23;
	--pfg-gold-deep:      #d6960f;
	--pfg-gold-ink:       #7a560a;   /* gold-as-text, AA >=5.4:1 — VIS-03 already satisfied */
	--pfg-hairline:       rgba(22, 34, 45, .10);
	--pfg-hairline-2:     rgba(22, 34, 45, .16);
	--pfg-paper-warm:     #f6f4ef;
	--pfg-shadow-sm:      0 2px 8px rgba(16,24,32,.05), 0 1px 2px rgba(16,24,32,.04);
	--pfg-shadow-md:      0 14px 34px -14px rgba(16,24,32,.20), 0 4px 10px -6px rgba(16,24,32,.10);
	--pfg-shadow-btn:     0 4px 14px -6px rgba(16,24,32,.30);
	--pfg-shadow-btn-h:   0 12px 26px -8px rgba(16,24,32,.34);
	--pfg-radius:         14px;
	--pfg-radius-sm:      10px;
	--pfg-ease:           cubic-bezier(.22, .61, .36, 1);
	--pfg-tf-fast:        .25s var(--pfg-ease);
	--pfg-tf:             .4s  var(--pfg-ease);
}
```

### Q3 — Vendor heading scale (base.css:223-249) — the fixed-px source TOK-03 makes fluid
```css
h1 { font-size: 58px; line-height: 65px; }   /* lh/fs 1.12 — OK */
h2 { font-size: 48px; line-height: 53px; }   /* 1.10 */
h3 { font-size: 40px; line-height: 45px; }   /* 1.12 */
h4 { font-size: 34px; line-height: 40px; }   /* 1.18 */
h5 { font-size: 28px; line-height: 32px; }   /* 1.14 */
h6 { font-size: 22px; line-height: ~28px; }
/* body: --pbmit-body-typography-font-size:17px; line-height:1.6 (base.css:37-38) */
/* Note: bare h1-h6 lh is already >= fs. The lh<fs problem (HE1) is hero .pbmit-slider-title
   font-size:170px / lh:150px in shortcode.css, NOT these base headings. */
```

### Q5 — F1 fix point: vendor source + existing override hook
```css
/* VENDOR (style.css:2635-2641) — the 15px source, READ-ONLY */
.form-control{ height:55px; font-size:15px; padding:10px 20px; ... }

/* EXISTING project override (custom.css:496-502) — add font-size HERE */
.pfg-form .form-control,
.pfg-form .form-select,
.pfg-form textarea.form-control{
	border: 1px solid var(--pfg-hairline-2);
	border-radius: var(--pfg-radius-sm);
	transition: border-color var(--pfg-tf-fast), box-shadow var(--pfg-tf-fast);
	/* ADD: font-size:16px;  — kills iOS<16 focus-zoom (F1); wins by specificity 0,2,0 > 0,1,0,
	   no !important needed; desktop visually unchanged (15->16px is +1px) */
}
```

### Q2 — Card padding 28px, the two off-scale occurrences (C1)
```css
/* custom.css:66  */ .pfg-card{ ...; padding:28px; ... }       /* -> var(--pfg-space-6) 24 or -8 32 */
/* custom.css:839 */ .pbmit-service-box-related h3 area{ padding:28px; }  /* second 28px, same snap */
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Fixed-px font-size + media-query ladder | `clamp(min, vw-preferred, max)` fluid type | Baseline since ~2020 | One declaration scales fluidly; no breakpoint churn — matches UI-SPEC locked fluid decision |
| `<br>` / JS to fix orphans | `text-wrap: balance` (headings) | Chrome 114/130, Safari 17.5, FF 121 [CITED: caniuse] | CSS-native, graceful degrade, no markup edit |
| `text-wrap: pretty` | newer body-line optimizer | Chrome 117+, Safari 26, FF limited [ASSUMED] | Progressive enhancement; degrades to `normal` where unsupported |

**Deprecated/outdated for this project:**
- Universal `*{transition-duration:.001ms!important}` reduced-motion killer — removed (commit `830a769`), broke brand animation. Never reintroduce.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `text-wrap: pretty` support (Chrome 117+, Safari 26, FF limited) | State of the Art | LOW — progressive enhancement; degrades to `normal`, no breakage. Exact versions not re-verified this session (caniuse page covered `balance` only) |
| A2 | contacts.html form inputs all sit under a `.pfg-form` ancestor (so the F1 override reaches them) | Pitfall 1 / Q5 | MEDIUM — if some input lacks `.pfg-form`, its 15px persists. Planner/executor must grep `.pfg-form` in contacts.html before relying on the override; fallback = broaden selector (still no `!important`) |
| A3 | The 8 uncited section-padding `!important` (ihbox-section, dark-section) are out of the AUD-02 fix list and stay untouched | Pitfall 2 | LOW — leaving them untouched is the safe default; only matters if planner chooses to snap them (then confirm beaten selector first) |
| A4 | Phase 2 owns heading **line-height policy** (no lh<fs); hero **height/LCP** is Phase 4 | Pitfall 3 | MEDIUM — UI-SPEC maps HE1 to both phases. If planner wants desktop-hero clamp in Phase 2, that's allowed but verify it doesn't regress hero composition |

## Open Questions

1. **Russian preposition non-breaking with markup read-only**
   - What we know: CSS `text-wrap: balance/pretty` guards orphans/widows globally and degrades gracefully. The CONTEXT decision lists "non-breaking для коротких предлогов/союзов (в, и, с, к, на, по, от)".
   - What's unclear: CSS alone **cannot** force a specific short word to never end a line — that requires `&nbsp;` in HTML (markup read-only) or a JS pass (no JS edit Phase 2).
   - Recommendation: Deliver `text-wrap: balance` (headings) + `pretty` (body) as the Phase-2 CSS-only wrapping fix. Explicitly **defer** per-word preposition `&nbsp;` to a future markup pass or optional JS enhancement (note as deferred, do not promise CSS-only). This is honest scoping — planner should record it as a known limitation, not a failure.

2. **z-index token inventory (TOK-01 completeness)**
   - What we know: TOK-01 lists "z-index" among tokens to consolidate. The existing `:root` block has no `--pfg-z-*`.
   - What's unclear: whether `custom.css` currently hardcodes any z-index worth tokenizing (whatsapp-float, sticky header, back-to-top).
   - Recommendation: Planner task should grep `z-index` in `custom.css`; if 0-2 occurrences and theme-owned, declaring `--pfg-z-*` is optional cosmetic consolidation, not a functional requirement. Do not invent a z-index scale with no consumers.

3. **HE1 desktop-hero clamp ownership (Phase 2 vs Phase 4)** — see A4. Resolve with planner: recommend Phase 2 = line-height policy only.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python (http.server) | Serve site for Playwright/font resolution | ✓ | 3.14.0 | Any static server |
| Node | npx runtime | ✓ | 24.11.1 | — |
| npx | Playwright + axe on demand | ✓ | 11.16.0 | — |
| Playwright browsers | DOM-measure @ 5 widths | Assumed (Phase-1 channel) | — | Re-install via `npx playwright install` if missing |
| axe-core | a11y/contrast scan | via npx/@axe-core/playwright (no local bin) | — | `npx @axe-core/cli` |

**Missing dependencies with no fallback:** none.
**Missing dependencies with fallback:** Playwright browser binaries not verified present this session — if a run fails, `npx playwright install chromium` resolves it (one-time, no project change). No local `axe` binary `[VERIFIED: ls]` — pulled transiently via npx, consistent with the Phase-1 durable channel.

## Verification Mechanics (Q7 — DOM-measured against AUD-01 floor)

**Durable channel (Юрий-confirmed, proven Phase 1):**
```bash
# 1. serve (relative css/font/Maps paths resolve over HTTP)
python -m http.server 8080
# 2. Playwright DOM-measure @ 1440 / 1024 / 768 / 390 / 360  +  axe scan
#    via npx (Playwright + @axe-core/playwright). Trust the RENDERED BOX, not CSS text.
# 3. JS smoke (VER-04): menu / WhatsApp float / lead-form->WhatsApp / marquee / slider / reduced-motion
# 4. budget gate
grep -c '!important' css/custom.css     # must stay <= 59
```

**Exact DOM measurements to assert after token edits (per finding):**
| Finding | DOM assertion @ widths | Pass condition |
|---------|------------------------|----------------|
| C1 card padding | `getComputedStyle(.pfg-card).padding` @ all | == 24px or 32px (snapped), no longer 28px |
| F1 input zoom | `getComputedStyle('.form-control').fontSize` @ 390, 360 | >= 16px |
| HE1/T2/G2 lh | heading `lineHeight` vs `fontSize` @ 1440 | lineHeight >= fontSize (no lh < fs) for clamped headings |
| TOK-03 fluid | heading `fontSize` @ 1440 vs 390 | scales (not constant); within clamp min/max |
| no-overflow | `document.documentElement.scrollWidth <= clientWidth` @ all | no horizontal scroll introduced |
| VIS-03 contrast | axe `color-contrast` (wcag2aa) all 11 pages | 0 violations (== AUD-01 floor) |
| a11y floor | Lighthouse a11y per page | >= AUD-01 row value (min 95) |

**Regression floor (must not drop):** a11y ≥ 95 every page, axe = 0 for `wcag2a/2aa/21a/21aa`, no new horizontal overflow, ≥44px tap targets unaffected, headings not clipped. Performance (55-57) recorded but NOT a gate this milestone.

## Security Domain

> `security_enforcement: true`, ASVS level 1. This phase is a **pure presentational CSS token layer** on a static, backend-less, form-less-of-server marketing site. There is no authentication, session, access control, server-side input handling, or cryptography in scope — and Phase 2 touches none of it (CSS custom properties + spacing/type only; `js/custom.js` not edited).

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No auth on site |
| V3 Session Management | no | No sessions/cookies/backend |
| V4 Access Control | no | Static public pages |
| V5 Input Validation | no (this phase) | Lead form validates client-side in `js/custom.js` (untouched Phase 2); form→WhatsApp deep-link, no server input sink |
| V6 Cryptography | no | None |

### Known Threat Patterns for static-CSS-edit
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| CSS `url()` data-URI injection / external request leak | Information Disclosure | Use inline SVG data-URI (already the pattern, `custom.css:86`); no new `url()` to third-party hosts in token work |
| Behavior/flow change masquerading as "style" | Tampering | Hard constraint: visual-only, `js/custom.js` not edited, form→WhatsApp byte-identical (VER-04 smoke) |

**Net security posture:** Phase 2 introduces no new attack surface. The only outbound requests on the site (Google Fonts `@import` in `base.css:16-19`, Maps) are vendor/theme-owned and untouched.

## Sources

### Primary (HIGH confidence — codebase, read/grep-verified this session)
- `css/custom.css` — token block (284-302), `.pfg-*` primitives (62-90), form override (496-509), section paddings (655-779), `!important` context, reduced-motion scope (332-345)
- `css/base.css` — `--pbmit-*` tokens (21-49), heading scale (223-249), body typography (208-217), `.pbmit-btn` (281-294)
- `css/style.css` — `.form-control{font-size:15px}` F1 source (2635-2641)
- `.planning/phases/01-baseline-audit-ui-design-contract/01-AUDIT.md` — HE1/HE2/C1/F1/T1/T2/G2 DOM-measured findings
- `.planning/phases/01-baseline-audit-ui-design-contract/01-CONFLICT-CATALOG.md` — 57 functional `!important` ledger, 31 uncited, do-not-touch boundary
- `.planning/phases/01-.../01-UI-SPEC.md`, `02-UI-SPEC.md`, `02-CONTEXT.md` — locked contract
- Tool versions: `node --version` 24.11.1, `npx --version` 11.16.0, `python --version` 3.14.0 [VERIFIED]

### Secondary (MEDIUM confidence)
- caniuse.com/css-text-wrap-balance — `text-wrap: balance` support ~88%, graceful degrade [CITED]

### Tertiary (LOW confidence)
- `text-wrap: pretty` exact version support — training knowledge [ASSUMED A1]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no packages; authoring surface and verify channel read-verified
- Architecture: HIGH — single CSS tier, cascade pattern confirmed in live file
- Token map (Q1): HIGH — existing `:root` read verbatim
- Spacing/type sources (Q2/Q3): HIGH — exact lines grep-confirmed in base.css/style.css/custom.css
- F1 source (Q5): HIGH — `style.css:2641` confirmed, override hook at `custom.css:496` confirmed
- `!important` zone (Q4): HIGH — ledger consumed from CONFLICT-CATALOG
- Russian wrapping (Q6): MEDIUM — CSS support cited; preposition limitation is a hard CSS fact, scoped honestly
- Pitfalls: HIGH — derived from documented prior incidents + live specificity analysis

**Research date:** 2026-06-25
**Valid until:** 2026-07-25 (stable — frozen vendored codebase, no fast-moving deps)
