# Stack Research — No-Build Static UI Polish Toolchain

**Domain:** Production UI polish of a vendored-Bootstrap static marketing site (taxpfg.kz)
**Researched:** 2026-06-25
**Mode:** Ecosystem (technique + tooling selection under fixed no-build constraints)
**Overall confidence:** HIGH

This is a *technique and tooling* research file, not a stack-selection file. The runtime stack is FIXED and non-negotiable (pure static HTML5/CSS3/vanilla-ES5-JS, no npm, no bundler, no backend; vendor libs vendored read-only). The only editable files are `css/custom.css`, `css/base.css`, `js/custom.js`. The question this answers: *which 2026 CSS techniques and audit tools are appropriate to reach production UI quality without breaking the vendored Bootstrap 5.2 theme or introducing a build.*

---

## Key Recommendations

| Decision | Recommendation | Confidence |
|----------|----------------|------------|
| CSS override strategy | Design tokens (custom properties) + **targeted specificity**, NOT `@layer` | HIGH |
| `@layer` cascade layers | **DO NOT USE** for the override layer — see rationale below | HIGH |
| `:where()` | Use for low-specificity *resets/defaults* you want to stay overridable | HIGH |
| Spacing/type scale | CSS custom properties on `:root`, consumed via `clamp()` for fluid type | HIGH |
| `!important` reduction | Replace with specificity escalation + the load-order guarantee | HIGH |
| Local serving for audits | `python -m http.server 8000` from repo root | HIGH |
| A11y automation | `@axe-core/playwright` (already have Playwright MCP) | HIGH |
| Lighthouse | Standalone CLI via `npx lighthouse` (no project needed) | HIGH |
| Responsive testing | Playwright viewport sweep at Bootstrap 5.2 breakpoints | HIGH |
| Images | Hand-authored `<picture>` + WebP/AVIF + `srcset` + `loading="lazy"` | HIGH |

---

## CSS Architecture — winning specificity without `!important`

### The decisive finding: `@layer` is the WRONG tool here

The intuitive 2026 answer to "how do I beat vendor CSS cleanly" is cascade layers. **For this project that is incorrect, and using it would make overrides weaker.**

Verified rule (MDN `@layer`, confirmed 2026-06-25): for normal (non-`!important`) declarations,

> Styles that are NOT defined in a layer always override styles declared in named and anonymous layers, regardless of specificity.

Bootstrap `5.2.0-beta1` and the GudFin theme files (`style.css`, `responsive.css`, `shortcode.css`, etc.) are all **unlayered** — they ship plain rules, not wrapped in `@layer`. Bootstrap did not adopt cascade layers in the 5.x line; its CSS remains unlayered. (Confidence: HIGH — verified the precedence rule against MDN; the vendor files in `css/` contain no `@layer` declarations.)

Consequence: if you wrapped `custom.css` in `@layer overrides { … }`, every unlayered Bootstrap/theme rule would **automatically beat** your layered rule no matter how specific yours is. You would have to escalate to `!important` to win — the exact opposite of the goal. `@layer` only helps when the thing you are overriding is *also* layered (or lower in the layer order). Since the vendor CSS is unlayered and you may not edit it, layers cannot help and actively hurt.

The only way `@layer` could work would be to load the vendor CSS *into* a layer via `@import url(bootstrap.min.css) layer(vendor);`. That requires changing how vendor CSS is loaded (it is currently 13 separate `<link>` tags duplicated across 11 HTML heads) and would mean re-routing vendor loading through `@import` — a structural change to load order with real regression risk on a live theme. **Not worth it. Do not pursue.**

**Verdict: keep `custom.css` / `base.css` unlayered, loaded last.** Win by living in the same unlayered cascade as the theme and being (a) later in source order and (b) at equal-or-higher specificity.

### What to use instead

**1. Design tokens as CSS custom properties (the backbone).**
Define the entire premium "ink + gold" system once on `:root` in `base.css`, consume everywhere in `custom.css`. Custom properties inherit and are trivially themeable; they do not participate in specificity battles because the *property value* is resolved separately from selector matching.

```css
:root {
  /* color tokens */
  --pfg-ink:        #0f1417;
  --pfg-gold:       #c9a24b;
  --pfg-gold-ink:   #1a1d21;
  /* spacing + type scales live here too (see next section) */
}
```

**2. Targeted specificity, not `!important`.** The current code uses `!important` ~59× in `custom.css` and 9× in `base.css`. The fragile-areas concern is real: overrides depend on both load order *and* `!important`. Reduce `!important` by matching the vendor selector's specificity and adding one extra qualifier. Practical recipe:

- Inspect the *exact* winning vendor rule in DevTools (Computed → the rule that won).
- Match its selector shape, then add one more class/attribute the element already has, or scope under a page/section class. One extra class (0,1,0) is almost always enough to beat theme selectors without `!important`.
- Reserve `!important` only for utility-style single-property overrides where escalation is genuinely impractical (e.g., overriding a vendor inline-style fallback). Document each remaining `!important` with a one-line comment of *why*.

**3. `:where()` for resets you WANT to stay overridable.** `:where()` always has specificity 0 (verified against MDN, 2026-06-25), including its arguments. Use it for baseline/normalize-style rules in `base.css` so later `custom.css` rules — or even single-class theme rules — can override them without fighting. Do **not** use `:where()` for the rules that must beat the theme (they would lose); use it only for the floor.

```css
/* low-specificity baseline that anything can override */
:where(.pfg-card, .pfg-panel) { border-radius: var(--pfg-radius); }
```

**4. Scoping.** Prefer a root scope class (e.g. a `data-pfg` attribute on `<body>` or a `.pfg` wrapper) when you need a deterministic specificity bump that reads as intentional, rather than chaining vendor classes.

### Load-order guarantee (do not break this)

`custom.css` and `base.css` MUST remain the last stylesheets in every `<head>`. Because the whole strategy is unlayered source-order + specificity, reordering `<link>` tags silently breaks overrides. This is a "change-all-11-pages" invariant — treat any `<head>` edit as an 11-file checklist.

---

## Spacing scale & type scale as custom properties

Layer a small, explicit scale on top of the theme so spacing/typography stop being ad-hoc. Define on `:root` (in `base.css`), reference everywhere.

### Spacing scale (modular, rem-based)

```css
:root {
  --pfg-space-0: 0;
  --pfg-space-1: 0.25rem;  /*  4px */
  --pfg-space-2: 0.5rem;   /*  8px */
  --pfg-space-3: 0.75rem;  /* 12px */
  --pfg-space-4: 1rem;     /* 16px — base */
  --pfg-space-5: 1.5rem;   /* 24px */
  --pfg-space-6: 2rem;     /* 32px */
  --pfg-space-7: 3rem;     /* 48px */
  --pfg-space-8: 4rem;     /* 64px */
  --pfg-space-9: 6rem;     /* 96px — section rhythm */
}
```

Use these for section padding, card gaps, and stack spacing so the "единые отступы секций" goal is enforced by tokens, not eyeballing. They coexist with Bootstrap's own spacing utilities — you are not replacing Bootstrap's `--bs-*` vars, you are adding a parallel `--pfg-*` namespace consumed only by custom rules. (Confidence: HIGH.)

### Type scale (fluid, `clamp()`-based)

`clamp()` gives responsive type with no JS and no breakpoint media queries — ideal for no-build. Pattern: `clamp(MIN, PREFERRED-with-vw, MAX)`.

```css
:root {
  --pfg-step--1: clamp(0.83rem, 0.8rem + 0.15vw, 0.94rem);
  --pfg-step-0:  clamp(1rem,    0.95rem + 0.25vw, 1.13rem); /* body */
  --pfg-step-1:  clamp(1.2rem,  1.1rem  + 0.5vw,  1.5rem);
  --pfg-step-2:  clamp(1.44rem, 1.3rem  + 0.7vw,  2rem);
  --pfg-step-3:  clamp(1.73rem, 1.5rem  + 1.1vw,  2.66rem);
  --pfg-step-4:  clamp(2.07rem, 1.7rem  + 1.8vw,  3.55rem); /* hero h1 */
  --pfg-line-tight: 1.15;
  --pfg-line-body:  1.6;
}
```

Tooling note: generate the ratios with the free **Utopia** fluid-type calculator (utopia.fyi) — copy the resulting custom properties in by hand. No dependency added. This directly serves the "размеры, line-height, переносы, читаемость" requirement and prevents the giant-on-mobile / tiny-on-desktop failure modes. (Confidence: HIGH.)

Pair with `text-wrap: balance` on headings and `text-wrap: pretty` on body copy (both supported in all current evergreen browsers as of 2026) to kill ugly orphans/ragged wrapping — a zero-cost win for the "нет грубых переносов" requirement. (Confidence: HIGH for `balance`; `pretty` is progressive-enhancement, degrades gracefully.)

---

## Audit Tooling — all runnable with no npm project

### Serve the static files first

Relative asset paths and the Google Fonts requests resolve correctly only over HTTP. From the repo root:

```bash
python -m http.server 8000
# site now at http://localhost:8000/index.html, /about.html, …
```

(Windows/PowerShell: `python -m http.server 8000` works identically; if `python` maps to the launcher, `py -m http.server 8000`.) Keep this running in a background terminal during the whole audit. (Confidence: HIGH.)

### Lighthouse — standalone, no build, per-page

Run Lighthouse without installing anything into the project via `npx`:

```bash
npx lighthouse http://localhost:8000/index.html \
  --only-categories=performance,accessibility,best-practices,seo \
  --preset=desktop \
  --output=html --output-path=./audit/lighthouse-index-desktop.html \
  --chrome-flags="--headless"

# mobile profile (throttled, the harsher target):
npx lighthouse http://localhost:8000/index.html \
  --preset=mobile --output=html \
  --output-path=./audit/lighthouse-index-mobile.html \
  --chrome-flags="--headless"
```

Loop the 11 pages. This establishes the a11y baseline the milestone must not regress below ("Lighthouse/accessibility не хуже текущего"). Capture the current scores BEFORE any change as the floor. Note: write audit artifacts to a gitignored folder (`.gitignore` already excludes screenshot/Playwright artifacts). (Confidence: HIGH.)

> "Lighthouse CI as a standalone" — full Lighthouse-CI (`@lhci/cli`) wants a config and ideally a CI runner; for a no-build manual audit the plain `npx lighthouse` per-page is the right weight. Reserve `lhci autorun` only if a CI pipeline is later added (out of scope this milestone).

### axe-core via Playwright — the a11y workhorse

Playwright is already the project's verification tool (per memory). Drive `@axe-core/playwright` for deterministic, rule-level a11y findings (better signal than Lighthouse's a11y subset, and scriptable across all 11 pages × 3 viewports). Even with Playwright via MCP you can run a throwaway script with `npx` (no project install):

```bash
# one-off, nothing added to the repo:
npx --yes playwright@latest install chromium
```

Script pattern (run with `node`, file kept outside the tree or gitignored):

```js
const { chromium } = require('playwright');
const AxeBuilder = require('@axe-core/playwright').default;

const pages = ['index','about','services','accounting','accounting-recovery',
  'taxes','consulting','registration','contacts','privacy','404'];
const viewports = { desktop:[1440,900], tablet:[768,1024], mobile:[390,844] };

(async () => {
  const browser = await chromium.launch();
  for (const p of pages) {
    for (const [name, [w,h]] of Object.entries(viewports)) {
      const page = await browser.newPage({ viewport:{width:w,height:h} });
      await page.goto(`http://localhost:8000/${p}.html`, {waitUntil:'networkidle'});
      const res = await new AxeBuilder({page})
        .withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();
      if (res.violations.length)
        console.log(`${p} @ ${name}:`, res.violations.map(v=>v.id));
      await page.close();
    }
  }
  await browser.close();
})();
```

This pins WCAG 2.2 AA tags — which surfaces the known header `target-size` (2.5.8) flag the project intentionally left. Goal is 0 *new* violations; the pre-existing header overlap is a documented exception, not a regression. (Confidence: HIGH.)

### Chrome DevTools — manual depth

For the things automation cannot judge (visual hierarchy, alignment, "looks expensive"): DevTools device-mode for breakpoint sweeps, the **Computed** pane + "Show all" to trace which vendor rule won an override fight (this is how you find the minimal specificity bump to retire an `!important`), and the **Rendering** tab for paint-flashing / layout-shift spotting. The **Recorder** + Performance panel catch CLS from the unsized images. (Confidence: HIGH.)

---

## Responsive Testing

### Bootstrap 5.2 breakpoints (test exactly at and around these)

| Name | Token | min-width | Test viewport |
|------|-------|-----------|----------------|
| (xs) | — | <576px | 375 / 390 (mobile) |
| sm | `sm` | ≥576px | 576 |
| md | `md` | ≥768px | 768 (tablet portrait) |
| lg | `lg` | ≥992px | 992 |
| xl | `xl` | ≥1200px | 1200 |
| xxl | `xxl` | ≥1400px | 1440 (desktop) |

(Bootstrap 5.x breakpoint set; stable across 5.0–5.3. Confidence: HIGH.) The theme's own `responsive.css` also keys off ≤1200px for the mobile nav/off-canvas — test the 992–1200 band carefully since that is where the header switches and where the known target-size overlap lives.

### Method

Drive the Playwright viewport sweep above with screenshots at each breakpoint for all 11 pages (`page.screenshot({path: ...})`), then eyeball desktop/tablet/mobile side by side. Test *just below and just above* each min-width (e.g. 575/576, 767/768, 991/992, 1199/1200) — breakpoint bugs hide at the boundary. Watch for: broken wrapping, collapsed/overflowing grids, spacing that doesn't scale (the reason for the `--pfg-space-*` tokens), and the hero/pricing/CTA conversion blocks specifically. (Confidence: HIGH.)

---

## Image Optimization — no build, hand-authored

`images/` is ~6.9 MB, all PNG/JPG/SVG, zero WebP/AVIF (per CONCERNS.md). All of this is achievable by hand without a bundler.

### Generate modern formats with a one-off CLI (not a build step)

Use `cwebp`/`avifenc` (libwebp / libavif binaries) or `npx @squoosh/cli` for a one-time conversion pass. This is a manual asset op, not a pipeline — it produces files you commit, consistent with no-build:

```bash
# WebP (broad support, big win over PNG/JPG)
npx --yes @squoosh/cli --webp '{"quality":78}' images/slider1-01.jpg
# AVIF (best ratio, evergreen-only) — only for the heaviest hero/bg art
npx --yes @squoosh/cli --avif '{"cqLevel":30}' images/video-bg.png
```

Target the worst offenders first: `video-bg.png` (1.18 MB), `service-left-bg.png` (693 KB), `pattarn-01.png` (518 KB), the slider JPGs. (Confidence: HIGH.)

### Author the markup by hand

For `<img>` content images, `<picture>` with AVIF→WebP→original fallback:

```html
<picture>
  <source srcset="images/slider1-01.avif" type="image/avif">
  <source srcset="images/slider1-01.webp" type="image/webp">
  <img src="images/slider1-01.jpg" width="1200" height="675"
       alt="…" loading="lazy" decoding="async">
</picture>
```

Mandatory on every below-the-fold image: explicit `width`/`height` (kills CLS — directly protects the Lighthouse score), `loading="lazy"`, `decoding="async"`. The hero/LCP image should NOT be lazy — keep it eager and consider `fetchpriority="high"`.

For **CSS background images** (the theme's `video-bg.png`, `pattarn-01.png`, `service-left-bg.png` are backgrounds, not `<img>`), `<picture>` doesn't apply. Use `image-set()` in `custom.css` with WebP/AVIF and a fallback `background-image`:

```css
.section-hero {
  background-image: url(../images/video-bg.png); /* fallback */
  background-image: image-set(
    url(../images/video-bg.avif) type("image/avif"),
    url(../images/video-bg.webp) type("image/webp")
  );
}
```

`image-set()` is supported across all current evergreen browsers in 2026; the preceding plain `background-image` is the graceful fallback. (Confidence: HIGH.)

`srcset` with width descriptors (`srcset="img-800.webp 800w, img-1600.webp 1600w" sizes="…"`) is worth it for the slider/hero photos that render at very different sizes across the breakpoints; for small fixed icons it's overkill. (Confidence: MEDIUM — payoff depends on how variable each image's rendered size is; audit per-image.)

---

## What NOT To Do

| Anti-action | Why |
|-------------|-----|
| **Wrap `custom.css`/`base.css` in `@layer`** | Vendor CSS is unlayered → unlayered always beats layered; overrides would *lose*. Verified against MDN. |
| **Re-route vendor CSS through `@import … layer()`** | Requires changing load mechanism across 11 heads; high regression risk on a live theme for no real gain. |
| **Add a bundler / Vite / npm `package.json` to ship the site** | Explicit constraint: site stays no-build. (Tooling like `npx lighthouse` is fine — it's an *audit* tool, not part of the shipped site.) |
| **Edit any vendor/theme file** (`bootstrap.min.css`, `style.css`, `responsive.css`, `shortcode.css`, `swiper.*`, `gsap*`, `chart.js`, …) | Read-only by constraint; breaks theme updatability and invites silent regressions. |
| **Escalate to `!important` to win a fight** | Prefer one extra class / scope. Reserve `!important` for documented single-property utility overrides only. |
| **Reorder the `<link>` tags** | The whole override strategy depends on `custom.css`/`base.css` loading LAST. Reordering silently breaks it. |
| **`:where()` on rules that must beat the theme** | `:where()` is specificity 0 — those rules would lose. Use it only for the overridable baseline. |
| **Add JS-based fluid type or breakpoint libraries** | `clamp()` + media queries do it natively, no dependency, no FOUC. |
| **Lazy-load the hero/LCP image** | Hurts LCP. Lazy only below the fold. |
| **Touch the header `target-size` overlap casually** | Pre-existing, intentionally deferred; fixing needs vendor off-canvas rewrite. Only revisit if audit promotes it to blocker. |
| **Delete `js/chart.js` as part of UI polish** | It's dead weight but not shipped (no `<script>` references it); cleanup belongs to a payload milestone, not the UI contract. Out of scope here. |

---

## Confidence Assessment

| Area | Confidence | Basis |
|------|------------|-------|
| `@layer` is wrong here (unlayered vendor) | HIGH | MDN `@layer` precedence rule verified 2026-06-25; vendor files contain no `@layer` |
| `:where()` = specificity 0 | HIGH | MDN `:where()` verified 2026-06-25 |
| Custom-property token strategy | HIGH | Standard, framework-agnostic, no specificity interaction |
| `clamp()` fluid type / `text-wrap` | HIGH | Native, broadly supported in 2026 evergreens |
| Bootstrap 5.2 breakpoint values | HIGH | Stable Bootstrap 5.x set |
| `python -m http.server` + `npx lighthouse` + `@axe-core/playwright` runnable with no project | HIGH | Standard `npx`/python invocations, no manifest required |
| `<picture>` / `image-set()` / `srcset` support | HIGH | Baseline-supported 2026; fallbacks degrade gracefully |
| `srcset` width-descriptor payoff per image | MEDIUM | Depends on per-image rendered-size variance — audit case by case |

## Gaps / Open Questions for the roadmap

- Exact current Lighthouse a11y/perf scores per page are unknown until the baseline run — capture them first; they define the "не хуже" floor.
- Which images are `<img>` vs CSS backgrounds must be inventoried before choosing `<picture>` vs `image-set()` per asset.
- The remaining `!important` count after specificity refactor is unknown — target a measured reduction, not zero (some may be legitimately irreducible against the theme).

---

*Stack/technique research: 2026-06-25*

Sources (verified):
- [MDN — CSS `@layer` precedence](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer)
- [MDN — CSS `:where()` specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/:where)
