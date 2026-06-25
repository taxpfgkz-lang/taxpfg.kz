# External Integrations

**Analysis Date:** 2026-06-25

## Summary

This is a static marketing site with **no backend and no first-party API**. External
dependencies are minimal and limited to: Google Fonts (CSS `@import`), an embedded Google
Maps iframe, and a "lead form" that hands off to **WhatsApp** via a `wa.me` deep link.
There are **no analytics, no tracking pixels, no payment, no auth, and no databases.**

## APIs & External Services

**Messaging / lead capture:**
- WhatsApp (`wa.me`) - the primary conversion channel. The contact form (`.pfg-form` in
  `contacts.html:256`) is intercepted by `js/custom.js:72-111` (`initLeadForm`), which
  `preventDefault()`s the submit, builds a prefilled message from the form fields
  (name, phone, business type, comment), and opens
  `https://wa.me/<number>?text=<encoded>` in a new tab (`js/custom.js:101-102`).
  - No SDK, no API key. Pure deep link.
  - The WhatsApp number is held in a JS constant `WA_NUMBER` in `js/custom.js`.
  - Header CTA links also point directly to `https://wa.me/77072370050` (e.g.
    `index.html:87`, `accounting.html:334`).

**Maps:**
- Google Maps embed - `<iframe src="https://www.google.com/maps?q=...&output=embed">` in
  `contacts.html:288`, plus an "Open in Google Maps" link in `contacts.html:290`. Uses the
  public no-key `maps?q=&output=embed` form (no Maps JS API, no API key, no billing).

**Fonts:**
- Google Fonts - remote CSS loaded via `@import url('https://fonts.googleapis.com/...')`
  in `css/base.css:16-19` (Be Vietnam Pro, Plus Jakarta Sans, Roboto). This is the only
  render-blocking third-party request on every page. See STACK.md → Text Fonts.

## Data Storage

**Databases:**
- None. No database, ORM, or persistence layer of any kind.

**File Storage:**
- Local filesystem only. All assets (`images/`, `fonts/`, `css/`, `js/`) are served as
  static files from the same origin.

**Caching:**
- None at the application level (static host / CDN may cache, but nothing is configured in-repo).

## Authentication & Identity

- None. No login, no sessions, no user accounts, no auth provider.

## Monitoring & Observability

**Error Tracking:**
- None. No Sentry/Rollbar/etc.

**Analytics:**
- None detected. No Google Analytics / gtag, no Google Tag Manager, no Yandex.Metrika,
  no Facebook Pixel, no Hotjar — confirmed by searching all HTML for `gtag`,
  `googletagmanager`, `analytics`, `yandex`/`metrika`, `fbq`, `pixel` (no matches).

**Logs:**
- Not applicable (static site, no server code).

## CI/CD & Deployment

**Hosting:**
- Static host serving `https://taxpfg.kz/` (canonical URL in `index.html:9`). Specific
  provider is not declared in-repo.

**CI Pipeline:**
- None in repository. No `.github/workflows`, no CI config.

## Environment Configuration

**Required env vars:**
- None. There is no `.env` file and no environment-variable mechanism — a static site has
  no runtime to read them. Site-specific values are hardcoded:
  - WhatsApp number: `WA_NUMBER` constant in `js/custom.js` (and inline `wa.me/77072370050` links)
  - Phone: `tel:+77072370050` (across all pages, e.g. `contacts.html:192`)
  - Email: `mailto:info@taxpfg.kz` (marked provisional — `<!-- [PFG] e-mail предварительный... -->`,
    e.g. `contacts.html:197`)
  - Address: проспект Абая 68/74, БЦ «AVENUE CITY», офис 39, Алматы (JSON-LD + Maps query)

**Secrets location:**
- None. No secrets, tokens, or API keys exist in the project (none are needed — all third-party
  uses are keyless: `wa.me`, `maps?q=&output=embed`, Google Fonts CSS).

## Contact Integrations

- **Phone:** `tel:+77072370050` links in the header, footer, and contact pages of every HTML file.
- **Email:** `mailto:info@taxpfg.kz` (provisional; flagged in HTML comments to confirm with client).
- **WhatsApp:** `https://wa.me/77072370050` direct links + the form-to-WhatsApp handoff above.
- **Map:** Google Maps embed + external link (see Maps above).

## Embedded Third-Party Content

- Google Maps iframe (`contacts.html:288`) — the only external embed.
- `js/email-decode.min.js` — Cloudflare email-obfuscation decoder shipped with the theme.
  It is a client-side decoder artifact; it does not call out to Cloudflare at runtime.

## Webhooks & Callbacks

**Incoming:**
- None. No server to receive them.

**Outgoing:**
- None. The form does not POST anywhere; it opens a WhatsApp chat in the browser. No
  `fetch`/`XMLHttpRequest` calls exist in `js/custom.js` (verified — only `addEventListener`
  and `window.open`).

## Search Form Note

Each page contains a theme search form `<form role="search" method="get" action="index.html">`
(e.g. `contacts.html:489`). This is a leftover from the GudFin WordPress theme and has **no
working backend** — a GET to `index.html` cannot perform a real search on a static site. Treat
it as non-functional UI inherited from the template.

---

*Integration audit: 2026-06-25*
