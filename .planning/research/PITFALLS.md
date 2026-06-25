# Pitfalls Research

**Domain:** UI polish / visual redesign of a vendored-theme static site (no build system, vendor read-only)
**Researched:** 2026-06-25
**Confidence:** HIGH (grounded in this repo's `.planning/codebase/` map + established CSS/WCAG/font-loading behavior)

> Scope reminder for everyone reading this: editable surface is **only** `css/custom.css`, `css/base.css`, `js/custom.js`. Everything else under `css/` and `js/` is vendor/theme and read-only. Header/footer/`<head>` markup is hand-duplicated across **11 HTML pages** with no include mechanism. Must not change behavior of business logic, forms→WhatsApp, analytics, routing, JSON-LD, or brand-identity animations. These constraints are what make the pitfalls below specific rather than generic.

---

## Critical Pitfalls

### Pitfall 1: `!important` escalation war against the theme

**What goes wrong:**
The override layer already carries ~59 `!important` in `css/custom.css` (+9 in `base.css`) purely to beat GudFin's deeply-nested, media-query-heavy selectors. A polish pass that adds rules by reflexively appending `!important` whenever "it didn't take" pushes that number up. Eventually two `!important` rules in the custom layer collide (e.g. a base-state override and a responsive override), and the only lever left is source order or even higher specificity stacked on top of `!important`. At that point the cascade is unreadable, every new change has unpredictable reach, and overrides silently stop working when the vendor ships a slightly different selector.

**Why it happens:**
`!important` is the fastest thing that "works" against a theme you don't control. Each individual use looks justified; the cost is only visible in aggregate. The theme's own high specificity trains the developer to escalate by default instead of diagnosing the actual winning rule.

**How to avoid:**
- Before adding `!important`, open DevTools, find the **exact** vendor rule winning, and beat it with **specificity** (add a contextual parent, e.g. `.pfg-prose p a:not(.pbmit-btn)` as already done at `custom.css:268`) rather than force. The convention is already documented at `custom.css:42-46` and `CONCERNS.md` — enforce it.
- New project-owned `.pfg-*` elements should need **zero** `!important`; reserve it strictly for fighting the theme. If a `.pfg-*` rule needs `!important`, that's a smell that the selector is too weak or it's colliding with another custom rule.
- Treat the `!important` count as a budget. Net-new `!important` in a polish phase should be near zero; if a change adds several, that is a signal to step back and find the structural cause.
- Consider scoping a clearly-bounded subset of new overrides inside a low-specificity wrapper class rather than escalating globally. (CSS `@layer` is the textbook fix for theme overrides, but note it would change the *meaning* of the existing `!important`-based cascade — see Technical Debt table; do not retrofit `@layer` mid-milestone.)

**Warning signs:**
- An override "works" only after a second or third `!important`.
- The same property is set `!important` in more than one custom rule and you're juggling which wins.
- Net `!important` count climbs during a phase whose goal was visual consistency, not new components.

**Phase to address:**
Audit phase (catalog current `!important` and the vendor rule each beats) + every implementation phase (specificity-first rule, `!important` budget in the UI design contract).

---

### Pitfall 2: Breaking theme JS by touching the hooks its scripts depend on

**What goes wrong:**
GudFin's `scripts.js` + GSAP/ScrollTrigger/SplitText, Swiper, AOS, Magnific Popup, and Bootstrap JS all select elements by **class, `data-*` attribute, or DOM structure**. A "harmless" visual edit — renaming a wrapper class, removing a `data-` attribute that looks decorative, re-nesting a slide, or adding a `transform`/`filter` to an ancestor — silently breaks slider init, scroll animations, the lightbox, or the off-canvas menu. Because there's no console error for "selector matched nothing," the breakage shows up only as a dead slider or frozen animation, often on one viewport.

**Why it happens:**
The class/attribute contract between markup and vendor JS is invisible. A polish task focuses on appearance and assumes markup is free to restructure. Some of the riskiest classes (`swiper-*`, `aos-*`, `pbmit-*`, `wow`, `data-aos`, `data-swiper-*`, `splitting`) look like styling hooks but are JS hooks.

**Dangerous to touch (do NOT rename, remove, or re-nest):**
- `swiper`, `swiper-wrapper`, `swiper-slide`, `swiper-pagination`, `swiper-button-*` and any `data-swiper-*` — Swiper queries these; re-nesting a slide breaks the slider.
- `data-aos`, `aos-init`, `aos-animate`, AOS offset/duration data attrs — AOS reads these on init.
- GSAP/ScrollTrigger targets: anything the theme animates by class/id (`pbmit-*` animated blocks, SplitText targets). Don't strip a class just because you restyled the element.
- `pbmit-*` structural classes that `scripts.js` selects (e.g. counters, circle-progress containers, marquee/`pbmit-*-slider` wrappers).
- Bootstrap behavior hooks: `data-bs-toggle`, `data-bs-target`, `collapse`, `modal`, `nav-link`, off-canvas menu classes the theme's mobile nav relies on.
- **Ancestor effects trap:** do NOT put `filter` / `backdrop-filter` / `transform` on an ancestor of the mobile off-canvas menu — it collapses the menu's `height:100%`. This exact constraint is already documented at `custom.css:382-389` (the glass header is gated to `min-width:1201px` precisely for this reason). Any new decorative effect must respect that gate.

**How to avoid:**
- **Style, don't restructure.** Achieve visual goals by adding `.pfg-*` classes/wrappers and CSS, not by editing the class soup the theme JS reads. If you must add a hook, *add* a class alongside the existing ones, never replace.
- All JS changes stay in `js/custom.js` (vanilla, IIFE, idempotent guards) and follow the established late-init polling pattern (`setInterval` 100ms / `MAX_TICKS`) when reaching into theme widgets — see `initMarqueeSpeed`, `initSwiperA11y`. Don't call Swiper `autoplay.stop()/start()` (breaks the marquee — documented at `custom.js:113-130`).
- After any markup or class edit, manually exercise every JS behavior (mobile menu open/close/Escape/backdrop, WhatsApp float, `.pfg-form` submit→`wa.me`, marquee, slider) per `TESTING.md` step 3.

**Warning signs:**
- A slider/animation/lightbox stops working after a CSS or markup edit, with no console error.
- You find yourself editing a `swiper-*`, `aos-*`, or `data-*` attribute "just for spacing."
- A decorative effect (shadow, blur, transform) is added high in the DOM tree near the header/menu.

**Phase to address:**
Audit phase (map which classes/attrs the theme JS depends on, mark a "do-not-touch" list in the UI design contract) + every implementation phase (style-don't-restructure rule; JS-behavior smoke test in verification).

---

### Pitfall 3: Visual drift from editing 1 of 11 duplicated pages

**What goes wrong:**
Header, footer, and the full `<head>` (13 `<link>` + 18 `<script>` + meta + JSON-LD) are copy-pasted into all 11 pages with no templating. A polish edit to nav, footer, a CTA, or a shared inline style applied to `index.html` and a few others — but not all 11 — leaves stale pages. The site looks consistent on the pages you reviewed and subtly wrong on the ones you didn't. There is no build-time check to catch it.

**Why it happens:**
No include mechanism + no test net. The reviewer naturally checks the pages they're working on (usually `index.html`) and assumes the shared chrome is shared. It isn't — it's 11 independent copies.

**How to avoid:**
- **Prefer CSS over markup for shared chrome.** Because `custom.css` loads on all 11 pages, a styling change made in CSS automatically reaches every page. Drive header/footer/CTA polish through `.pfg-*` rules in `custom.css` rather than per-page markup edits whenever possible. This sidesteps the duplication entirely.
- When a markup edit to shared chrome is unavoidable, treat it as a **"change-all-11" checklist item** (the term used in `CONCERNS.md`). Apply to all 11 in one pass: `404.html, about.html, accounting-recovery.html, accounting.html, consulting.html, contacts.html, index.html, privacy.html, registration.html, services.html, taxes.html`.
- **Detection strategy:** after any shared-chrome edit, diff the header/footer block across all 11 files (e.g. `rg`/Grep the changed string and confirm 11 hits, or extract the `<footer>`…`</footer>` block from each and compare). Then Playwright-screenshot the header + footer of all 11 at one breakpoint and eyeball for the odd one out. Do NOT mark done after checking only the page you edited.

**Warning signs:**
- A Grep for the new/changed shared string returns fewer than 11 hits.
- Footer year, phone, nav label, or CTA text differs between two pages.
- You only opened 2–3 pages during review of a change to shared chrome.

**Phase to address:**
Any phase touching header/footer/CTA/`<head>`. The "change-all-11 + diff + multi-page screenshot" verification belongs in every such phase's success criteria.

---

### Pitfall 4: Accessibility regressions introduced by visual changes

**What goes wrong:**
Visual polish silently erodes the a11y floor the project already paid for:
- **Focus removed:** a `:focus { outline: none }` (or `outline:0`) added "to clean up" a button/input/link kills keyboard focus visibility — a WCAG 2.4.7 failure and a real usability break for keyboard users.
- **Contrast lost:** restyling text gold-on-white using the brand fill `#ecab23` (≈1.9:1 on white) instead of the text token `--pfg-gold-ink: #7a560a` (chosen to clear AA ≥5.4:1) fails WCAG 1.4.3. Lightening the body color, putting text on a hero photo without the overlay, or low-contrast placeholder/disabled states do the same.
- **Motion without guard:** a new hover lift/parallax/transition added outside the scoped `prefers-reduced-motion` block (`custom.css:332-345`) reintroduces motion for users who opted out (WCAG 2.3.3 / vestibular safety).
- **ARIA / semantics broken:** restyling that drops `aria-hidden` on a decorative SVG, removes an icon control's `aria-label`/`title`, breaks the `role="status" aria-live` form region, shrinks a 44px tap target below threshold (WCAG 2.5.5/2.5.8), or introduces a second `<h1>` (the index page relies on a visually-hidden `<h1 class="pfg-sr-only">` while the theme `h1.site-title` is hidden via CSS — restyling the logo could expose the duplicate).

**Why it happens:**
The a11y wins are encoded in tokens and scoped rules that look like ordinary styling, so a polish edit overwrites them without realizing they were load-bearing. `outline:none` is a near-universal reflex. Contrast and motion regressions are invisible without measurement.

**How to avoid:**
- **Never** write a bare `:focus { outline:none }`. If you restyle focus, replace it with an equal-or-better visible indicator (`:focus-visible` outline / ring) on the same element. Make "visible keyboard focus on every interactive element" a hard line in the UI design contract.
- Use **only** the contrast-verified tokens for text: `--pfg-gold-ink` for gold-colored text on light, `--pfg-ink` for body. Keep the gold **fill** `#ecab23` for backgrounds/borders, never for small text on white. Re-measure contrast (axe/Lighthouse, DOM-measured) for any text-color or background change.
- Any new decorative motion goes **into** the existing scoped `prefers-reduced-motion` block; brand-identity motion (Swiper/marquee/GSAP) stays out of it. Don't reintroduce a universal motion killer (it was deliberately removed — `custom.css:315-331`, commit `830a769`).
- Preserve existing ARIA/semantic patterns: don't strip `aria-hidden`/`aria-label`/`role`/`aria-live`, keep exactly one `<h1>` per page, keep 44px hit zones. Idempotent JS a11y patches in `custom.js` must keep their guards.
- Re-run axe/Lighthouse on every touched page and confirm **0 new violations** (the project's standing target). The one accepted exception is the documented mobile header search tap-target (`custom.css:141-151`) — confirm a flag matches that before accepting it.

**Warning signs:**
- `outline:none` / `outline:0` appears in a diff.
- New `color`/`background`/`opacity` on text without a recorded contrast ratio in the comment.
- New `transition`/`animation`/`transform` outside the reduced-motion block.
- axe/Lighthouse a11y score drops vs. baseline on any page.

**Phase to address:**
Every implementation phase (a11y-floor is a gate, not a phase). Audit phase establishes the baseline score per page to compare against.

---

### Pitfall 5: Responsive breakage — looks right on desktop, breaks on tablet/mobile

**What goes wrong:**
A change tuned on a 1440 desktop breaks narrow viewports: a fixed `width`/`min-width` in px causes horizontal scroll; large headings or long Russian words overflow or wrap brutally; a `white-space:nowrap` or wide padding pushes content past the viewport; a tap target that's fine with a mouse drops below 44px on touch; a newly "sticky"/`position:fixed` element overlaps the header or off-canvas menu. The theme also has its own `responsive.css` media queries the custom layer must out-specify at the *same* breakpoints (the override at `custom.css:651-652` already cites `responsive.css:145`), so a desktop-only edit can be overridden — or override — unexpectedly below 1200px.

**Why it happens:**
Desktop is where the work is done and reviewed. The theme's mobile behavior (off-canvas menu, stacked grids) is delicate and easy to disturb. Cyrillic text has different wrapping/length characteristics than the theme's original Latin demo content.

**How to avoid:**
- Avoid fixed px widths on content; use `max-width`, `%`, `clamp()`, `min()`/`max()`, and `gap`. Let text wrap naturally; for long Russian words use `overflow-wrap:break-word` / `hyphens` rather than `white-space:nowrap`.
- Respect the off-canvas gate: no `filter`/`backdrop-filter`/`transform` on ancestors of the mobile menu (≤1200px); the glass header stays `min-width:1201px` only.
- New sticky/fixed elements (e.g. the WhatsApp float) must be checked for overlap with header and off-canvas menu at every breakpoint and must not cover content or tap targets.
- Touch targets ≥44px on mobile specifically (mouse-fine ≠ touch-fine).
- **Test the project's standard breakpoints every time:** 1440 / 1024 / 768 / 390 / 360 (spacing audits use 1440 / 768 / 390). Confirm `document.documentElement.scrollWidth` ≤ viewport (no horizontal scroll) and no clipped headings — DOM-measured, per `TESTING.md`.

**Warning signs:**
- Horizontal scrollbar appears at 768/390/360.
- A heading clips or a word overflows its container on mobile.
- A change only verified at one width.
- `white-space:nowrap` or a px `width`/`min-width` in a diff that targets content.

**Phase to address:**
Every implementation phase. Multi-breakpoint Playwright check (incl. no-horizontal-scroll DOM assertion) is a required verification step.

---

### Pitfall 6: Performance / CLS regressions from polish

**What goes wrong:**
- **Webfont CLS/FOUT:** Be Vietnam Pro + Plus Jakarta Sans load from Google Fonts (external). Without `font-display: swap` and a metric-matched fallback, late font arrival shifts layout (CLS) or hides text (FOIT). Adding *more* font weights/families for "polish" worsens this and adds render-blocking requests.
- **Image CLS:** below-fold or hero images without explicit `width`/`height` (or `aspect-ratio`) shift content as they load; the repo's ~6.9 MB of un-optimized PNG/JPG (no WebP) makes this worse and slows LCP.
- **Animation jank / layout thrash:** animating `width`/`height`/`top`/`left`/`box-shadow` instead of `transform`/`opacity` forces layout/paint on every frame; heavy `backdrop-filter` on large areas drops scroll FPS.
- **Dead weight confusion:** `js/chart.js` (208 KB) sits in the repo unused by any page (not in the 18 script tags). It isn't shipped, but it invites someone to "wire it up" or wastes review time. (Deleting a vendor file is out of scope this milestone unless promoted.)

**Why it happens:**
Fonts/animations are the easy reach for "premium feel." CLS and thrash are invisible without measurement; they don't show on a fast local `file://` load. The unused 208 KB looks like a quick win but lives in read-only vendor territory.

**How to avoid:**
- Don't add font families/weights for polish. Keep `font-display: swap` on the existing faces, and rely on the metric-matched system fallback so swap doesn't shift layout. Preload only the one or two faces actually used above the fold; don't add render-blocking font CSS. *(Confidence MEDIUM on exact preload set — verify against actual `<head>` font links and Lighthouse before changing.)*
- Animate only `transform`/`opacity`; keep `will-change` minimal and scoped; avoid large-area `backdrop-filter` (already gated to desktop header).
- For any image you touch, set explicit `width`/`height` or `aspect-ratio` and `loading="lazy"` below the fold. Image format conversion to WebP is a separate optimization milestone — don't smuggle it into a visual-polish phase.
- Don't reference `chart.js`; leave it (read-only vendor, deletion is its own scoped decision).
- Measure CLS / LCP in Lighthouse on a throttled profile, not just eyeball a local load.

**Warning signs:**
- New `@font-face`/Google Fonts family or extra weights in a diff.
- CLS in Lighthouse rises vs. baseline; text flashes/reflows on load.
- An animation targets layout properties (`width`, `top`, `margin`) instead of `transform`.
- An `<img>` added/edited without `width`/`height`.

**Phase to address:**
Audit phase (record baseline CLS/LCP per page, inventory font requests). Any phase adding imagery/motion/fonts guards CLS. Payload/image/dead-code optimization is explicitly a **separate future milestone** (per PROJECT.md), not this one.

---

### Pitfall 7: Cross-browser / font-rendering gotchas

**What goes wrong:**
- **FOUT/FOIT divergence:** Safari historically blocks text up to 3s on slow fonts (FOIT) while Chrome swaps; without `font-display:swap` the site looks different (and worse) per browser. Google Fonts outage/blocking (some regions) leaves text in an unstyled fallback — fine only if the fallback is metric-matched.
- **Icon-font fallback:** the theme uses FontAwesome + `pbminfotech-base-icons` icon fonts. If an icon font fails or is subset wrong, glyphs render as tofu boxes or the wrong character. Restyling icon containers can clip glyphs (line-height/overflow).
- **Cyrillic transform bug:** the theme's `text-transform:capitalize/uppercase` mangles Russian (capitalizing prepositions "В"/"И"). The fix is `text-transform:none` relying on already-correct source case (`custom.css:215-218, 243-258, 865-873`). A new component that inherits a theme transform reintroduces the bug.
- **Rendering nits:** `-webkit-font-smoothing`, sub-pixel letter-spacing for Cyrillic, and `backdrop-filter` support differ across browsers.

**Why it happens:**
Local dev is usually one browser (Chrome). Font behavior is the most browser-divergent part of CSS. The Cyrillic transform trap is theme-specific and easy to re-trigger on new elements.

**How to avoid:**
- Keep `font-display:swap` + a metric-matched fallback stack so a font failure degrades gracefully and identically.
- For any new text element, set `text-transform:none` if the theme would otherwise impose a transform on Russian copy; rely on correct source case.
- Don't restyle icon-font containers in ways that clip (`overflow:hidden` + tight line-height). Verify icons still render after container changes.
- Spot-check at least Chrome + one of Safari/Firefox for font rendering and `backdrop-filter` on the polished areas.

**Warning signs:**
- Russian text shows capitalized prepositions ("В", "И", "На") — a transform leaked in.
- Tofu boxes / wrong glyphs where icons should be.
- Text invisible for a beat on first load (FOIT) in Safari.

**Phase to address:**
Any phase touching typography, buttons, eyebrows, or icon components. Cross-browser font check in verification.

---

### Pitfall 8: Scope creep — "polish" mutating into content/logic rewrites

**What goes wrong:**
A visual task drifts into rewriting copy, restructuring page content, "improving" the WhatsApp message format, touching analytics/routing, or editing JSON-LD — all explicitly **out of scope** and a hard customer constraint. Each looks like a small adjacent improvement; together they risk the conversion path and the agreed boundary, and they're exactly the changes the customer said not to make.

**Why it happens:**
While restyling a block you notice the copy could be tighter or the form flow "smoother," and the edit is one line away. The audit-first rule exists precisely to resist this.

**How to avoid:**
- The UI design contract defines the allowed surface: spacing scale, type scale, color/states, component styling — **visual only**. Copy, message strings, form behavior, analytics, routing, JSON-LD are off-limits; if a wording/logic problem is found, log it as a separate backlog item, don't fix it inline.
- Honor audit-first: no code change before an approved plan + design contract (PROJECT.md Key Decision).
- Behavior-diff guard: after a change, confirm forms still open `wa.me` with the same assembled message, analytics still fire, routes/links unchanged, JSON-LD byte-identical unless the task is explicitly about it.

**Warning signs:**
- A diff touches `WA_NUMBER`, the message-assembly code, `application/ld+json`, analytics snippets, or page prose.
- A "while I'm here" content edit.
- The change can't be expressed purely in `custom.css`/`base.css` + presentational `custom.js`.

**Phase to address:**
Audit phase (the design contract draws the line). Every implementation phase verifies "no behavior/content/schema change" before done.

---

### Pitfall 9: Verification gaps — "done" without all 3 viewports + a11y

**What goes wrong:**
A change is declared done after eyeballing `index.html` on desktop. The regressions above (a11y floor, mobile overflow, the stale 1-of-11 page, FOUT, broken slider) are exactly the ones a single-viewport desktop glance misses. With **no automated tests at all**, an unstructured manual check is the only net — and it's the thing most likely to be skipped under time pressure.

**Why it happens:**
No CI, no `npm test`, no snapshot to fail. "Looks fine here" feels like done. The Workflow API proxy that would run audit sub-agents has been failing (HTTP 400, no balance — project memory), so anyone relying on automated agents gets a false sense of coverage.

**How to avoid — structure the Playwright QA so it can't miss these:**
1. **All affected pages × standard breakpoints.** Drive each touched page (and all 11 if shared chrome changed) at **1440 / 1024 / 768 / 390 / 360**.
2. **DOM-measured assertions, not CSS-text trust** (the project's hard-won lesson: *верить DOM-измерению, а не тексту CSS*):
   - `document.documentElement.scrollWidth` ≤ viewport width → no horizontal scroll.
   - `getBoundingClientRect()` on interactive elements ≥ 44px (tap targets).
   - computed `padding`/spacing matches the spacing scale; headings not clipped.
3. **axe / Lighthouse a11y = 0 new violations** vs. recorded baseline, per touched page; any flag must match a documented accepted exception (mobile search tap-target).
4. **JS behavior smoke test** (no auto coverage, so do it by hand): mobile menu open/close/Escape/backdrop, WhatsApp float + number, `.pfg-form` consent-block then `wa.me` message + status line, marquee scrolling, slider working, reduced-motion (brand motion on, micro-interactions off).
5. **Load-order check** after any markup edit: vendor CSS before `custom.css`, vendor JS before `custom.js`.
6. **Multi-page screenshot diff** for shared-chrome changes (catch the stale 1-of-11).
   - Treat critical checks as **manually duplicated** since audit sub-agents can't be trusted (proxy down).

**Warning signs:**
- "Done" with screenshots from only one width or one page.
- Verification cites CSS source ("I set padding to X") instead of measured DOM.
- a11y not re-run after a visual change.
- JS behaviors not exercised after a class/markup edit.

**Phase to address:**
Every phase. This checklist *is* the definition-of-done; bake it into each phase's success criteria and the final UI review.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Add `!important` instead of finding the winning vendor rule | Override "just works" now | Specificity war, unreadable cascade, silent breakage on theme change | Only when a vendor media-query/inline-ish rule genuinely can't be beaten by specificity — and document the vendor file:line beaten |
| Edit shared header/footer on the pages you're looking at | Fast, fewer files open | Stale 1-of-11 page, visual drift, no test catches it | Never ship partial; always change-all-11 + diff |
| Retrofit CSS `@layer` to "fix" overrides mid-milestone | Cleaner override model in theory | Reorders the entire `!important`-based cascade the site currently depends on → mass regression | Only as its own planned milestone with full 11-page re-audit; not in a polish pass |
| Add font weights/families for "premium feel" | Nicer type instantly | Render-blocking requests, FOUT/CLS, cross-browser divergence | Rarely; only with `font-display:swap` + preload + measured CLS, ideally self-hosted |
| Inline `style="..."` for a one-off tweak | Quickest possible fix | Blocks future CSP `style-src`, can't be themed/overridden centrally, drifts across 11 pages | Avoid; put it in `custom.css` (also helps the future CSP goal in CONCERNS) |
| Animate layout properties (`width`/`top`) for an effect | Looks right, easy to reason about | Layout thrash, jank on mobile scroll | Never for scroll/hover loops; use `transform`/`opacity` |
| Wire up the unused `chart.js` | "Free" charting already in repo | Ships 208 KB, vendor read-only, off-scope | Never this milestone; deletion is its own decision |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Swiper | Re-nesting/renaming `swiper-slide`/`swiper-wrapper`; calling `autoplay.stop()/start()` (breaks marquee) | Style via added `.pfg-*` classes only; reach widgets via the polling init pattern (`custom.js:131-146`) |
| AOS | Removing `data-aos*` attrs thinking they're decorative | Leave AOS hooks intact; restyle around them |
| GSAP / ScrollTrigger / SplitText | Stripping a class the theme animates; effects on menu ancestors | Keep animated-element classes; never animate-block ancestors of off-canvas menu |
| Google Fonts | Adding families/weights, no `font-display`, no metric-matched fallback | `swap` + preload above-fold faces + matched fallback; don't add families for polish |
| FontAwesome / pbmit base icons | Clipping icon containers (`overflow:hidden` + tight line-height) | Verify glyphs render after container restyle; keep fallback box sizing |
| WhatsApp lead form (`wa.me`) | "Improving" the message string or flow during a CSS task | Treat message/number/flow as logic — out of scope; only style `.pfg-form`/status |
| JSON-LD / analytics / routing | Editing while restyling adjacent markup | Leave byte-identical unless the task explicitly targets them; behavior-diff before done |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Late-loading webfont shifts layout | Text reflows ~0.5–3s after load; CLS up | `font-display:swap` + metric-matched fallback; preload above-fold face | Slow networks, cold cache, Google Fonts blocked/slow |
| Image without dimensions | Content jumps as image paints | Explicit `width`/`height` or `aspect-ratio`; `loading="lazy"` below fold | Any first visit / slow connection |
| Animating layout props | Scroll/hover jank, dropped frames | Animate `transform`/`opacity` only; minimal scoped `will-change` | Mobile / low-end devices |
| Large-area `backdrop-filter` | Scroll FPS drops, fans spin | Keep gated to small desktop header area (already done) | Mobile, large viewports |
| More render-blocking CSS/JS for polish | Slower FCP/LCP | No new blocking requests; piggyback on existing `custom.css`/`custom.js` | Always, compounds with existing ~760 KB CSS / ~600 KB JS payload |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Adding more inline `style="..."` during polish | Cements need for `style-src 'unsafe-inline'`, blocks a future CSP | Put styles in `custom.css`; don't grow inline-style count (CONCERNS flags this) |
| Introducing an external asset/CDN for a font/icon "upgrade" | Runtime supply-chain exposure (repo is fully self-hosted today) | Keep assets vendored/self-hosted; if external is unavoidable, add SRI |
| Editing form/`wa.me` handling for visual reasons | Could leak/break the only lead path; off-scope logic change | Style only; never touch `WA_NUMBER` or message assembly in a UI task |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Removing visible focus to "clean up" | Keyboard users can't see where they are (WCAG 2.4.7) | Always provide `:focus-visible` ring/outline |
| Gold text on white using brand fill | Low-vision users can't read it (1.4.3) | Use `--pfg-gold-ink` for text; fill gold for backgrounds only |
| Tap target shrinks below 44px on mobile | Mis-taps, frustration on touch | Keep 44px hit zones; verify with `getBoundingClientRect` |
| Motion added without reduced-motion guard | Vestibular discomfort for opted-out users (2.3.3) | Decorative motion goes in the scoped reduced-motion block |
| Conversion blocks (hero/pricing/CTA/form) weakened visually | Lower lead conversion — the site's whole purpose | Treat conversion blocks as highest-priority polish; verify clarity at all breakpoints |
| Russian copy capitalized wrong by theme transform | Looks unprofessional, erodes trust | `text-transform:none` on new text elements |

---

## "Looks Done But Isn't" Checklist

- [ ] **Shared header/footer/CTA edit:** verify the change landed in **all 11** pages (Grep returns 11; multi-page screenshot) — not just the page you edited.
- [ ] **Any visual change:** re-run axe/Lighthouse on touched pages → **0 new** a11y violations vs. baseline.
- [ ] **Focus styles:** every interactive element still shows a visible keyboard focus (no `outline:none` left bare).
- [ ] **Text color/background change:** contrast re-measured and recorded; gold text uses `--pfg-gold-ink`, not `#ecab23`.
- [ ] **New motion:** added to the scoped `prefers-reduced-motion` block; brand motion still runs with reduce-motion on.
- [ ] **Responsive:** checked at 1440/1024/768/390/360 — no horizontal scroll (DOM-measured), no clipped headings/words.
- [ ] **Markup/class edit:** every JS behavior re-exercised (menu, WhatsApp float, form→`wa.me`, marquee, slider) — nothing silently dead.
- [ ] **Load order:** `custom.css` last among CSS, `custom.js` last among JS, on every edited page.
- [ ] **Behavior/content unchanged:** `wa.me` message, `WA_NUMBER`, analytics, routing, JSON-LD byte-identical unless the task explicitly targets them.
- [ ] **Fonts:** no new families/weights; `font-display:swap` intact; no FOUT/CLS regression in Lighthouse.
- [ ] **`!important` budget:** net-new `!important` near zero; each new one cites the vendor rule it beats.

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Stale 1-of-11 page after shared-chrome edit | LOW | Diff the block across 11 files, copy the corrected block to the stragglers, re-screenshot all 11 |
| `!important` escalation tangle | MEDIUM | Identify the colliding rules in DevTools, replace force with specificity, remove redundant `!important`, re-verify all breakpoints |
| Broken theme JS (dead slider/animation) | MEDIUM | Revert the markup/class edit; reapply the visual goal via added `.pfg-*` class + CSS instead of restructuring |
| a11y regression shipped | LOW–MEDIUM | Restore the token/scoped rule (focus, `--pfg-gold-ink`, reduced-motion block, ARIA attr); re-run axe to confirm 0 |
| CLS/FOUT from added font | LOW | Remove the added family/weight, restore `font-display:swap` + fallback, re-measure CLS |
| Mobile overflow from fixed width | LOW | Replace px width with `max-width`/`clamp`/`%`; re-check `scrollWidth` at 390/360 |
| Scope-crept content/logic edit | LOW | Revert the off-scope hunk; refile as a backlog item; keep the diff visual-only |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| `!important` escalation | Audit (catalog) + design contract (budget) + each impl phase | Net-new `!important` count ≈ 0; each cites beaten vendor rule |
| Breaking theme JS | Audit (do-not-touch class/attr list) + each impl phase | JS-behavior smoke test passes after every markup/class edit |
| 1-of-11 visual drift | Any shared-chrome phase | Grep = 11 hits + multi-page screenshot diff |
| A11y regression | Each impl phase (a11y is a gate) | axe/Lighthouse 0 new violations vs. baseline per page |
| Responsive breakage | Each impl phase | DOM-measured: no horizontal scroll, ≥44px targets, no clipped text at 1440/1024/768/390/360 |
| Performance / CLS | Audit (baseline) + any font/image/motion phase | Lighthouse CLS/LCP not worse than baseline |
| Cross-browser / fonts | Any typography/icon phase | Chrome + Safari/Firefox spot-check; no Cyrillic transform leak; icons render |
| Scope creep | Audit (contract draws the line) + each impl phase | Behavior/content/JSON-LD diff = no change |
| Verification gaps | Every phase (definition-of-done) | Full Playwright checklist run, critical checks manually duplicated |

---

## Confidence

| Area | Confidence | Basis |
|------|------------|-------|
| `!important` / specificity, duplication drift, theme-JS hooks, scope, verification | HIGH | Directly grounded in this repo's `CONCERNS.md`, `CONVENTIONS.md`, `TESTING.md`, `PROJECT.md` with file:line references |
| A11y regressions (focus, contrast, motion, ARIA) | HIGH | Established WCAG behavior + the project's own documented tokens/scoped rules and baseline target |
| Responsive breakage | HIGH | Standard responsive CSS behavior + project's documented breakpoints and off-canvas gate |
| Cross-browser / font rendering | MEDIUM–HIGH | Established FOUT/FOIT and Cyrillic-transform behavior; exact current Safari font-block timing not re-verified this pass |
| Performance/CLS specifics (exact preload set, current font-display state) | MEDIUM | General font/CLS behavior is solid; the precise current `<head>` font config should be confirmed against the live `<head>` + a Lighthouse run before changing |

Note: live web searches returned no results in this environment, so external 2025/2026 source citations are not included; findings rest on the codebase map files plus established CSS/WCAG/web-performance behavior. Font/preload specifics flagged MEDIUM should be confirmed against the actual `<head>` and a Lighthouse run during the audit phase.

## Sources

- `.planning/PROJECT.md` — scope, constraints, out-of-scope, key decisions
- `.planning/codebase/CONCERNS.md` — `!important` count, 11-page duplication, payload, unused `chart.js`, specificity wars, no tests
- `.planning/codebase/CONVENTIONS.md` — override strategy, tokens, scoped `prefers-reduced-motion`, a11y conventions, off-canvas filter trap
- `.planning/codebase/TESTING.md` — Playwright + DevTools/Lighthouse/axe QA, standard breakpoints, DOM-measurement lesson, proxy caveat
- Project memory: `ui-audit-2026-06-23.md`, `workflow-api-proxy-balance.md`
- Established CSS cascade, WCAG 2.1/2.2, and web-font-loading behavior (training knowledge; live web search unavailable this session)

---
*Pitfalls research for: vendored-theme static-site UI polish (taxpfg.kz)*
*Researched: 2026-06-25*
