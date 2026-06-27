# Phase 4: Conversion Blocks + Imagery - Research

**Researched:** 2026-06-27
**Domain:** No-build static site (GudFin/PBMIT theme + Bootstrap 5.2 + `pfg-*` override layer); conversion composites (hero polish, net-new pricing, footer parity, imagery sizing, title-bar tier)
**Confidence:** HIGH (every claim grep/Read-verified against the live repo this session)

## Summary

Phase 4 lands five visual-only changes on a frozen, vendored stack: hero polish (CNV-01), a net-new pricing block on services.html (CNV-02), CTA-hierarchy + sticky-collision resolution-by-absence (CNV-03), footer parity across 11 pages (CNV-04), and imagery/title-bar sizing (IMG-01 + T1). Everything composes from Phase-2 tokens and Phase-3 primitives (`.pfg-card`, `.pbmit-btn`, `.pfg-section`, `.pfg-faq`) already verified at 18/18 — there is **no new component primitive** and **no new library** to research. The stack is read-only and no-build; nothing is installed.

The single highest-value finding for the planner: the master/04 contract claims the hero primary CTA is **«Получить консультацию» existing byte-identical**, but the actual hero markup carries three different CTA texts («Наши услуги», «Подробнее», «Подробнее» — `index.html:178/209/240`). «Получить консультацию» lives on services.html/contacts.html, **not** in the hero. Because copy is read-only (VER-04), the planner cannot retext the hero CTA to «Получить консультацию» without breaking VER-04. CNV-01 must be read as "exactly one CTA per hero slide (already true) + lh/visual polish", not "rename the hero CTA". This is flagged as Assumption A1 and Open Question 1.

**Primary recommendation:** Insert the pricing block on services.html between the existing "Получить консультацию" CTA section (closes `services.html:450`) and the FAQ comment (`services.html:452`), built as a `.pfg-grid` of three `.pfg-card` tier variants with per-tier `<a class="pbmit-btn" href="https://wa.me/77072370050">` CTAs (reusing the existing direct-link WhatsApp pattern, no JS). Footer parity is **CSS-only** (markup divergence is per-page `.active` nav state + two content strings, which are legitimate and must NOT be flattened). Title-bar T1 and imagery IMG-01 are pure `custom.css` overrides with zero new `!important`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Pricing-блок CNV-02 (net-new, на сайте отсутствует)**
- Разместить на **services.html** (после hero/услуг, перед FAQ) — единственное логичное место.
- Структура: 3 пакета (напр. ИП-старт / ТОО-стандарт / Премиум), ровно один «популярный» highlight, per-tier CTA.
- Контент цен: БЕЗ конкретных цифр — формулировки про объём услуг; цена «от X ₸» или «по запросу» → CTA. (Точные цены не задавать — риск устаревания, бизнес не подтвердил тарифы.)
- CTA тарифа → тот же WhatsApp-flow (паттерн «Получить консультацию», VER-04 — не новая логика, переиспользовать существующий механизм формы/ссылки).
- pricing — page-specific (только services.html) → НЕ shared chrome → НЕ change-all-11.

**Hero + sticky-CTA коллизия (CNV-01, CNV-03)**
- Hero CNV-01: полировать существующий — value-prop + единственный primary CTA + trust-сигналы выше сгиба; чинит HE1/HE2 (hero line-height; height/LCP — visual, perf не gate).
- **Sticky mobile CTA НЕ существует на сайте** (grep подтвердил). CNV-03 коллизия sticky-CTA↔WhatsApp-float физически отсутствует.
- CNV-03 разрешение: НЕ создавать net-new sticky-CTA. Задокументировать отсутствие; `.pfg-whatsapp-float` (js/custom.js:58-60) — единственный плавающий элемент, ничего не перекрывает. JS-правки в этой фазе НЕ требуются.
- CTA-иерархия по сайту: единая через токены/компоненты Фазы 3 (один заметный primary на экран).

**Footer-паритет + imagery (CNV-04, IMG-01)**
- Footer CNV-04: унифицировать вид на 11/11; FT3 vertical density на mobile (low-priority). Если markup трогается — change-all-11 атомарно.
- IMG-01: presentation/sizing ONLY (object-fit, корректные пропорции, нет искажений/визуального мусора) на существующие 12 `<img>` + CSS-bg. WebP/AVIF/srcset bulk re-encode = v2/PERF-01 OUT-OF-SCOPE.
- T1 title-bar: добавить min-height tier между 768 и 390 (550px band fix на 768).

**change-all-11 дисциплина и verify**
- Footer markup-правки — атомарно во все 11 HTML (grep=11), один коммит.
- Pricing — только services.html → не change-all-11.
- !important бюджет: net-new ≈ 0 (floor 59); каждый новый — с русским комментарием о vendor-правиле.
- Verify: Playwright DOM @ 1440/1024/768/390/360 + axe + VER-04 JS-smoke против AUD-01 floor (a11y≥95, axe=0); pricing CTA→WhatsApp работает (тот же flow); footer-паритет на 11.

### Claude's Discretion
- Точные названия/состав 3 тарифов и формулировки (русский sentence case, осмысленно для бухгалтерско-налоговых услуг).
- Какие trust-сигналы поднять в hero выше сгиба (из существующего контента).
- Конкретные object-fit/sizing значения для imagery.

### Deferred Ideas (OUT OF SCOPE)
- WebP/AVIF/srcset image re-encode — v2/PERF-01.
- Точные цены тарифов — ждут подтверждения бизнеса (пока «по запросу»).
- Финальный a11y pass + cross-device verification + before/after — Phase 5.
- chart.js removal, font-loading opt, header/footer templating — v2.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CNV-01 | Hero: value-prop + единственный primary CTA + trust выше сгиба | §CNV-01 Hero — current structure mapped; exactly 1 CTA/slide already present; lh policy from Phase 2 confirmed at `custom.css:523-531`; CTA-text discrepancy flagged (A1/OQ1) |
| CNV-02 | Pricing: 3 tiers, ровно 1 «популярный» highlight, per-tier CTA | §CNV-02 Pricing — exact insertion point `services.html:450↔452`; compose `.pfg-grid`+`.pfg-card`+`.pbmit-btn`; WhatsApp via existing direct link pattern, no JS |
| CNV-03 | CTA hierarchy; sticky-CTA↔whatsapp collision resolved/absent | §CNV-03 — grep confirms only `.pfg-whatsapp-float` (`custom.css:25`) + vendor off-canvas are `fixed`; zero sticky CTA → no collision; JS untouched |
| CNV-04 | Footer unified, credibility, identical on 11 | §CNV-04 Footer — all 11 carry `.site-footer`; divergence is per-page `.active` + 2 content strings; CSS-only parity recommended |
| IMG-01 | Imagery/icons: single style, sizes, proportions, no junk | §IMG-01 — 12 `<img>` inventory; no `object-fit`/`aspect-ratio` in custom.css today; presentation-only sizing, no re-encode |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Hero polish (CNV-01) | Custom CSS override (`custom.css` §9.7) | HTML (read-only copy) | lh/visual is cascade-override; copy byte-identical (VER-04) |
| Pricing block (CNV-02) | HTML markup (services.html, net-new) | Custom CSS (`.pfg-card` variant) | New presentation markup + tier styling; page-specific, not chrome |
| Pricing CTA → WhatsApp (CNV-02) | HTML `<a href="wa.me/…">` (existing pattern) | — | Reuse direct-link mechanism; **no `js/custom.js` edit** |
| CTA hierarchy / sticky (CNV-03) | Documentation (resolution by absence) | Custom CSS (button hierarchy already in Phase 3) | No sticky CTA exists; nothing to build |
| Footer parity (CNV-04) | Custom CSS override | HTML ×11 (only if markup truly needed) | Appearance unifies via CSS; markup divergence is legitimate state |
| Imagery sizing (IMG-01) | Custom CSS (`object-fit`/`aspect-ratio`) | — | Presentation-only; assets untouched (no re-encode) |
| Title-bar tier (T1) | Custom CSS media-query override | — | Beats `shortcode.css:4932-4934` 550px by source-order |

## Standard Stack

**Not applicable.** No-build static site; the stack is frozen and vendor-read-only (master §Design System). No component library or registry to choose, nothing to install. Editable surface is exactly three files: `css/custom.css` (primary this phase), `css/base.css` (not needed this phase), `js/custom.js` (**not edited** — CNV-03 resolved by absence). All other `css/*` / `js/*` are theme-owned read-only.

Phase-4 builds **only** by:
1. Cascade override in `custom.css` (loaded last — `index.html:54`).
2. Net-new HTML markup on services.html (pricing) composing existing `.pfg-*` / `.pbmit-*` classes.

## Package Legitimacy Audit

**Not applicable.** Zero external packages installed or referenced this phase. No `package.json`, no lockfile, no registry. All libraries are vendored and read-only. Nothing to audit.

## Architecture Patterns

### System Architecture Diagram

```
                         services.html  (page-specific edits)
                              │
   ┌──────────────────────────┼────────────────────────────────────┐
   │ <main id="content">       │                                     │
   │   ├─ .pfg-section (hero/intro)                                  │
   │   ├─ .service-section-one  (5 pbmit-service cards)              │
   │   ├─ .pfg-section--alt      (отчётность list)                   │
   │   ├─ .pfg-section           (доп. услуги — 4 .pfg-card)         │
   │   ├─ .pfg-section--alt       (CTA «Получить консультацию») ◄─ closes :450
   │   │                                                             │
   │   ├─ ★ NET-NEW pricing .pfg-section  ◄── INSERT HERE (450↔452) │
   │   │     └─ .pfg-grid                                            │
   │   │          ├─ .pfg-card  (tier 1, secondary CTA)             │
   │   │          ├─ .pfg-card.pfg-pricing--popular (gold, primary) │
   │   │          └─ .pfg-card  (tier 3, secondary CTA)             │
   │   │               each CTA → <a href="wa.me/77072370050">      │
   │   │                                                             │
   │   └─ .pfg-faq-section  (Phase-3 FAQ — :456)                    │
   └─────────────────────────────────────────────────────────────────┘

   css/custom.css (loaded LAST, wins by source-order)
     ├─ §9.0 tokens  →  --pfg-space-* / --pfg-fs-* / --pfg-gold / --pfg-card
     ├─ §9.7 hero lh (HE1/G2)        ── extend for CNV-01 polish
     ├─ §9.8 .pfg-card lift          ── reuse for pricing tiers
     ├─ §scoped reduced-motion (377) ── add pricing-card hover here
     ├─ §12.7 title-bar mobile (990) ── add 768→576 tier (T1) here
     └─ NEW: pricing tiers, footer density (FT3), img object-fit (IMG-01)

   js/custom.js  ── BYTE-IDENTICAL this phase (VER-04). wa.me direct links only.
```

### Recommended Project Structure

No new files. Append-only edits inside the existing layered `custom.css` (follow the numbered "ЭТАП N" banner-comment convention) and net-new markup inside `services.html` `<main>`.

### Pattern 1: Pricing tier = `.pfg-card` composite (CNV-02)

**What:** Three `.pfg-card` in a `.pfg-grid`; one carries a modifier class for the gold highlight; each has its own `.pbmit-btn` CTA.
**When to use:** The net-new pricing block — this is the entire CNV-02 build.
**Why this shape:** `.pfg-card` already provides `height:100%`, hairline, soft shadow, hover-lift (`custom.css:72, 545-557`); `.pfg-grid` already declares `align-items:stretch` + `repeat(auto-fit,minmax(260px,1fr))` (`custom.css:74, 1147`) so same-row tiers are equal-height for free (master C2). No new layout primitive needed.

```html
<!-- Source: composes services.html:401-418 (.pfg-grid + .pfg-card) + :431-439 (.pbmit-btn) -->
<section class="pfg-section pfg-pricing-section">
  <div class="container">
    <div class="pbmit-heading-subheading">
      <p class="pbmit-subtitle">Тарифы</p>
      <h2 class="pbmit-title">Пакеты бухгалтерского сопровождения</h2>
    </div>
    <div class="pfg-grid pfg-pricing">
      <div class="pfg-card pfg-pricing-tier">
        <h3>ИП на упрощёнке</h3>
        <p class="pfg-pricing-price">от … ₸ / мес</p>
        <ul>…объём услуг…</ul>
        <a href="https://wa.me/77072370050" class="pbmit-btn white" target="_blank" rel="noopener">
          <span class="pbmit-button-content-wrapper"><span class="pbmit-button-text-wrap"><span class="pbmit-button-text"><span>Получить консультацию</span></span></span></span>
        </a>
      </div>
      <div class="pfg-card pfg-pricing-tier pfg-pricing-tier--popular">
        <span class="pfg-pricing-badge">Популярный</span>
        <h3>ТОО на общем режиме</h3>
        <p class="pfg-pricing-price">от … ₸ / мес</p>
        <ul>…объём услуг…</ul>
        <a href="https://wa.me/77072370050" class="pbmit-btn" target="_blank" rel="noopener">
          <span class="pbmit-button-content-wrapper"><span class="pbmit-button-text-wrap"><span class="pbmit-button-text"><span>Получить консультацию</span></span></span></span>
        </a>
      </div>
      <div class="pfg-card pfg-pricing-tier">
        <h3>Премиум / по запросу</h3>
        <p class="pfg-pricing-price">по запросу</p>
        <ul>…объём услуг…</ul>
        <a href="https://wa.me/77072370050" class="pbmit-btn white" target="_blank" rel="noopener">
          <span class="pbmit-button-content-wrapper"><span class="pbmit-button-text-wrap"><span class="pbmit-button-text"><span>Получить консультацию</span></span></span></span>
        </a>
      </div>
    </div>
  </div>
</section>
```

Notes on button hierarchy: bare `.pbmit-btn` is the gold-fill primary (theme default); `.pbmit-btn white` is the secondary/light variant used on the sibling tiers (matches the existing services.html CTA pattern at `:431` primary vs `:440` `white`). This keeps exactly one prominent primary on the highlight tier (master CMP-01).

### Pattern 2: WhatsApp CTA via existing direct-link (CNV-02, no JS)

**What:** Pricing CTAs are plain `<a href="https://wa.me/77072370050" target="_blank" rel="noopener">` — the *direct-link* arm of the existing WhatsApp pattern, **not** the form arm.
**When to use:** Every per-tier pricing CTA.
**Why:** The site has two WhatsApp mechanisms and the per-tier CTA must use the no-JS one:

| Mechanism | Trigger | Where | Phase-4 use |
|-----------|---------|-------|-------------|
| Direct link | `<a href="wa.me/77072370050">` | `index.html:87`, `services.html:440`, `contacts.html` secondary CTA, `.pfg-whatsapp-float` (built in JS but a plain anchor) | **Pricing tier CTAs use this** — zero JS, byte-identical behavior |
| Form → prefilled chat | `.pfg-form` submit → `initLeadForm` builds `wa.me/…?text=encodeURIComponent(...)` | `js/custom.js:72-111`, contacts.html form only | **Not used by pricing** — would require a form; out of scope |

Using the direct-link arm means `js/custom.js` stays byte-identical (VER-04) and no new logic ships. `WA_NUMBER` = `77072370050` (confirmed `js/custom.js:61,101` and 6 markup occurrences).

### Pattern 3: Title-bar min-height tier (T1)

**What:** Add a tablet tier between the vendor 550px (`shortcode.css:4932-4934`) and the existing ≤575px collapse (`custom.css:990-1006`).
**Why:** Vendor sets `.pbmit-title-bar-wrapper, .pbmit-title-bar-content { min-height:550px }`. custom.css only overrides at `max-width:575px` (→ `min-height:auto` + content `200px`). So **768px still renders the full 550px band** — exactly the T1 finding. Add a `@media (max-width:768px)` (and optionally a 992px step) override that reduces the band, mirroring the existing `!important`-cited pattern at `custom.css:990` but for the tablet tier. Override the same two selectors by source-order; the existing rule already uses `!important` to beat the vendor `min-height`, so the new tier likely also needs `!important` on `min-height` — **cite `shortcode.css:4934` in a Russian comment** (this is the one plausible net-new `!important` this phase; see budget section).

### Anti-Patterns to Avoid

- **Flattening footer markup to byte-identical across 11.** The footer differs *legitimately* by per-page `.active` nav state (`<li class="active">` marks the current page) and two intentional content strings. Removing `.active` would break the "you are here" affordance and regress nav semantics. CNV-04 means *visual* parity, achievable in CSS — do **not** force markup equality. (See §CNV-04.)
- **Retexting the hero CTA to «Получить консультацию».** Copy is read-only (VER-04). The hero CTAs are «Наши услуги»/«Подробнее»×2. Changing them violates VER-04. (See A1/OQ1.)
- **Adding a sticky mobile CTA bar.** None exists; building one then "resolving" a collision fabricates work and adds a `fixed` element that *would* overlap `.pfg-whatsapp-float`. CNV-03 is satisfied by documenting absence.
- **Touching `js/custom.js`.** Expect `git diff HEAD js/custom.js` empty. The marquee `params.speed` poll and form flow are fragile vendor-coupled code — no reason to enter the file.
- **`filter`/`transform`/`backdrop-filter` on off-canvas ancestors.** Pricing/footer live outside the header, so this is low-risk, but card hover uses `transform: translateY` — that is on `.pfg-card` itself (a leaf), already safe per Phase-3 precedent (`custom.css:553`).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Equal-height pricing tiers | JS height-matching / manual `min-height` | `.pfg-grid{align-items:stretch}` + `.pfg-card{height:100%}` | Already declared (`custom.css:1147, 72`); CSS grid stretches the row for free (master C2 finding) |
| Pricing card hover lift | New transition rules | Reuse `.pfg-card:hover{transform:translateY(-4px)}` (`custom.css:553`) + its reduced-motion entry | Pattern + reduced-motion gating already exist; just ensure the tier inherits `.pfg-card` |
| Accordion/FAQ near pricing | Anything | Already shipped: `.pfg-faq` native `<details>` (`services.html:456`) | Phase 3 built it; pricing sits *before* it |
| WhatsApp CTA wiring | New JS handler | `<a href="wa.me/77072370050">` direct link | Existing mechanism; no JS edit keeps VER-04 |
| Focus ring on tier CTAs | New `:focus-visible` | Inherited `a:focus-visible{outline:2px solid var(--pfg-gold)}` (`custom.css:351`) | `.pbmit-btn` is an `<a>`; ring already applies |

**Key insight:** Phase 4 is composition, not construction. Every primitive (card, grid, button, focus ring, hover, reduced-motion block, FAQ) already exists and is verified. The only genuinely new artifacts are: (1) pricing markup on one page, (2) a handful of `.pfg-pricing-*` styling rules, (3) a title-bar media tier, (4) image `object-fit` rules, (5) optional footer-density tweaks.

## Runtime State Inventory

Not a rename/refactor/migration phase — presentation-only edits to CSS + net-new markup. No stored data, service config, OS-registered state, secrets, or build artifacts are affected.
- **Stored data:** None — static site, no datastore.
- **Live service config:** None.
- **OS-registered state:** None.
- **Secrets/env vars:** None — WhatsApp number is public, hardcoded in markup/JS already.
- **Build artifacts:** None — no build step exists.

## Common Pitfalls

### Pitfall 1: Hero CTA text mismatch breaks the contract literally
**What goes wrong:** Planner reads "Hero primary CTA: «Получить консультацию» (existing, byte-identical)" and tries to make the hero say that.
**Why it happens:** The contract conflates the *site-wide* primary-CTA copy with the *hero* CTA. The hero actually says «Наши услуги»/«Подробнее».
**How to avoid:** Treat CNV-01 as "exactly one CTA per hero slide (already satisfied) + lh/visual polish." Do not retext. If business wants «Получить консультацию» in the hero, that is a copy change → defer/escalate (VER-04 forbids it this milestone).
**Warning signs:** Any task touching `index.html:178/209/240` text.

### Pitfall 2: Malformed hero heading tag
**What goes wrong:** `index.html:169` opens `<h2 class="pbmit-slider-title …>` but `:171` closes `</h1>`. Slides 2 and 3 correctly open+close `<h2>`. A naive "fix the tag" edit risks changing heading semantics or the visually-hidden-H1 invariant (master: index uses a `.pfg-sr-only` `<h1>`, slider uses `<h2>`).
**Why it happens:** Pre-existing theme/markup typo.
**How to avoid:** Phase 4 is CSS-led; do **not** open this can unless verification flags an a11y regression. If touched, the close tag should become `</h2>` to match the open — but only as a deliberate, tested change (it is markup, currently editable, but axe baseline is already 0 so it is not surfacing as a violation). Flag, don't silently rewrite.
**Warning signs:** Heading-order axe rule appearing on index.

### Pitfall 3: DOM-vs-CSS discrepancy on tap targets / heights
**What goes wrong:** Trusting `custom.css` source text over the rendered box (the FT1 history — `custom.css` claimed a 44px footer hit-zone the live render didn't apply, AUD-02 Pitfall 5).
**How to avoid:** Verify every sizing claim (title-bar tier, pricing card height, footer density) with Playwright `getBoundingClientRect` at the five viewports, not by reading CSS.
**Warning signs:** "It should be X because the CSS says X."

### Pitfall 4: `!important` budget creep from comment prose
**What goes wrong:** `grep -c '!important'` counts the literal string in Russian comments. Phase 3 spiked to 62 because three comments contained the words "без !important" (03-02-SUMMARY Issues).
**How to avoid:** When writing the required Russian comment citing a beaten vendor rule, phrase it as "без important-флага" (no literal `!important`). Target floor stays **59**; net-new functional declarations ≈ 0 (the title-bar tier is the only likely exception — cite it).

### Pitfall 5: Serving over file:// hides font/asset/measurement reality
**What goes wrong:** Auditing via `file://` breaks relative paths, Google Fonts `@import`, and the Maps iframe; measurements become wrong (AUD-02 method note).
**How to avoid:** Always `python -m http.server 8080 --bind 127.0.0.1` from repo root and audit `http://127.0.0.1:8080/<page>`.

## Code Examples

### Pricing styling (compose tokens; no hardcoded hex/px)
```css
/* Source: composes custom.css §9.0 tokens + §9.8 .pfg-card */
/* ЭТАП 15 — CNV-02 pricing (services.html only, не shared chrome). */
.pfg-pricing-tier{ display:flex; flex-direction:column; gap:var(--pfg-space-4); }
.pfg-pricing-tier .pbmit-btn{ margin-top:auto; }            /* CTA прижат к низу — ровный ряд */
.pfg-pricing-price{ font-size:var(--pfg-fs-h4); font-weight:600; color:var(--pfg-ink); }
.pfg-pricing-tier--popular{
  border-color: var(--pfg-gold);                            /* единственный gold highlight (master reserved-for) */
  box-shadow: var(--pfg-shadow-md);
}
.pfg-pricing-badge{
  align-self:flex-start; background:var(--pfg-gold); color:#1b1b1b;   /* текст-на-золоте держит AA */
  font-size:var(--pfg-fs-label); padding:var(--pfg-space-1) var(--pfg-space-3);
  border-radius:var(--pfg-radius-sm); text-transform:none;  /* русский sentence case */
}
```

### Title-bar tablet tier (T1) — the one likely net-new !important
```css
/* Source: beats shortcode.css:4934 (.pbmit-title-bar-wrapper,.pbmit-title-bar-content{min-height:550px}) */
/* T1 (AUD-02): 550px полоса непропорциональна для одной строки на планшете.
   Вендор задаёт min-height:550px; добавляем тир 768→576 между desktop и существующим
   мобильным коллапсом (custom.css:990, ≤575px). important — иначе vendor min-height
   (та же специфичность 0,2,0) выигрывает source-order при равенстве. */
@media (max-width:768px){
  .pbmit-title-bar-wrapper,
  .pbmit-title-bar-content{ min-height: 360px !important; }
  .pbmit-title-bar-content{ padding: 110px 0 36px; }
}
```

### Imagery sizing (IMG-01, presentation-only)
```css
/* Source: index.html 12 <img>; AUD-02 I1 (about-01.jpg 900×1000 → ~300px box, no distortion) */
/* IMG-01: единый object-fit для фото-блоков, чтобы пропорции не «прыгали».
   Только presentation — ассеты не перекодируем (re-encode = v2/PERF-01). */
.pbmit-featured-wrapper img,
.pbmit-ihbox-img img{ width:100%; height:100%; object-fit:cover; display:block; }
```
(Planner: confirm the exact wrapper selectors against the live render before locking — the `<img>` containers are theme-owned; target the wrapper, not bare `img`, to avoid catching logo/icon images.)

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Original imp-plan: CNV-03 = JS spike to resolve sticky-CTA↔float collision (`01-IMPL` Phase-4 row) | CNV-03 = documented absence; **no JS edit** | 04-CONTEXT (2026-06-27) | Removes the only JS task; `js/custom.js` byte-identical |
| Pricing imagined as possibly "v1/placeholder" | NET-NEW, build in full, no scope-reducing framing | 01-IMPL Net-new table | Plan must deliver complete 3-tier block |

**Deprecated/outdated:**
- `01-IMPLEMENTATION.md` Phase-4 row mentioning a `js/custom.js` "sticky-CTA collision resolution" — **superseded** by 04-CONTEXT documented-absence finding. Do not action it.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Hero CNV-01 = "1 CTA/slide (already true) + lh/visual polish", NOT retexting hero CTA to «Получить консультацию» (which is not the existing hero text) | CNV-01, Pitfall 1 | If business actually wants the hero retexted, that is a VER-04 copy change → must escalate, not silently do |
| A2 | Footer "parity" = visual unification via CSS; per-page `.active` + 2 content strings are legitimate and stay | CNV-04 | If contract intends literal markup equality, planner must reconcile (would strip nav "active" state — not recommended) |
| A3 | Pricing prices stay «от … ₸» / «по запросу» (no figures) — locked decision, but actual числа unknown | CNV-02 | Low — explicitly deferred to v2 pending business confirmation |
| A4 | Title-bar tablet tier needs one net-new `!important` (cited) to beat vendor `min-height:550px` | T1, !important budget | Low — if a non-`!important` selector wins, even better; verify rendered box |
| A5 | Imagery wrapper selectors for `object-fit` target theme wrappers; exact selector to be confirmed against live DOM | IMG-01 | Medium — wrong selector could distort logos/icons; verify before locking |

## Open Questions (RESOLVED)

1. **Hero CTA copy vs contract**
   - What we know: Hero markup says «Наши услуги»/«Подробнее»×2 (`index.html:178/209/240`); contract says hero primary CTA is «Получить консультацию» "existing byte-identical" — but that string is on services/contacts, not the hero.
   - What's unclear: Whether CNV-01 expects a (forbidden) retext or just visual polish.
   - Recommendation: Treat as visual polish only (A1). If a stakeholder wants the hero CTA reworded, raise it as an explicit copy-change request outside VER-04. Planner should add a `checkpoint:human-verify` if it intends any hero text change.
   - **RESOLVED:** locked by CONTEXT decision A1 (hero = visual polish only, copy read-only VER-04); encoded in plan 04-02 (guards `git diff index.html` empty, refuses retext).

2. **Footer content divergence — normalize or preserve?**
   - What we know: Two intentional-looking string differences exist beyond `.active`: (a) recovery-service label — 8 pages say «Восстановление учёта», others say the full «Восстановление и наведение порядка в учёте»; (b) the footer CTA heading — 10 pages «Обсудим!», contacts.html «Обсудить сотрудничество.».
   - What's unclear: Whether these are bugs (should be unified for credibility/parity) or deliberate.
   - Recommendation: If CNV-04 markup is opened anyway, unify the recovery label to one string across 11 (change-all-11, one commit) for credibility; leave `.active` per-page. The CTA-heading variance is copy → treat as read-only unless flagged. Confirm with stakeholder before editing copy.
   - **RESOLVED:** plan 04-03 keeps footer CSS-only (no markup flatten); the two copy strings are preserved as read-only (not treated as bugs this phase). Copy-unification deferred to an explicit stakeholder request — out of scope for CSS-only footer parity.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python (http.server) | Local serving for DOM-accurate audit | ✓ (used in Phase 1) | `python -m http.server` | any static server |
| Playwright | DOM measurement @5vp + JS smoke | ✓ (used Phases 1/3) | from prior phases | — |
| `@axe-core/playwright` | a11y regression gate (axe=0) | ✓ | 4.12.1 (AUD-01) | — |
| Lighthouse | a11y score floor (≥95) | ✓ | 13.4.0 (AUD-01) | — |

**Missing dependencies with no fallback:** None.
**Missing dependencies with fallback:** None — verification toolchain is the same one used in Phases 1 and 3.

## Validation Architecture

> `nyquist_validation` not explicitly false in config → treated as enabled. This site has no unit-test framework (no `package.json`); validation is **DOM-measured Playwright + axe + Lighthouse + behavior smoke**, matching the AUD-01/Phase-3 established harness.

### Test Framework
| Property | Value |
|----------|-------|
| Framework | Playwright (ephemeral measurement scripts, e.g. `baseline/measure.cjs`) + `@axe-core/playwright` 4.12.1 + Lighthouse 13.4.0 |
| Config file | none — ephemeral runner scripts under `baseline/`; serve via `python -m http.server 8080 --bind 127.0.0.1` |
| Quick run command | Playwright DOM measure on the two touched pages (index, services) @1440/390 |
| Full suite command | Playwright @1440/1024/768/390/360 + axe + Lighthouse across all 11 pages |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CNV-01 | Hero ≥1.0 lh @1440/1024; exactly 1 CTA/slide | automated_ui | Playwright: measure `.pbmit-slider-title` lh≥fs; count `.swiper-slide .pbmit-btn` == 1/slide | ❌ Wave 0 (extend measure.cjs) |
| CNV-02 | Pricing: 3 tiers, exactly 1 gold highlight, equal-height row, per-tier CTA→wa.me | automated_ui | Playwright: count `.pfg-pricing-tier`==3; `.pfg-pricing-tier--popular`==1; equal `getBoundingClientRect().height` in row; each CTA `href*="wa.me/77072370050"` | ❌ Wave 0 |
| CNV-03 | No sticky CTA; only `.pfg-whatsapp-float` fixed; JS byte-identical | other + automated_ui | `git diff HEAD js/custom.js` empty; grep fixed/sticky == only float; float overlaps nothing @390 | ✅ (grep) / ❌ overlap check Wave 0 |
| CNV-04 | Footer visual parity 11/11; gold 3px top-border preserved; FT3 not regressed | automated_ui | Playwright: footer border-top `3px solid rgb(236,171,35)` on 11; footer height sane @390 | ❌ Wave 0 |
| IMG-01 | No image distortion; sensible box; no horizontal overflow | automated_ui | Playwright: `<img>` naturalRatio vs renderRatio; `scrollWidth==clientWidth` @5vp | ❌ Wave 0 |
| T1 | Title-bar < 550px @768; ≥390 collapse not regressed | automated_ui | Playwright: `.pbmit-title-bar-wrapper` height @768 < 550 and > mobile floor | ❌ Wave 0 |
| VER-04 | Form→WhatsApp, menu, marquee, slider, reduced-motion all still work | automated_ui (smoke) | Playwright: submit `.pfg-form`→`window.open` wa.me; menu toggle; marquee running; slider slides | ✅ (Phase-3 smoke reusable) |

### Sampling Rate
- **Per task commit:** Playwright quick DOM check on the touched page (index for hero, services for pricing) @1440/390 + `git diff HEAD js/custom.js` empty.
- **Per wave merge:** axe=0 + Lighthouse a11y≥95 on touched pages.
- **Phase gate:** Full suite green across all 11 @5vp before `/gsd-verify-work`.

### Wave 0 Gaps
- [ ] Extend the ephemeral Playwright measure script to capture: pricing tier count/highlight/row-height, hero CTA count + lh, title-bar height @768, footer border + height, image render-vs-natural ratio. (No persistent test file convention exists; reuse the `baseline/measure*.cjs` pattern.)
- [ ] Reuse Phase-3 VER-04 smoke (form submit → wa.me, menu, marquee, slider) — already exercised on services/contacts.

## Security Domain

> `security_enforcement` not set false. This is a static, no-backend marketing site with no auth, no data mutations, no server. Phase 4 adds presentation + outbound `wa.me` links only.

### Applicable ASVS Categories
| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No accounts/auth exist |
| V3 Session Management | no | No sessions |
| V4 Access Control | no | No protected resources |
| V5 Input Validation | minimal | Pricing CTAs are static links — no user input added this phase; existing form unchanged (VER-04) |
| V6 Cryptography | no | No secrets/crypto; WhatsApp number is public |

### Known Threat Patterns for static-site + outbound links
| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Reverse tabnabbing on `target="_blank"` | Tampering | `rel="noopener"` — already the site convention; **every new pricing CTA must include `target="_blank" rel="noopener"`** (matches `index.html:914`, `services.html:440`) |
| Markup injection via copy | Tampering | All pricing copy is static author-controlled Russian text; no dynamic interpolation |

## Sources

### Primary (HIGH confidence — verified in repo this session)
- `services.html:163-498` — page structure; pricing insertion point (450↔452); FAQ at 456; existing `.pfg-grid`/`.pfg-card` (401-418) and CTA `.pbmit-btn` (431-448)
- `index.html:160-258` — hero Swiper 3 slides; one CTA/slide; CTA texts «Наши услуги»/«Подробнее»; malformed `</h1>` at :171; 12 `<img>` inventory (337/341/350/404/679/699/716/808-818)
- `css/custom.css` — tokens §9.0 (290-346), hero lh §9.7 (523-542), `.pfg-card` (72, 545-557), `.pfg-grid` (74, 1147), scoped reduced-motion (377-389), title-bar mobile §12.7 (990-1006), whatsapp-float (24-40), `.pfg-faq` (1186+), footer (583, 862)
- `css/shortcode.css:4922-4966` — title-bar vendor source; `min-height:550px` at 4932-4934
- `js/custom.js:56-146` — whatsapp-float (direct link) + `initLeadForm` (form→wa.me) + marquee; `WA_NUMBER=77072370050`
- grep: footer present on all 11 (`<footer class="site-footer …">`); footers differ only by `.active` + 2 content strings; only `.pfg-whatsapp-float` + vendor off-canvas are `position:fixed`; zero sticky/mobile-CTA classes
- `.planning/phases/01-*` (AUDIT HE1/HE2/T1/I1/I2/FT1-3, UI-SPEC accent reserved-for + hard constraints, IMPLEMENTATION file-map), `03-02-SUMMARY` (FAQ + 59 `!important` floor, native `<details>`)

### Secondary (MEDIUM confidence)
- None — all claims rest on direct repo reads.

### Tertiary (LOW confidence)
- None.

## Metadata

**Confidence breakdown:**
- Insertion point / composition (CNV-02): HIGH — exact lines read, primitives verified in Phase 3.
- Hero structure (CNV-01): HIGH for structure; the CTA-text discrepancy is a HIGH-confidence *finding* that the contract is internally inconsistent (flagged A1/OQ1).
- CNV-03 absence: HIGH — grep-confirmed only float + vendor off-canvas are fixed.
- Footer parity (CNV-04): HIGH — diffed all 11; divergence characterized.
- Imagery/title-bar (IMG-01/T1): HIGH for the vendor source and gap; MEDIUM on exact `object-fit` wrapper selectors (verify against live DOM — A5).

**Research date:** 2026-06-27
**Valid until:** 2026-07-27 (stable no-build repo; only invalidated by edits to the cited files)
