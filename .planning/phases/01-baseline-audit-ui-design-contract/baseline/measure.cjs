// Ephemeral DOM-measurement + screenshot harness for AUD-02 (plan 01-03).
// External/npx-style tooling — NOT site code. Drives global playwright@1.60.0
// (vendored under gsd-pi) against the local static server on :8080.
// Records DOM-measured boxes (RESEARCH Pattern 2) per block-type per viewport.
const path = require('path');
const PW = 'C:/Users/Администратор/AppData/Roaming/npm/node_modules/gsd-pi/node_modules/playwright';
const { chromium } = require(PW);

const BASE = 'http://127.0.0.1:8080';
const OUT = path.join(__dirname, 'screenshots');
const VIEWPORTS = [1440, 1024, 768, 390, 360];

// representative pages (Claude's discretion per CONTEXT.md)
const PAGES = {
  index: '/index.html',          // hero + slider + img-heavy + static boxes
  services: '/services.html',    // title-bar + service cards
  contacts: '/contacts.html',    // lead form + map iframe
  about: '/about.html',          // shared chrome + inner content
};

const results = []; // {block, page, vw, metric, value, note}
function rec(block, page, vw, metric, value, note) {
  results.push({ block, page, vw, metric, value, note: note || '' });
}

async function measure(page, sel, prop) {
  return page.evaluate(({ sel, prop }) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const out = { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) };
    if (prop) for (const p of prop) out[p] = cs.getPropertyValue(p);
    return out;
  }, { sel, prop });
}

async function shot(page, name) {
  await page.screenshot({ path: path.join(OUT, name), fullPage: false });
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const vw of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vw, height: 900 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();

    // ---- shared chrome (header / nav) — audited once on about.html ----
    await page.goto(BASE + PAGES.about, { waitUntil: 'networkidle', timeout: 30000 }).catch(()=>{});
    await page.waitForTimeout(1200);

    // doc width vs viewport (horizontal scroll check)
    const docW = await page.evaluate(() => ({
      scrollW: document.documentElement.scrollWidth,
      clientW: document.documentElement.clientWidth,
      bodyScrollW: document.body.scrollWidth,
    }));
    rec('global', 'about', vw, 'scrollWidth', docW.scrollW, `clientWidth=${docW.clientW} overflow=${docW.scrollW - docW.clientW}px`);

    // header
    const hdr = await measure(page, '.site-header', ['position','height','background-color']);
    if (hdr) rec('header', 'about', vw, 'box', `${hdr.w}x${hdr.h}`, `pos=${hdr.position}`);

    // logo
    const logo = await measure(page, '.pfg-logo, .site-branding, .pbmit-logo-area');
    if (logo) rec('header', 'about', vw, 'logo-box', `${logo.w}x${logo.h}`);

    // header search toggle (known target-size flag)
    const search = await page.evaluate(() => {
      const el = document.querySelector('.pbmit-search-btn, .search-btn, [class*="search"] a, [class*="search"] button');
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { w: Math.round(r.width), h: Math.round(r.height), cls: el.className };
    });
    if (search) rec('header', 'about', vw, 'search-tap', `${search.w}x${search.h}`, `cls=${search.cls} (44px floor)`);

    // menu toggle (mobile)
    const burger = await page.evaluate(() => {
      const el = document.querySelector('#mobile-menu, .pbmit-menu-bar, [aria-label="Меню"], .menu-toggle');
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const vis = getComputedStyle(el).display !== 'none' && r.width > 0;
      return { w: Math.round(r.width), h: Math.round(r.height), vis, cls: el.className };
    });
    if (burger) rec('nav', 'about', vw, 'burger-tap', `${burger.w}x${burger.h}`, `visible=${burger.vis} (44px floor)`);

    await shot(page, `header-${vw}.png`);

    // off-canvas nav: open it on mobile widths
    if (vw <= 1024) {
      const opened = await page.evaluate(() => {
        const t = document.querySelector('#mobile-menu, [aria-label="Меню"], .menu-toggle, .pbmit-menu-bar');
        if (t) { t.click(); return true; }
        return false;
      });
      if (opened) {
        await page.waitForTimeout(600);
        const navBox = await measure(page, '#site-navigation, .main-menu, nav.navigation', ['width','transform']);
        if (navBox) rec('nav', 'about', vw, 'offcanvas-box', `${navBox.w}x${navBox.h}`);
        await shot(page, `nav-offcanvas-${vw}.png`);
        // first menu link tap height
        const link = await page.evaluate(() => {
          const a = document.querySelector('#site-navigation a, .main-menu a, nav a');
          if (!a) return null;
          const r = a.getBoundingClientRect();
          return { w: Math.round(r.width), h: Math.round(r.height) };
        });
        if (link) rec('nav', 'about', vw, 'menu-link-tap', `${link.w}x${link.h}`, '44px floor');
      }
    }

    // ---- title-bar (inner pages) — services.html ----
    await page.goto(BASE + PAGES.services, { waitUntil: 'networkidle', timeout: 30000 }).catch(()=>{});
    await page.waitForTimeout(1000);
    const tb = await measure(page, '.pbmit-title-bar-wrapper', ['min-height','padding-top','padding-bottom','background-image']);
    if (tb) rec('title-bar', 'services', vw, 'box', `${tb.w}x${tb.h}`, `minH=${tb['min-height']} padT=${tb['padding-top']} padB=${tb['padding-bottom']}`);
    const tbH1 = await page.evaluate(() => {
      const h = document.querySelector('.pbmit-title-bar-wrapper h1, .pbmit-tbar-title, .pbmit-title');
      if (!h) return null;
      const r = h.getBoundingClientRect();
      const cs = getComputedStyle(h);
      return { fs: cs.fontSize, lh: cs.lineHeight, w: Math.round(r.width), h: Math.round(r.height), text: (h.textContent||'').trim().slice(0,40) };
    });
    if (tbH1) rec('title-bar', 'services', vw, 'h1', tbH1.fs, `lh=${tbH1.lh} box=${tbH1.w}x${tbH1.h} "${tbH1.text}"`);
    await shot(page, `titlebar-${vw}.png`);

    // service cards
    const card = await page.evaluate(() => {
      const els = document.querySelectorAll('.pfg-card, .pbmit-service-style-1, .pbmit-ihbox, [class*="service-box"]');
      if (!els.length) return null;
      const el = els[0];
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return { w: Math.round(r.width), h: Math.round(r.height), pad: cs.padding, count: els.length, cls: el.className.slice(0,60) };
    });
    if (card) rec('cards', 'services', vw, 'box', `${card.w}x${card.h}`, `pad=${card.pad} count=${card.count}`);
    await shot(page, `cards-${vw}.png`);

    // ---- hero / slider (index) ----
    await page.goto(BASE + PAGES.index, { waitUntil: 'networkidle', timeout: 30000 }).catch(()=>{});
    await page.waitForTimeout(1800);
    const hero = await measure(page, '.pbmit-slider-area, .pbmit-slider-one, .swiper', ['height']);
    if (hero) rec('hero', 'index', vw, 'box', `${hero.w}x${hero.h}`);
    const heroH = await page.evaluate(() => {
      const h = document.querySelector('.pbmit-slider-area h2, .pbmit-slider-title, .swiper-slide h2, h2');
      if (!h) return null;
      const r = h.getBoundingClientRect();
      const cs = getComputedStyle(h);
      return { fs: cs.fontSize, lh: cs.lineHeight, w: Math.round(r.width), h: Math.round(r.height), overflow: Math.round(r.right) };
    });
    if (heroH) rec('hero', 'index', vw, 'title', heroH.fs, `lh=${heroH.lh} box=${heroH.w}x${heroH.h} right=${heroH.overflow}`);
    // index doc overflow
    const idxW = await page.evaluate(() => ({ s: document.documentElement.scrollWidth, c: document.documentElement.clientWidth }));
    rec('global', 'index', vw, 'scrollWidth', idxW.s, `clientWidth=${idxW.c} overflow=${idxW.s - idxW.c}px`);
    await shot(page, `hero-${vw}.png`);

    // images on index
    const img = await page.evaluate(() => {
      const imgs = [...document.querySelectorAll('img')].filter(i => i.getBoundingClientRect().width > 0);
      return imgs.slice(0,3).map(i => {
        const r = i.getBoundingClientRect();
        return { w: Math.round(r.width), h: Math.round(r.height), nw: i.naturalWidth, nh: i.naturalHeight, src: (i.currentSrc||i.src).split('/').pop() };
      });
    });
    if (img && img.length) rec('imagery', 'index', vw, 'imgs', JSON.stringify(img), 'render vs natural');

    // ---- lead form (contacts) ----
    await page.goto(BASE + PAGES.contacts, { waitUntil: 'networkidle', timeout: 30000 }).catch(()=>{});
    await page.waitForTimeout(1200);
    const form = await measure(page, '.pfg-form, form', ['gap']);
    if (form) rec('form', 'contacts', vw, 'box', `${form.w}x${form.h}`);
    const field = await page.evaluate(() => {
      const el = document.querySelector('.pfg-form input, .form-control, input[type="text"], input[name]');
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return { w: Math.round(r.width), h: Math.round(r.height), fs: cs.fontSize };
    });
    if (field) rec('form', 'contacts', vw, 'input-box', field ? `${field.w}x${field.h}` : 'n/a', field ? `fontSize=${field.fs} (iOS-zoom<16px?)` : '');
    const submit = await page.evaluate(() => {
      const el = document.querySelector('.pfg-form button, .pfg-form [type="submit"], button[type="submit"]');
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { w: Math.round(r.width), h: Math.round(r.height) };
    });
    if (submit) rec('form', 'contacts', vw, 'submit-tap', `${submit.w}x${submit.h}`, '44px floor');
    const consent = await page.evaluate(() => {
      const el = document.querySelector('.pfg-consent input[type="checkbox"], input[type="checkbox"]');
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { w: Math.round(r.width), h: Math.round(r.height) };
    });
    if (consent) rec('form', 'contacts', vw, 'consent-checkbox', `${consent.w}x${consent.h}`, '44px floor');
    const mapBox = await measure(page, 'iframe[src*="google"], iframe[src*="maps"], .pfg-map iframe, iframe');
    if (mapBox) rec('form', 'contacts', vw, 'map-iframe', `${mapBox.w}x${mapBox.h}`);
    await shot(page, `form-${vw}.png`);

    // ---- footer (contacts; shared chrome) ----
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(600);
    const ft = await measure(page, '.site-footer', ['border-top','background-color']);
    if (ft) rec('footer', 'contacts', vw, 'box', `${ft.w}x${ft.h}`, `borderTop=${ft['border-top']}`);
    const ftLink = await page.evaluate(() => {
      const a = document.querySelector('.site-footer a');
      if (!a) return null;
      const r = a.getBoundingClientRect();
      return { w: Math.round(r.width), h: Math.round(r.height) };
    });
    if (ftLink) rec('footer', 'contacts', vw, 'footer-link-tap', `${ftLink.w}x${ftLink.h}`, '44px floor');
    await shot(page, `footer-${vw}.png`);

    await ctx.close();
    console.error(`viewport ${vw} done`);
  }
  await browser.close();

  // dump measurements as JSON for Task 2
  const fs = require('fs');
  fs.writeFileSync(path.join(__dirname, 'measurements.json'), JSON.stringify(results, null, 2));
  console.log('MEASUREMENTS_TOTAL=' + results.length);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
