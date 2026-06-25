# Feature Research — UI/UX Patterns for Trust & Lead Conversion

**Domain:** Lead-gen marketing site for a professional financial/accounting consulting firm (taxpfg.kz, PrimeFinance Group), Kazakhstan SMB audience, Russian-language, static brownfield (11 pages, GudFin theme + `pfg-*` premium layer).
**Researched:** 2026-06-25
**Confidence:** HIGH for established CRO/UX patterns (Baymard, W3C ARIA APG, NN/g-class heuristics); MEDIUM for region-specific (KZ/RU SMB) conversion nuance, which is reasoned from general principles rather than KZ-specific studies.

> Scope note: this is a UI-polish milestone on an existing site. "Feature" here = a UI/UX pattern or convention, not a new app capability. Business logic, forms→WhatsApp flow, routing, and JSON-LD are frozen (PROJECT.md Out of Scope). Every recommendation is tied to **trust** or **lead conversion**, not generic prettiness, and every CSS change lands in `css/custom.css`/`css/base.css`, every JS change in `js/custom.js`.

---

## Feature Landscape

### Table Stakes (Users Expect These)

Missing or weak versions of these make a financial-services site read as amateur or untrustworthy — which directly kills lead intent. Users give no credit for having them; they penalize hard for their absence.

| Feature | Why Expected (trust/conversion rationale) | Complexity | Pages | Notes |
|---------|-------------------------------------------|------------|-------|-------|
| **Above-the-fold value prop in one glance** — what the firm does + for whom + why-them, readable in <5s without scrolling | A confused visitor leaves. Clarity is the single biggest conversion lever; "one focused conversion goal" per the Unbounce anatomy | LOW | `index.html` hero | Headline must name the outcome ("бухгалтерия под ключ для МСБ"), not just the brand. Subhead = proof/scope. Verify hero text legibility over the slider image (contrast ≥4.5:1) |
| **Single, unmistakable primary CTA above the fold** | One dominant action reduces decision paralysis; competing CTAs split intent | LOW | hero on all pages, title-bar on inner pages | Primary = "Оставить заявку"/WhatsApp. Everything else (phone, secondary link) must be visually subordinate |
| **Trust signals above the fold** — years in business, # clients served, "лицензия/сертификат", or a recognizable stat | Financial decisions are high-trust; people verify legitimacy before contact. Social proof is "the most powerful tool" (Unbounce) | LOW–MED | hero/`index.html`, repeated on `about.html` | Stats/counters already exist (numinate/circle-progress). Ensure they read as credible specifics, not round marketing fluff |
| **Visible, tap-friendly contact path everywhere** (phone, WhatsApp, "Заявка") | Lead-gen site's entire purpose. Friction to contact = lost lead | LOW | header (all 11), footer (all 11), floating WhatsApp (exists) | `.pfg-whatsapp-float` exists. Confirm 44×44px min target on mobile and that it never overlaps the form submit or footer CTA |
| **Sticky header with persistent CTA** | Lets a scrolled, convinced visitor convert without scrolling back up | LOW (exists) | all 11 (theme sticky header) | Sticky header already implemented (`gsap-animation.js`). Ensure the header CTA stays visible/contrast-correct in the sticky/compact state |
| **Mobile menu that works** | >50% of KZ SMB traffic is mobile; broken nav = bounce | LOW (exists) | all 11 | `initMobileMenu` exists. Audit focus trap, `aria-expanded`, body-scroll-lock, and 44px targets |
| **Service grid with scannable cards** — icon + title + 1-line benefit + link | Visitors scan, don't read. Parallel, equal-weight cards signal a complete, organized offering | LOW–MED | `services.html`, `index.html`, footers of detail pages | `.pfg-card`/`.pfg-grid` exist. Enforce equal card heights, consistent icon size, aligned CTAs; broken/ragged cards read as sloppy |
| **Lead form: short, labeled, validated** | Each extra field costs conversions; "22% abandon due to complexity" (Baymard). Visible labels + inline validation are expected | MED | `contacts.html` `.pfg-form` | Keep fields minimal (name, phone, optional message + consent). Visible labels (not placeholder-only), inline validation, clear required marks |
| **Form success + error states** | Silence after submit = "did it work?" doubt; for a WhatsApp-handoff form, the state message is the only feedback | LOW (exists, audit) | `contacts.html` | `.pfg-form-status` exists. Ensure success/error are visually distinct, announced to AT (`aria-live`), and not color-only |
| **Mobile-correct input types/keyboards** | Wrong keyboard on a phone field = friction & typos | LOW | `contacts.html` | `type="tel"`, `inputmode`, `autocomplete` on phone/name. Localized phone mask helps (Baymard: 64% miss this) |
| **FAQ / objection-handling accordion** | SMB buyers have predictable objections (price, switching, deadlines, confidentiality). Answering them pre-empts drop-off | MED | `index.html` and/or service pages | If accordions exist via theme, retrofit ARIA APG semantics (see Anti-Features for the wrong way) |
| **Credible footer** — full contact block, address, legal entity, privacy link, hours | A complete footer is itself a trust signal; a thin footer reads as fly-by-night | LOW | all 11 | Footer duplicated ×11 — edits must be applied to every file. Include БИН/legal name, address, phone, WhatsApp, privacy link |
| **Consistent visual hierarchy & spacing scale** | Inconsistent spacing/type reads as "cheap" and erodes trust subconsciously | MED | all 11 | Already partially done (commit c08cbd3). This milestone hardens it into a contract |
| **Visible keyboard focus + AA contrast** | Accessibility floor; also a quality signal. Required by PROJECT.md a11y-floor | LOW (exists) | all 11 | Focus ring + contrast tokens already in `custom.css`; keep ≥ baseline |

### Differentiators (Competitive Polish That Lifts Conversion)

Not expected, but they meaningfully raise trust and conversion above a typical KZ accounting-firm template site. Align with Core Value: "выглядеть дорого + чисто конвертировать."

| Feature | Value Proposition (trust/conversion) | Complexity | Pages | Notes |
|---------|--------------------------------------|------------|-------|-------|
| **Specific, attributed testimonials** — real name, company, photo, concrete result | Specific social proof ("снизили налог на X / закрыли год без штрафов") outconverts generic praise; "you can't fake it" + use real names/photos (Unbounce) | MED | `index.html`, `about.html` | Avoid stock-photo + fake-name testimonials — actively harmful (see Anti-Features). If real ones unavailable, prefer a quantified result block instead |
| **Transparent pricing / tariff packages** | Pricing transparency is rare among KZ accounting firms; showing "от X ₸/мес" pre-qualifies leads and signals confidence. Reduces "звоните узнавать цену" friction | MED–HIGH | new/`services.html`, `accounting.html` | 3-tier package layout (e.g. ИП / ТОО малый / ТОО полный). Highlight one "популярный" tier with a badge + elevated card. Each tier ends in its own CTA. If exact prices can't be shown, use "от" anchors or a clear "по запросу" with a CTA — never an empty table |
| **"Популярный/Рекомендуем" highlighted tier** | Anchoring + social proof in one move; guides undecided buyers to the target package | LOW | pricing section | Visual emphasis: scale-up, accent border (gold), badge. Don't highlight more than one |
| **Sticky mobile CTA bar** | On mobile, a bottom-anchored "Заявка / WhatsApp" bar keeps the conversion action one tap away through long scrolls | MED | all 11 (mobile only) | New `pfg-` component in `custom.js`/`custom.css`. Must not cover footer content or the form submit; hide when the form/footer CTA is in view to avoid redundancy. Respect safe-area inset |
| **Trust-stat counters with context** | Animated counters (years, clients, returns filed, ₸ saved) give scannable proof; theme already ships numinate/circle-progress | LOW (exists) | `index.html`, `about.html` | Reuse existing widget; ensure numbers are believable and labeled. Respect `prefers-reduced-motion` (already handled) |
| **Process / "как мы работаем" steps** | A 3–4 step "how it works" lowers perceived risk of switching accountants — a top SMB objection | LOW (exists) | `about.html` (`.pfg-steps`), service pages | `.pfg-steps` exists. Reuse on service detail pages to convert mid-funnel visitors |
| **Guarantee / risk-reversal statement** | "Гарантия отсутствия штрафов по нашей вине" or "бесплатная консультация" dramatically lowers contact friction | LOW | hero/pricing/contacts | Pure copy+UI; place near CTAs. Must be truthful (avoid dark-pattern guarantees) |
| **Credential / membership badges** | ППС, сертификаты, partner logos (1С, Kaspi, banks) are concrete legitimacy markers for finance | LOW–MED | `about.html`, footer, hero strip | Real badges only. Grayscale logo strip is a clean, premium convention |
| **Above-the-fold micro-trust row** | A thin row of 3 proof points under the hero CTA (e.g. "10+ лет · 200+ клиентов · работаем по РК") converts skeptics before they scroll | LOW | `index.html` hero | Cheap, high-impact; pure CSS layout addition |
| **Inline-validated, low-friction form UX** | Real-time validation + retained input + clear phone format reduces abandonment (Baymard) beyond the table-stakes minimum | MED | `contacts.html` | Adaptive messages, validate-on-blur, keep values on error |

### Anti-Features (Seem Good, Actively Hurt Trust/Conversion)

Document these to prevent scope creep and dark patterns. For a trust-driven financial site, several "conversion hacks" backfire badly.

| Anti-Feature | Why It Gets Requested | Why It's Problematic | Do This Instead |
|--------------|-----------------------|----------------------|-----------------|
| **Entry/exit pop-up modal** ("оставьте заявку!") | "Captures more leads" | Interrupts trust-building, annoys, hurts mobile UX and a11y; reads as desperate for a financial firm | Persistent sticky CTA + a strong contacts section. Let intent build |
| **Fake countdown timer / "осталось 2 места"** | Urgency lifts conversion | Dishonest urgency is a dark pattern; for a finance/trust brand it destroys credibility if noticed | Genuine reasons to act (free consult, response-time promise) |
| **Stock-photo testimonials with invented names** | "Need social proof now" | Easily spotted; "you can't fake it" — fake proof converts negatively once detected | Quantified result blocks, real client logos, or honest "новый сайт — отзывы скоро" placeholder absence |
| **Carousel/slider of multiple hero messages** | "Show everything important" | Auto-rotating heroes bury the value prop, get ignored (banner blindness), hurt a11y & LCP. Theme ships a Swiper hero — keep it static-feeling or single-message | One clear hero message + one CTA. If slider stays, ensure pause control + readable contrast + no critical CTA hidden on slide 2 |
| **Placeholder-only form labels** | "Looks cleaner" | Label disappears on focus → users forget the field, fail validation, abandon; fails a11y | Always-visible labels above inputs; placeholder only for format hints |
| **Long lead form (address, company size, budget, etc.)** | "Qualify the lead" | Each field cuts conversion; "22% abandon due to complexity" (Baymard). Wrong tradeoff for top-of-funnel | Minimal fields (name + phone + consent); qualify in the WhatsApp conversation |
| **CTA copy "Отправить"/"Click here"** | Default button text | Generic copy underperforms; says nothing about value | Outcome copy: "Получить консультацию", "Рассчитать стоимость", "Написать в WhatsApp" |
| **Too many competing CTAs / link soup in hero** | "Give options" | Splits attention, lowers primary conversion | One primary CTA; demote phone/secondary links visually |
| **Auto-playing sound/video, heavy parallax everywhere** | "Looks premium/modern" | Hurts performance (site already ~6.9MB images), motion-sensitivity, mobile. Premium ≠ busy | Restrained motion (theme GSAP already tuned), `prefers-reduced-motion` respected |
| **Accordion that animates height with display:none toggling and no ARIA** | "FAQ looks tidy" | Inaccessible (no `aria-expanded`/`aria-controls`), keyboard-broken; a11y-floor violation | Implement per W3C ARIA APG: header = `button` inside heading, `aria-expanded`, `aria-controls`, Enter/Space toggles |
| **Color-only success/error states** | Quick to style | Fails contrast/colorblind users; ambiguous | Pair color with icon + text + `aria-live` announcement |
| **Highlighting every pricing tier as "best"** | "Make all attractive" | Removes the anchoring/guidance benefit; reads as gimmicky | Exactly one highlighted "популярный" tier |

---

## Feature Dependencies

```
[Spacing scale + type scale contract]
    └──requires by──> [Service grid cards]  (cards need consistent rhythm)
    └──requires by──> [Pricing tiers]       (tiers are specialized cards)
    └──requires by──> [Hero layout]

[Single primary CTA hierarchy]
    └──enables──> [Sticky mobile CTA bar]   (bar reuses the one primary action)
    └──enables──> [Above-the-fold micro-trust row]

[Lead form (table stakes)]
    └──enhanced by──> [Inline validation UX] (differentiator layer on same form)
    └──requires──> [Success/error states]

[Pricing tiers]
    └──requires──> [Per-tier CTA]            (each tier routes to the same lead flow)
    └──enhanced by──> ["Популярный" highlight]

[FAQ accordion]
    └──requires──> [ARIA APG semantics]      (a11y-floor is non-negotiable)

[Testimonials / credential badges] ──enhances──> [Hero trust signals]

[Sticky mobile CTA bar] ──conflicts──> [Floating WhatsApp button]
    (both bottom-anchored on mobile → visual collision; must coexist or one yields)
```

### Dependency Notes

- **Spacing/type contract is the root dependency.** Cards, pricing, hero all inherit it. The UI design contract (PROJECT.md Active) must land before component-level polish, or fixes won't compose.
- **CTA hierarchy precedes the sticky mobile bar.** The bar simply re-surfaces the established primary action; define "the one CTA" first.
- **Sticky mobile CTA bar conflicts with the existing floating WhatsApp button.** Both anchor bottom-right/bottom on mobile. Resolve deliberately: either fold WhatsApp into the bar, or offset/hide one when the other is active. Audit this collision explicitly.
- **FAQ accordion requires ARIA semantics** — not optional given the a11y-floor constraint. If the theme accordion lacks them, patch in `custom.js`.
- **Pricing tiers depend on per-tier CTAs** all routing into the existing WhatsApp lead flow — no new backend (logic-safe constraint).

---

## MVP Definition (this UI-polish milestone)

### Launch With (v1) — Table stakes hardened

- [ ] Hero value-prop clarity + single primary CTA + readable contrast over slider — `index.html`
- [ ] Above-the-fold trust row (stats/years/clients) — `index.html`
- [ ] Consistent service-grid cards (equal height, aligned CTAs) — `services.html`, `index.html`
- [ ] Lead form: visible labels, minimal fields, inline validation, distinct success/error with `aria-live`, mobile input types — `contacts.html`
- [ ] FAQ accordion with correct ARIA APG semantics + keyboard — page(s) with FAQ
- [ ] Credible footer parity across all 11 pages
- [ ] Spacing/type-scale contract applied site-wide; focus + AA contrast at/above baseline

### Add After Validation (v1.x) — Differentiators

- [ ] Transparent 3-tier pricing with one "популярный" highlight + per-tier CTA — `services.html`/`accounting.html`
- [ ] Sticky mobile CTA bar (resolve WhatsApp-float collision)
- [ ] Specific attributed testimonials / credential-badge strip — `index.html`, `about.html`
- [ ] Guarantee / risk-reversal copy near CTAs
- [ ] Process "как мы работаем" steps reused on service detail pages

### Future Consideration (v2+) — Out of this milestone's scope

- [ ] Build-system/payload optimization (WebP, asset trimming) — flagged as separate milestone in PROJECT.md
- [ ] Templating to kill header/footer ×11 duplication — separate milestone
- [ ] Backend form handling / CRM integration — out of scope (static + WhatsApp by design)

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Hero clarity + single CTA + contrast | HIGH | LOW | P1 |
| Lead form labels/validation/states | HIGH | MEDIUM | P1 |
| FAQ ARIA accordion | MEDIUM | MEDIUM | P1 (a11y-floor) |
| Service-grid card consistency | HIGH | MEDIUM | P1 |
| Footer credibility parity ×11 | MEDIUM | LOW | P1 |
| Above-the-fold trust row | HIGH | LOW | P1 |
| Spacing/type contract | HIGH | MEDIUM | P1 |
| Transparent pricing tiers | HIGH | HIGH | P2 |
| Sticky mobile CTA bar | HIGH | MEDIUM | P2 |
| Attributed testimonials | HIGH | MEDIUM | P2 |
| Guarantee / risk-reversal | MEDIUM | LOW | P2 |
| Process steps on service pages | MEDIUM | LOW | P3 |
| Credential/partner logo strip | MEDIUM | MEDIUM | P3 |

**Priority key:** P1 = must-have for production bar; P2 = high-leverage conversion lift, add after table stakes; P3 = nice-to-have polish.

## Per-Page Mapping (quick reference)

| Page | Primary patterns to enforce |
|------|------------------------------|
| `index.html` | Hero clarity + single CTA, above-fold trust row, trust-stat counters, testimonials, service-grid cards, FAQ, sticky mobile CTA, footer |
| `services.html` | Service-grid card consistency (hub), pricing tiers, per-card CTA, footer |
| `accounting.html` / detail pages | Pricing tiers, process steps, mid-page CTA, card consistency, footer |
| `accounting-recovery.html`, `taxes.html`, `consulting.html`, `registration.html` | Process steps, single mid-page CTA, scannable benefit blocks, footer |
| `contacts.html` | Lead form best practices (labels, validation, states, mobile inputs), trust block near form, footer |
| `about.html` | Testimonials, credential badges, stats/counters, process steps, footer |
| `privacy.html` | Readable prose, consistent type scale, footer |
| `404.html` | Clear path back to value (links to services/contacts), footer |
| All 11 | Sticky header + CTA, mobile menu a11y, footer parity, spacing/type contract, focus + contrast |

## Competitor / Convention Analysis

| Pattern | Typical KZ accounting-firm site | Premium B2B services site | taxpfg.kz approach |
|---------|-------------------------------|---------------------------|--------------------|
| Pricing | Hidden ("звоните") | Transparent tiers w/ "popular" | Show "от X ₸" tiers + one highlight → differentiator |
| Social proof | Generic / none | Specific attributed testimonials + logos | Specific, real-only; quantified results |
| Hero | Busy auto-slider, vague slogan | One outcome headline + one CTA + trust row | Single message, readable over slider, micro-trust row |
| Lead capture | Long form or phone-only | Short form + chat handoff | Minimal form → WhatsApp (already the model); polish UX |
| Mobile CTA | Buried | Sticky bar / persistent button | Sticky bar + reconciled WhatsApp float |

## Sources

- Baymard Institute — checkout/form field count, labels, inline validation, mobile input formatting (HIGH; "22% abandon due to complexity", "14% abandon if phone simply required", inline-validation gaps). https://baymard.com/blog/checkout-form-best-practices
- W3C ARIA Authoring Practices Guide — Accordion pattern: `button` in heading, `aria-expanded`, `aria-controls`, Enter/Space, region tradeoff (HIGH). https://www.w3.org/WAI/ARIA/apg/patterns/accordion/
- Unbounce — Anatomy of a Landing Page: social proof as primary lever, real names/photos, one conversion goal, conversational CTA copy, short forms (MEDIUM–HIGH). https://unbounce.com/landing-page-articles/the-anatomy-of-a-landing-page/
- Project context: `.planning/PROJECT.md`, `.planning/codebase/STRUCTURE.md`, `.planning/codebase/ARCHITECTURE.md` (existing `.pfg-*` components, WhatsApp lead flow, constraints).

---
*Feature research for: financial/accounting consulting lead-gen marketing site (UI-polish milestone)*
*Researched: 2026-06-25*
