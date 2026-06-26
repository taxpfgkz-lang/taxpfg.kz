# Phase 3: Components - Research

**Researched:** 2026-06-26
**Domain:** Static no-build site UI component layer (vendored GudFin/PBMIT theme + Bootstrap 5.2 + `pfg-*` override layer); CSS cascade overrides, JS post-init a11y patching, net-new accessible FAQ accordion markup
**Confidence:** HIGH (all findings DOM/source-verified in this repo; zero external dependencies)

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Net-new компоненты (CMP-05 FAQ, CMP-06 модалки)**
- CMP-05 FAQ-аккордеон — построить ПОЛНОСТЬЮ: HTML `.accordion`-разметка (theme-handler js/scripts.js:309 уже существует, но ни одна страница не инстанцирует) + корректный ARIA + клавиатура. Разместить на **services.html** (вопросы об услугах) и **contacts.html** (перед формой) — типовые конверсионные места.
- FAQ a11y-слой — в js/custom.js (ARIA-состояния expanded/collapsed, keyboard) поверх theme-handler, по существующему initX()-паттерну (guard + early-return + idempotent). Форма→WhatsApp behavior-identical.
- CMP-06 модалки — **DESCOPE**: Magnific Popup загружен на 11 страницах, но триггеров (.pbmin-lightbox-video / a.pbmit-lightbox) ноль. Контракт гейтит «только если инстанцирован». НЕ фабриковать модалку. Зафиксировать descope честно.

**Стилизация существующих компонентов (CMP-01/02/03/04)**
- Кнопки (CMP-01): primary/secondary/ghost через override `.pbmit-btn` (не переименовывать), все 4 состояния hover/focus-visible/active/disabled. Primary=gold fill #ecab23 + ink-текст AA; secondary=outline/ink; ghost=text-weight + gold-ink hover. Тени --pfg-shadow-btn/-btn-h.
- Формы (CMP-02): rest/focus/error/success на `.pfg-form .form-control`; error/success через `.pfg-form-status` + классы. Soft gold focus-ring. Форма→WhatsApp поведение НЕ меняется.
- Карточки (CMP-03): rest + hover-lift (декоративный → в scoped reduced-motion блок custom.css:332-345); выровнять height-jitter (C2: 283px@1024 vs 256px@768).
- Навигация (CMP-04): rest/hover-underline-grow/active/focus-visible; glass-header gated ≥1201px; off-canvas-safe (нет filter/transform/backdrop-filter на предках мобильного меню). Theme-JS не ломать.

**a11y/tap-target markup-фиксы (AUD-02 P1)**
- FT1 footer links 26px (P1): починить 44px hit-zone через CSS padding на footer nav-links — выяснить, почему текущее правило custom.css:565-571 не применяется к этой группе ссылок (DOM-vs-CSS расхождение). Shared chrome → change-all-11 если трогается markup.
- F2 consent label 36px (P1): поднять hit-area до ≥44px через CSS (padding/min-height на `.pfg-consent label`).
- Подход: CSS-only где достигает (FT1/F2 — это padding/min-height); markup только если CSS не достаёт.
- VIS-01: свести heading/subheading/CTA/блоки/карточки к одному визуальному языку через токены Фазы 2 на всех 11 страницах.

**change-all-11 дисциплина и verify**
- Shared chrome (header/footer/nav) — любая markup-правка атомарно во все 11 HTML (grep возвращает 11), один коммит.
- FAQ не shared (разный контент на services/contacts) → единый СТИЛЬ без change-all-11 на контент.
- !important бюджет: net-new ≈ 0 (floor 59); каждый новый — с русским комментарием о перебиваемом vendor-правиле.
- Verify: Playwright DOM-measured @ 1440/1024/768/390/360 + axe + VER-04 JS-smoke (форма→WhatsApp/меню/marquee/slider/reduced-motion) против AUD-01 floor (a11y≥95, axe=0).

### Claude's Discretion
- Точные значения паддингов/теней состояний (в рамках токенов и контракта).
- Конкретный HTML-каркас FAQ-аккордеона (semantic <details>/<summary> vs button+region) — выбрать по лучшей a11y и совместимости с theme-handler.
- Сколько FAQ-вопросов и их формулировки (контент) — разумный минимум для услуг.

### Deferred Ideas (OUT OF SCOPE)
- CMP-06 модалки — descoped (Magnific не инстанцирован); если позже инстанцируют — отдельная задача.
- Conversion-блоки (hero/pricing CNV-02/CTA/footer) — Phase 4.
- Финальный a11y pass + cross-device verification + before/after — Phase 5.
- PERF (image/font опт), MNT (templating) — v2.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| VIS-01 | Единая визуальная система heading/subheading/CTA/блоки/карточки на 11 страницах | §VIS-01 drift map below: identifies which selectors already unify (eyebrow, `.pbmit-btn`, `.pfg-card`) and the two card-carrier divergence (`.pfg-card` vs `.pbmit-minfotech-post-item` vs `.pbmit-element-service-style-2`). Enforcement via existing Phase-2 tokens — no new tokens. |
| CMP-01 | Кнопки primary/secondary/ghost × hover/focus-visible/active/disabled, контраст AA | Q1 below: full inventory of existing `.pbmit-btn` rules (color/shadow/transform/radius/focus-ring), the three carriers (`.pbmit-btn`, `.pbmit-btn.white`, `.pbmit-btn.blackish`), missing states (`:disabled`, explicit ghost tier), specificity needed (0,1,0 + source-order beats vendor — net-new !important=0). |
| CMP-02 | Формы: labels, focus/error/success, mobile keyboards; форма→WhatsApp неизменна | Q2 below: `.pfg-form .form-control` rest/focus rules exist; `.pfg-form-status.is-error/.is-ok` color-only today (needs non-color affordance). `initLeadForm` flow documented byte-for-byte (VER-04 do-not-touch). Error/success class-add points identified — no JS behavior change. |
| CMP-03 | Карточки rest + hover-lift; C2 height-jitter resolved; ARIA/focus; theme-JS intact | Q3 below: `.pfg-card` rest+hover already complete (custom.css:543-555). C2 root cause = `height:100%` on `.pfg-card` only equalizes inside a flex/grid row whose track stretches; jitter is content-driven, not min-height. Fix = grid `align-items:stretch` already implied; equalize via consistent card content or min-height token. |
| CMP-04 | Nav rest/hover-underline/active/focus-visible; glass ≥1201; off-canvas-safe; theme-JS intact | Q4 below: underline-grow exists (custom.css:458-471), focus ring exists (351-358), glass-header gated `min-width:1201px` (434-441) with documented off-canvas rationale. N1/N2 tap targets healthy. No new work beyond documenting scope + verifying. |
| CMP-05 | FAQ-аккордеон net-new: collapsed/expanded/focus, ARIA+keyboard, theme-JS compatible | Q5 below: theme handler (scripts.js:309) is class-toggle only, NOT a state manager — `<details>/<summary>` recommended (native a11y+keyboard, zero JS dependency, won't fight handler). Exact insertion points given for services.html (after line 450, before `</main>`) and contacts.html (replace/augment line 295 "Остались вопросы?" section, before form at 256 — CONTEXT says "before the form"). |
| CMP-06 | Модалки — только если Magnific инстанцирован | Q6 below: grep across all 11 HTML = 0 occurrences of `pbmin-lightbox-video`, `pbmit-lightbox`, `magnificPopup`, `mfp-`, `.accordion`. DESCOPE confirmed honestly. |
</phase_requirements>

## Summary

Phase 3 is the largest phase but contains **almost no greenfield risk**: four of seven requirements (CMP-01/02/03/04) are *polish of components that already have substantial styling in `css/custom.css`*, and the Phase-2 token foundation they consume is verified landed. The single genuinely net-new artifact is the **CMP-05 FAQ accordion** (markup + a11y layer), and the single genuine root-cause investigation is **FT1** (footer links measured 26px despite a documented 44px rule). CMP-06 is a clean, honest descope — verified zero Magnific triggers across all 11 HTML files.

The dominant architectural fact: this is a **cascade-override + post-init-patch** system. CSS wins by source-order (`custom.css` loads last) at matched or higher specificity — the repo has driven net-new `!important` to ~0 by exploiting this, and Phase 3 must continue that discipline. JS never owns widget init (the theme does); `js/custom.js` only adds the a11y layer the theme lacks, via guarded, idempotent `initX()` functions. The form→WhatsApp flow in `initLeadForm` is the VER-04 behavior-identity contract and must not be touched.

Two findings change the plan materially. **(1) FT1 root cause is selector miss, not override:** the existing 44px footer rule (custom.css:634-640) targets *only* `.site-footer .widget .pbmit-two-column-menu ul.menu li a` and *only* `@media (max-width:575px)`. The 26px-measured links live in a **second, separate** footer menu — `.col-md-2 .widget > ul.menu` (the "Разделы" column, no `.pbmit-two-column-menu` wrapper) — which the selector never reaches. The fix is a broader footer-link hit-zone rule, not another padding stack on the existing selector. **(2) For CMP-05, prefer native `<details>/<summary>`:** the theme's accordion handler (scripts.js:309) is a naive class-toggler that assumes `.accordion-item`/`.accordion-button.collapsed` Bootstrap markup and provides no real open/close state or keyboard support — native `<details>` gives correct ARIA, keyboard, and zero coupling to that handler, satisfying the contract's "best a11y + compatibility" discretion.

**Primary recommendation:** Treat CMP-01/02/03/04 as targeted gap-fills on existing rules (add `:disabled` + explicit ghost tier for buttons; add a non-color affordance to form status; equalize card content height; document nav scope) styled with Phase-2 tokens at 0,1,0 specificity + source-order. Build CMP-05 as semantic `<details>/<summary>` with a thin idempotent `initFaqA11y()` enhancement (not a re-implementation). Fix FT1 with a footer-wide link hit-zone rule that reaches both menu groups; fix F2 with `min-height`/`padding` on `.pfg-consent label`. Descope CMP-06. Verify everything with DOM-measured Playwright + axe + VER-04 smoke.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Button hierarchy + states (CMP-01) | Browser / CSS (`custom.css`) | — | Pure presentation; cascade override of vendor `.pbmit-btn`. No JS. |
| Form visual states (CMP-02 visual) | Browser / CSS (`custom.css`) | — | Rest/focus/error/success are CSS class-driven; `.is-error`/`.is-ok` toggled by existing JS. |
| Form→WhatsApp behavior (CMP-02 logic) | Browser / JS (`custom.js` `initLeadForm`) | — | **Do-not-touch (VER-04).** Already complete; phase adds zero behavior. |
| Card styling + hover-lift (CMP-03) | Browser / CSS (`custom.css`) | — | Presentation + decorative motion (reduced-motion-gated). |
| Card height equalization (C2) | Browser / CSS (`custom.css`) | — | Layout via grid/flex stretch + content normalization. |
| Nav states + glass header (CMP-04) | Browser / CSS (`custom.css`) | Browser / JS (theme `scripts.js`, `custom.js` `initMobileMenu`) | Styling is CSS; open/close behavior owned by theme + existing `initMobileMenu` (do-not-touch). |
| FAQ accordion markup (CMP-05) | Browser / HTML (`*.html`) | Browser / CSS (`custom.css`) | Net-new semantic markup; styled via tokens. |
| FAQ a11y/keyboard (CMP-05) | Browser / JS (`custom.js` `initFaqA11y`) OR native `<details>` | — | Native `<details>` needs ~no JS; if button-based, thin idempotent patch. |
| FT1 footer hit-zone | Browser / CSS (`custom.css`) | — | Selector-reach fix; CSS-only (markup is identical across 11 — no markup edit needed). |
| F2 consent hit-zone | Browser / CSS (`custom.css`) | — | `min-height`/`padding` on label; CSS-only. |
| VIS-01 consistency | Browser / CSS (`custom.css`) | — | Enforcement via existing tokens across all carriers. |

## Standard Stack

No external packages. This is a **vendored, no-build static site** — the "stack" is the already-committed theme plus the project override layer. The phase introduces **zero new libraries, zero registry fetches, zero build tooling**.

### Core (already present — editable this phase)
| Asset | Version | Purpose | Why Standard |
|-------|---------|---------|--------------|
| `css/custom.css` | project (last stylesheet) | All bespoke overrides + `.pfg-*` primitives | Loaded last → wins by source-order; the one place styling lives |
| `js/custom.js` | project (last script) | a11y/ARIA patches + lead form; `initX()` IIFE | Loaded last → patches after theme init; the one place behavior lives |
| `*.html` (11 pages) | project | Page markup (scope-expanded 2026-06-26) | FAQ markup + (if ever needed) hit-zone markup land here |

### Supporting (vendored — READ-ONLY, do not edit)
| Asset | Version | Purpose | Constraint |
|-------|---------|---------|------------|
| GudFin/PBMIT theme CSS | commercial | `pbmit-*` components, `.accordion` handler base | Override only via cascade; never edit |
| `js/scripts.js` | theme | Widget init incl. `.accordion` click handler (line 309), Magnific init (296-303) | Read-only; layer over it |
| Bootstrap | 5.2.0-beta1 | Grid, `.form-control`, `.row`/`.col-*`, `.accordion`* classes | Use as-is in markup |
| jQuery | 3.7.1 | Theme handler dependency only | `custom.js` stays vanilla |

*Bootstrap 5.2's own `.accordion` component is NOT initialized by the theme; the theme's line-309 handler is a custom class-toggler, not Bootstrap's collapse plugin. See Q5.

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Native `<details>/<summary>` for FAQ | Theme `.accordion` + button[aria-expanded] + JS | Theme handler (scripts.js:309) is a fragile class-toggler with no keyboard/ARIA and Bootstrap-shaped markup assumptions; replicating it means more JS to maintain and a coupling to vendor behavior. Native `<details>` ships correct semantics, keyboard, and focus for free and is fully styleable. **Recommend native `<details>`.** |
| Bootstrap 5.2 collapse accordion | `<details>` | Bootstrap collapse needs JS init + `data-bs-*` wiring + ARIA authoring; heavier, and the theme doesn't init it. |

**Installation:** None. No `npm install`. No package manager exists in this project (confirmed: no `package.json`, no lockfile).

## Package Legitimacy Audit

**Not applicable.** This phase installs **zero external packages**. No npm/PyPI/crates dependency is added or considered. All libraries are pre-vendored and committed; the phase edits only `css/custom.css`, `js/custom.js`, and `*.html`. No registry verification required.

**Packages removed due to [SLOP] verdict:** none
**Packages flagged as suspicious [SUS]:** none

## Architecture Patterns

### System Architecture Diagram

```
                       ┌─────────────────────────────────────┐
   page load  ───────► │  *.html  (11 self-contained pages)  │
                       │  identical head/header/footer/scripts│
                       └───────────────┬─────────────────────┘
                                       │ links load assets in order
              ┌────────────────────────┼─────────────────────────────┐
              ▼                        ▼                              ▼
   ┌──────────────────┐   ┌──────────────────────┐   ┌────────────────────────┐
   │ vendor theme CSS │   │  css/custom.css      │   │ vendor JS (scripts.js, │
   │ (style/base/...) │──►│  LAST stylesheet     │   │ gsap, swiper, jQuery)  │
   │ pbmit-* rules    │   │  wins by source-order│   │ inits widgets on ready │
   └──────────────────┘   │  + matched specificity│   └───────────┬────────────┘
        cascade ▲          └──────────┬───────────┘               │ runs first
                └─── override ─────────┘                          ▼
                                                       ┌────────────────────────┐
   rendered  ◄────────────────────────────────────────│  js/custom.js          │
   component                                            │  LAST script          │
   (button/form/card/nav/FAQ)                           │  DOMContentLoaded →    │
                                                        │  initX() guarded,      │
                                                        │  idempotent a11y patches│
                                                        │  + initLeadForm (VER-04)│
                                                        └────────────────────────┘

   FAQ data flow (CMP-05, native <details>):
   user click/Enter on <summary> ─► browser toggles [open] ─► CSS animates panel
                                  └─► (optional) initFaqA11y observes, no behavior change

   Form data flow (CMP-02, VER-04 — UNCHANGED):
   submit ─► preventDefault ─► consent check ─► build text ─► window.open(wa.me/77072370050)
          └─► .pfg-form-status .is-error / .is-ok (CSS visual only)
```

### File-to-edit map (this phase)
| File | Edit type | What |
|------|-----------|------|
| `css/custom.css` | **Primary, append-only sections** | Button `:disabled` + explicit ghost tier; form status non-color affordance; card height equalization; FAQ `<details>` styling; FT1 footer hit-zone; F2 consent hit-zone; VIS-01 consistency enforcement |
| `*.html` (services.html, contacts.html) | Net-new markup | FAQ `<details>` sections at identified insertion points |
| `js/custom.js` | a11y layer only (optional for `<details>`) | If button-based accordion chosen: `initFaqA11y()`; otherwise none |

### Pattern 1: Cascade override at minimal specificity + source-order
**What:** Add a rule that matches the vendor selector at equal or +1 specificity; because `custom.css` loads last, equal specificity already wins.
**When to use:** Every CMP-01..04 gap-fill.
**Example (verified in repo, custom.css:561-578):**
```css
/* F1: vendor .form-control = 15px (style.css:2641). 0,2,0 > 0,1,0 + source-order; no !important. */
.pfg-form .form-control,
.pfg-form .form-select,
.pfg-form textarea.form-control{
	font-size: 16px;          /* beats vendor 15px without !important */
	border: 1px solid var(--pfg-hairline-2);
	border-radius: var(--pfg-radius-sm);
}
```

### Pattern 2: Guarded, idempotent post-init a11y patch
**What:** A small `initX()` that early-returns when its target is absent and checks-before-writing so late/repeat runs don't clobber state.
**When to use:** Any JS a11y enhancement (e.g. button-based FAQ, if chosen).
**Example (verified in repo, custom.js:153-159, 167-173):**
```js
function initSvgAria() {
	document.querySelectorAll('.pbmit-social-links svg').forEach(function (svg) {
		if (!svg.getAttribute('aria-hidden')) {     // idempotent
			svg.setAttribute('aria-hidden', 'true');
		}
	});
}
```

### Pattern 3: Scoped reduced-motion (never universal)
**What:** Disable *only* decorative micro-interactions added by the premium layer; never a universal `*{transition:none}` killer (that breaks Swiper/marquee brand motion).
**When to use:** Any new decorative motion (card lift, nav underline, FAQ expand).
**Example (verified in repo, custom.css:376-389):**
```css
@media (prefers-reduced-motion: reduce){
	.pfg-card, .pfg-card:hover, .pbmit-btn, .pbmit-btn:hover,
	.pbmit-header-style-1 .site-navigation ul.navigation > li > a::after{
		transition: none !important;   /* decorative only; brand motion untouched */
		transform: none !important;
	}
}
```

### Anti-Patterns to Avoid
- **Re-implementing the theme `.accordion` handler in `custom.js`:** It is a fragile class-toggler (scripts.js:309) assuming Bootstrap `.accordion-item`/`.accordion-button.collapsed` markup. Native `<details>` avoids the coupling entirely.
- **Adding a new `!important` to fix specificity:** The budget floor is 59 / net-new ≈ 0. Win by matched specificity + source-order. Every `!important` must cite the beaten vendor rule in a Russian comment (existing convention).
- **`filter`/`transform`/`backdrop-filter` on off-canvas-menu ancestors:** Collapses `height:100%` of the fixed mobile menu (documented custom.css:422-433). Glass effects stay gated `min-width:1201px`.
- **Touching `initLeadForm` / the WhatsApp number / message text:** VER-04 behavior-identity. Visual error/success is CSS-class only.
- **Stacking another padding rule on the existing footer selector for FT1:** It misses the affected link group (see Q7). Fix the selector reach, not the padding depth.
- **Universal `*` reduced-motion killer:** Removed historically (commit 830a769); breaks brand motion.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Accordion expand/collapse + keyboard + ARIA | Custom JS state machine over theme handler | Native `<details>/<summary>` | Browser gives focusable summary, Enter/Space toggle, `[open]` state, and correct AT semantics for free; fully styleable incl. marker |
| Focus ring | New per-component outline rules | Existing `:focus-visible` ring (custom.css:351-358) | Already gold, offset 3px, AA; reuse for FAQ summary |
| Spacing/type/color values | Hardcoded px/hex | Phase-2 tokens (`--pfg-space-*`, `--pfg-fs-*`/`--pfg-lh-*`, `--pfg-gold*`, shadows, radii) | Verified landed (02-VERIFICATION 5/5); VIS-01 consistency depends on it |
| Card hover lift | New transform rules | Existing `.pfg-card:hover` (custom.css:551-555) | Already lift+shadow+gold-border, reduced-motion-gated |
| Reduced-motion handling | New media block | Append to existing scoped block (custom.css:376-389) | Single source; avoids universal-killer regression |

**Key insight:** Almost every "component" in this phase already exists in `custom.css`. The work is *gap-filling specific states and reconciling two real defects*, not building components. The only true hand-roll temptation — an accordion — is exactly the thing the platform gives natively via `<details>`.

## Runtime State Inventory

This is **not** a rename/refactor/migration phase — it is additive UI styling + one net-new component. No stored data, service config, OS registrations, secrets, or build artifacts carry phase-relevant state.

- **Stored data:** None — static site, no datastore.
- **Live service config:** None — no external service config embeds component identifiers.
- **OS-registered state:** None.
- **Secrets/env vars:** None — the only "config" value is the hardcoded WhatsApp number `77072370050` in `custom.js:4`, which is **do-not-touch (VER-04)**, not renamed.
- **Build artifacts:** None — no build step; files served as-is.

**Cross-page propagation note (not runtime state, but plan-critical):** Header/footer/nav/script-block is **copy-pasted into all 11 HTML files** (no includes). Any shared-chrome *markup* edit is a change-all-11 atomic commit (grep returns 11 — verified). FT1/F2 are CSS-only (no markup edit needed), so change-all-11 does **not** trigger for them. FAQ content is page-specific (services/contacts only) → not shared chrome → no change-all-11.

## Common Pitfalls

### Pitfall 1: "The 44px footer rule exists, so FT1 is already fixed"
**What goes wrong:** Adding more padding to the existing footer selector; DOM still measures 26px.
**Why it happens:** The existing rule (custom.css:634-640) targets only `.pbmit-two-column-menu ul.menu li a` inside `@media (max-width:575px)`. The 26px links are in the **"Разделы" column** (`.col-md-2 .widget > ul.menu`, contacts.html:373) which has **no `.pbmit-two-column-menu` wrapper** — the selector never matches them. (The "Услуги" two-column group *is* covered.)
**How to avoid:** Write a footer-link hit-zone rule that reaches **both** menu groups — e.g. `.site-footer .widget ul.menu li a` (the common ancestor of both `<ul class="menu">` blocks). Verify by DOM-measuring *both* columns at 390/360.
**Warning signs:** A "fix" that only changes the Услуги column height in the screenshot.

### Pitfall 2: Trusting CSS source text over rendered box
**What goes wrong:** Concluding a target is ≥44px because a rule says so.
**Why it happens:** Vendor `line-height`, flex shrink, or selector miss override the intent.
**How to avoid:** Measure `getBoundingClientRect()` via Playwright at all 5 viewports (the established AUD method). Trust the box.
**Warning signs:** No DOM measurement in the verification evidence.

### Pitfall 3: FAQ markup that the theme handler hijacks or breaks
**What goes wrong:** Using `.accordion .accordion-item` Bootstrap-shaped markup triggers the theme's line-309 click handler, which toggles `.active` classes with no real state — clashing with `<details>` or producing dead toggles.
**Why it happens:** scripts.js:309 binds to `.accordion .accordion-item` globally on every page.
**How to avoid:** Use native `<details>/<summary>` with a **project class** (e.g. `.pfg-faq` / `.pfg-faq-item`), NOT `.accordion`/`.accordion-item`. The theme handler then never matches → no interference. (If a button-based pattern is chosen instead, also avoid `.accordion-item`.)
**Warning signs:** FAQ items that close instantly or require two clicks.

### Pitfall 4: iOS focus-zoom regression on the FAQ or any new input-like control
**What goes wrong:** Sub-16px font on an interactive control triggers iOS Safari zoom.
**Why it happens:** Same class as F1 (already fixed for form inputs).
**How to avoid:** FAQ summary text uses a token ≥16px (`--pfg-fs-body` clamps 16→18). No raw 15px on interactive text.

### Pitfall 5: Breaking the off-canvas mobile menu with decorative effects
**What goes wrong:** Adding `transform`/`filter`/`backdrop-filter` to a header/nav ancestor collapses the fixed off-canvas panel to ~49px.
**Why it happens:** Documented containing-block trap (custom.css:422-433).
**How to avoid:** Keep all glass/transform effects gated `min-width:1201px`; never apply to ancestors of `.pbmit-menu-wrap`.

### Pitfall 6: Color-only error/success status
**What goes wrong:** `.is-error` red / `.is-ok` green alone fails "never color-only" (master contract) for color-blind users.
**Why it happens:** Current rules (custom.css:52-53) are color-only.
**How to avoid:** The status already carries **text** (custom.js:84,105) so the message is non-color. Add a redundant non-color affordance (icon/`✓`/`!` prefix or border/weight) to make state visible without relying on hue. `role="status" aria-live="polite"` already present (contacts.html:273) — keep.

## Code Examples

Verified patterns from the actual repo (no external source needed — this is the project's own established style).

### CMP-01: Button states already present (the gaps to fill)
```css
/* PRESENT (custom.css:477-492): shadow, hover lift+gold-deep, active reset, blackish variant */
.pbmit-btn{ box-shadow: var(--pfg-shadow-btn); transition: background-color var(--pfg-tf-fast), box-shadow .4s ..., transform var(--pfg-tf-fast), color var(--pfg-tf-fast), padding .4s ease; }
.pbmit-btn:hover{ background-color: var(--pfg-gold-deep); box-shadow: var(--pfg-shadow-btn-h); transform: translateY(-2px); }
.pbmit-btn:active{ transform: translateY(0); }
.pbmit-btn.blackish{ box-shadow: 0 8px 22px -10px rgba(16,24,32,.55); }

/* PRESENT (custom.css:138-145): ink text holds AA on gold; focus ring (351-358) */
/* GAP TO ADD this phase: explicit :disabled (reduced-opacity, cursor:not-allowed, no shadow),
   and an explicit "ghost" tier (text-weight + --pfg-gold-ink hover, minimal chrome).
   Secondary tier already exists as .pbmit-btn.white / .blackish. */
```

### CMP-02: Form status — JS contract (DO NOT TOUCH) + CSS visual (the editable surface)
```js
// custom.js:82-108 — VER-04 behavior-identity. The phase touches NONE of this:
var consent = form.querySelector('[name="consent"]');
if (consent && !consent.checked) {
	status.textContent = 'Пожалуйста, подтвердите согласие на обработку данных.';
	status.className = 'pfg-form-status is-error';   // JS sets the class
	return;
}
// ...builds text, window.open('https://wa.me/' + WA_NUMBER + '?text=' + ...)
status.className = 'pfg-form-status is-ok';
```
```css
/* custom.css:52-53 — color-only TODAY. Phase 3 adds non-color affordance + soft focus ring
   already at :572-576. Style .pfg-form .form-control rest/error/success here, not in JS. */
.pfg-form .pfg-form-status.is-error{ color:#d33; }
.pfg-form .pfg-form-status.is-ok{ color:#1a9e57; }
```

### CMP-05: Recommended FAQ markup (native, theme-handler-safe)
```html
<!-- Insert in services.html before </main> (after line 450); in contacts.html before the
     lead-form <section> at line 247 (CONTEXT: "before the form"), reusing the existing
     "Остались вопросы?" eyebrow pattern. Use .pfg-faq NOT .accordion (avoids scripts.js:309). -->
<section class="pfg-section">
  <div class="container">
    <div class="pbmit-heading-subheading">
      <p class="pbmit-subtitle">Частые вопросы</p>
      <h2 class="pbmit-title">Отвечаем коротко</h2>
    </div>
    <div class="pfg-faq">
      <details class="pfg-faq-item">
        <summary>Вопрос на русском в предложном регистре?</summary>
        <div class="pfg-faq-panel"><p>Ответ.</p></div>
      </details>
      <!-- more items -->
    </div>
  </div>
</section>
```
```css
/* Native <details>: focusable <summary> gets the existing gold focus ring for free.
   Style with tokens; gate the expand transition into the reduced-motion block. */
.pfg-faq-item{ border-bottom:1px solid var(--pfg-hairline); }
.pfg-faq-item summary{ cursor:pointer; font-size:var(--pfg-fs-body); padding:var(--pfg-space-4) 0; list-style:none; }
.pfg-faq-item summary::-webkit-details-marker{ display:none; }   /* replace with token chevron */
/* :focus-visible ring already covers <summary> via the global a/button rule? NO — add summary
   to the existing focus-visible group (custom.css:351-358) so it gets the gold ring. */
```

### FT1: Root-cause fix (reach both footer menu groups)
```css
/* FT1 (AUD-02 P1): footer links 26px. Existing rule (custom.css:634-640) covers ONLY
   .pbmit-two-column-menu ("Услуги"); the "Разделы" col-md-2 .widget>ul.menu is uncovered.
   Reach BOTH via the common ancestor. line-height 26 + vertical padding → ≥44px hit zone.
   Specificity 0,4,1 ties/﹥ vendor + source-order; no !important needed if vendor sets no padding. */
.site-footer .widget ul.menu li a{
	display: inline-block;       /* or block; padding needs a box that respects it */
	padding-top: 9px;
	padding-bottom: 9px;         /* 26 + 18 = 44px target — DOM-verify both columns @390/360 */
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Custom JS accordion over theme handler | Native `<details>/<summary>` | Baseline HTML5; universally supported | Free keyboard/ARIA/state; no vendor coupling |
| Color-only status messaging | Text + non-color affordance | WCAG 1.4.1 | Required by master contract ("never color-only") |
| Universal `*` reduced-motion killer | Scoped reduced-motion block | commit 830a769 (this repo) | Brand motion (Swiper/marquee) preserved |
| Gold pill eyebrow badge | Ledger-stroke eyebrow (gold dash + spaced caps) | Этап 9 (custom.css:391-420) | The site-wide signature VIS-01 must keep consistent |

**Deprecated/outdated:**
- Theme `.accordion` handler (scripts.js:309): not deprecated but unsuitable as a standalone accordion engine (class-toggle only, Bootstrap-shaped markup assumption, no keyboard/ARIA). Avoid coupling FAQ to it.
- Bootstrap 5.2 `.accordion` collapse plugin: present in CSS but **not initialized** by the theme; do not rely on it.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Native `<details>/<summary>` is the best FAQ choice vs button+region | Q5 / Standard Stack | LOW — CONTEXT explicitly grants this as Claude's Discretion ("choose by best a11y + theme-handler compatibility"); both satisfy the contract. If styling the marker proves limiting, fall back to button[aria-expanded]+region with `initFaqA11y()`. |
| A2 | FT1's 26px links are the "Разделы" `col-md-2 .widget>ul.menu` group not covered by the existing `.pbmit-two-column-menu` selector | Q7 / Pitfall 1 | MEDIUM — verified by reading contacts.html:370-392 markup + the selector at custom.css:634. Planner should DOM-measure BOTH footer menu columns to confirm which group(s) read 26px before finalizing the selector. The AUD measured "15 visible links" which spans both groups. |
| A3 | Adding `<summary>` to the existing `:focus-visible` group gives it the gold ring | Code Examples (CMP-05) | LOW — `<summary>` is focusable; the existing ring targets `a/button/[role=button]/.pbmit-btn`. `<summary>` matches none → must be added explicitly. Verify focus ring renders on Tab. |
| A4 | C2 card-height jitter is content/track-driven, equalized by grid stretch + content normalization, not a min-height bug | Q3 | MEDIUM — `.pfg-card{height:100%}` only fills a stretched track; `.pfg-grid` uses `auto-fit minmax`. Planner should DOM-measure adjacent cards in a row at 1024 vs 768 to confirm whether a `min-height` token or content trim is the right lever. |

## Open Questions (RESOLVED)

1. **Exact FAQ content (questions/answers) for services.html and contacts.html**
   - What we know: CONTEXT marks count + wording as Claude's Discretion ("reasonable minimum for the services on each page"). Services page covers 5 service lines (footer "Услуги" menu enumerates them).
   - What's unclear: Which specific questions convert best for this accounting/tax firm.
   - Recommendation: Planner drafts 4-6 service-oriented Q&A per page in correct Russian sentence case (pricing, onboarding, document handoff, deadlines). Net-new Russian copy is the only new text (master contract allows).
   - **RESOLVED:** execution-time authoring task in plan 03-02 Task 1 (Claude's Discretion content, 4-6 Q&A/page).

2. **Which footer column(s) actually measure 26px (FT1 scope)**
   - What we know: Two distinct footer menus exist — "Разделы" (`col-md-2 .widget>ul.menu`, no two-column wrapper) and "Услуги" (`.pbmit-two-column-menu>ul.menu`). The existing 44px rule covers only the latter, and only ≤575px.
   - What's unclear: Whether both groups read 26px, or only the uncovered "Разделы" group, at 390/360.
   - Recommendation: DOM-measure both at 390/360 first; write one rule reaching the common ancestor `.site-footer .widget ul.menu li a` so both are covered regardless.
   - **RESOLVED:** plan 03-02 Task 2 mandates DOM-measuring BOTH columns @390/360 before finalizing, then applies a common-ancestor rule robust to either.

3. **C2 height-jitter lever (min-height token vs content normalization)**
   - What we know: `.pfg-card{height:100%}`; `.pfg-grid` is `auto-fit minmax(260px,1fr)`; jitter is 283@1024 vs 256@768 (cosmetic, no clipping per AUD).
   - What's unclear: Whether the jitter is acceptable reflow or needs an explicit `min-height`.
   - Recommendation: Confirm grid track `align-items:stretch` makes same-row cards equal (the AUD finding is about *cross-breakpoint* difference, which is expected reflow). Likely document as acceptable; only add `min-height` if same-row cards are unequal.
   - **RESOLVED:** plan 03-01 Task 3 uses diagnosis-before-fix — DOM-confirm same-row equality first; add min-height only if unequal, else document cross-breakpoint reflow as acceptable.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python (http.server) | Local serve for DOM-measured verify | ✓ (used in AUD-01/Phase-2 verify) | 3.x | Any static server |
| Playwright | DOM measurement @ 5 viewports | ✓ (used in baseline `measure.cjs`) | per baseline | Manual browser devtools (worse) |
| @axe-core/playwright | a11y regression gate (axe=0) | ✓ (4.12.1 in AUD-01) | 4.12.1 | axe browser extension |
| Lighthouse | a11y ≥95 floor confirmation | ✓ (13.4.0 in AUD-01) | 13.4.0 | Manual a11y review |
| Browser (Chromium) | Render | ✓ | — | — |

**Missing dependencies with no fallback:** none — the full verify toolchain was exercised in Phase 1 (AUD-01) and Phase 2 verification, both over `http://127.0.0.1:8080`.
**Missing dependencies with fallback:** none.

> Windows/Cyrillic-path note (from AUD-01): Lighthouse prints a non-fatal `EPERM ... rmSync` at temp cleanup *after* reports are saved — reports are valid; the error is cosmetic teardown only.

## Validation Architecture

**Section omitted per config:** `.planning/config.json` sets `workflow.nyquist_validation: false` (verified). No automated unit-test framework exists (no-build static site). Verification is the **DOM-measured Playwright + axe + Lighthouse + VER-04 JS-smoke** gate described below under the phase's own verify contract — not a Nyquist unit-test map.

**Phase verify gate (from CONTEXT + master contract):**
- Playwright DOM-measured @ 1440 / 1024 / 768 / 390 / 360: no horizontal scroll; ≥44px tap targets (footer links BOTH columns, consent label, FAQ summary); button states present; FAQ `<details>` toggles + `[open]`/`aria-expanded` consistent; same-row card heights equal; headings not clipped.
- axe (`wcag2a/2aa/21a/21aa`) = **0** on all 11 pages (AUD-01 floor).
- Lighthouse a11y ≥ **95** every page (AUD-01 floor; index/services/contacts = 96).
- VER-04 JS smoke: lead-form→WhatsApp (same number `77072370050` + message), mobile menu open/close, marquee speed, hero slider, reduced-motion — all behavior-identical.
- `grep -c '!important' css/custom.css` ≤ **59** (net-new ≈ 0); each new one cites beaten vendor rule in Russian.
- change-all-11 grep = 11 only if shared-chrome markup touched (FT1/F2 are CSS-only → should NOT trigger).

## Security Domain

> Required when `security_enforcement` is enabled (absent = enabled).

This is a **static, no-backend, presentation-only** phase. No authentication, sessions, access control, server-side input handling, or cryptography exist or are introduced.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No auth in project |
| V3 Session Management | no | No sessions; static files |
| V4 Access Control | no | No protected resources |
| V5 Input Validation | partial | Lead form is client-side only → composes a `wa.me` deep link via `encodeURIComponent` (custom.js:101). **Do-not-touch (VER-04).** No server trusts this input; values go only into a WhatsApp URL the user explicitly opens. |
| V6 Cryptography | no | None — no secrets handled client-side; WhatsApp number is public contact info |

### Known Threat Patterns for static-site/client-JS

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Reflected/stored XSS via injected markup | Tampering | FAQ content is **static authored HTML**, not user-supplied → no injection surface. Do not introduce `innerHTML` from untrusted input. The existing WhatsApp float uses a static SVG string (custom.js:65) — safe. |
| Open-redirect / tabnabbing on new-tab links | Tampering | New external links (WhatsApp, maps) already use `target="_blank" rel="noopener"` (verified contacts.html:403, custom.js:63). FAQ adds no external links; if any are added, keep `rel="noopener"`. |
| Deep-link parameter tampering (form→wa.me) | Tampering | Values pass through `encodeURIComponent` (custom.js:101) — already correct; **do not modify (VER-04).** |

**Phase-specific security note:** The only new author-controlled content is static FAQ copy. No new network calls, no new input sinks, no secret handling. Security posture is unchanged from baseline.

## Sources

### Primary (HIGH confidence — direct codebase read this session)
- `css/custom.css` (full, 1022 lines) — button/form/card/nav/footer/eyebrow rules, tokens, reduced-motion block, FT1/F2-adjacent rules
- `js/custom.js` (full, 202 lines) — `initX()` pattern, `initLeadForm` (VER-04 flow), a11y patches
- `js/scripts.js:296-329` — Magnific init + `.accordion` handler (CMP-05/CMP-06 truth)
- `contacts.html:247-451` — lead form, consent label, both footer menu groups (FT1 root cause), FAQ insertion point
- `services.html:163-453` — sections + button markup pattern, FAQ insertion point
- Grep across all 11 `*.html` for `pbmin-lightbox-video|pbmit-lightbox|magnificPopup|mfp-|.accordion` = **0 matches** (CMP-06 descope proof; FAQ-class-collision proof)
- `.planning/config.json` — `nyquist_validation:false`, no package manager

### Primary (HIGH confidence — prior phase artifacts)
- `01-AUDIT.md` (AUD-02) — DOM-measured findings C2/F2/FT1 + positive findings N1/N2/F3/FT2
- `01-UI-SPEC.md` + `03-UI-SPEC.md` — Component State Contract, Hard Constraints
- `01-IMPLEMENTATION.md` — Phase-3 file-map, net-new vs descope, `!important` budget
- `02-VERIFICATION.md` — Phase-2 tokens landed 5/5 (the foundation CMP-* consume)

### Secondary / Tertiary
- None needed. No external library/web research applies (vendored no-build site; no packages installed this phase).

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — "no new packages" is definitive (no `package.json`; vendored theme read directly).
- Architecture (override + post-init patch): HIGH — read full `custom.css`/`custom.js`; patterns are explicit and self-documented.
- CMP-01..04 gap analysis: HIGH — existing rules read line-by-line; gaps (`:disabled`, ghost tier, non-color status, card equalization) are concrete.
- CMP-05 FAQ approach: HIGH on theme-handler behavior (read scripts.js:309); MEDIUM on `<details>` vs button choice (explicitly Claude's Discretion).
- CMP-06 descope: HIGH — grep across all 11 HTML = 0 triggers.
- FT1 root cause: MEDIUM-HIGH — selector-miss identified by reading markup + selector; planner should DOM-confirm which column(s) read 26px (Open Q2).
- Pitfalls: HIGH — derived from documented repo history (commit 830a769, off-canvas trap, F1 zoom).

**Research date:** 2026-06-26
**Valid until:** 2026-07-26 (stable — static vendored site, no fast-moving deps)
