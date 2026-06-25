// Focused re-measure to disambiguate selector-misses from real zero-size issues.
const path = require('path');
const PW = 'C:/Users/Администратор/AppData/Roaming/npm/node_modules/gsd-pi/node_modules/playwright';
const { chromium } = require(PW);
const BASE = 'http://127.0.0.1:8080';

(async () => {
  const browser = await chromium.launch({ headless: true });

  // --- contacts: consent label hit-area + real submit/inputs at 390 ---
  let ctx = await browser.newContext({ viewport: { width: 390, height: 900 } });
  let page = await ctx.newPage();
  await page.goto(BASE + '/contacts.html', { waitUntil: 'networkidle' }).catch(()=>{});
  await page.waitForTimeout(1000);
  const consent = await page.evaluate(() => {
    const cb = document.querySelector('input[type="checkbox"]');
    const label = cb && cb.closest('label');
    const r1 = cb && cb.getBoundingClientRect();
    const r2 = label && label.getBoundingClientRect();
    return {
      checkbox: cb ? { w: Math.round(r1.width), h: Math.round(r1.height) } : null,
      label: label ? { w: Math.round(r2.width), h: Math.round(r2.height), cls: label.className } : null,
    };
  });
  console.log('CONSENT', JSON.stringify(consent));

  // footer links real hit area
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(400);
  const footer = await page.evaluate(() => {
    const links = [...document.querySelectorAll('.site-footer a')].filter(a => a.getBoundingClientRect().height > 0);
    const menu = links.slice(0, 4).map(a => { const r = a.getBoundingClientRect(); return { w: Math.round(r.width), h: Math.round(r.height), t: (a.textContent||'').trim().slice(0,20) }; });
    return { totalVisible: links.length, sample: menu };
  });
  console.log('FOOTER_LINKS', JSON.stringify(footer));
  await ctx.close();

  // --- off-canvas real container at 390 ---
  ctx = await browser.newContext({ viewport: { width: 390, height: 900 } });
  page = await ctx.newPage();
  await page.goto(BASE + '/about.html', { waitUntil: 'networkidle' }).catch(()=>{});
  await page.waitForTimeout(1000);
  const navProbe = await page.evaluate(() => {
    const cands = ['#site-navigation','.main-menu','nav','.pbmit-mobile-menu','.navbar-collapse','#mobile-menu','.menu-mobile'];
    return cands.map(s => { const el = document.querySelector(s); if(!el) return [s,'(none)']; const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return [s, `${Math.round(r.width)}x${Math.round(r.height)} disp=${cs.display} vis=${cs.visibility} pos=${cs.position}`]; });
  });
  console.log('NAV_CANDS', JSON.stringify(navProbe, null, 1));
  // toggle then re-probe the navigation element
  await page.evaluate(() => { const t = document.querySelector('[aria-label="Меню"], .menu-toggle, #mobile-menu, .pbmit-menu-bar'); if(t) t.click(); });
  await page.waitForTimeout(700);
  const navOpen = await page.evaluate(() => {
    const el = document.querySelector('#site-navigation');
    if(!el) return null; const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    const bodyCls = document.body.className;
    return { w: Math.round(r.width), h: Math.round(r.height), disp: cs.display, transform: cs.transform, bodyCls };
  });
  console.log('NAV_OPEN', JSON.stringify(navOpen));
  await ctx.close();

  // --- hero real slide title at 1440 + 390 ---
  for (const vw of [1440, 390]) {
    ctx = await browser.newContext({ viewport: { width: vw, height: 900 } });
    page = await ctx.newPage();
    await page.goto(BASE + '/index.html', { waitUntil: 'networkidle' }).catch(()=>{});
    await page.waitForTimeout(1800);
    const hero = await page.evaluate(() => {
      const sel = ['.pbmit-slider-title','.pbmit-title','.swiper-slide-active h2','.swiper-slide h2','.pbmit-slider-area h1'];
      const out = {};
      for (const s of sel) { const el = document.querySelector(s); if (el) { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); out[s] = { fs: cs.fontSize, lh: cs.lineHeight, w: Math.round(r.width), h: Math.round(r.height), right: Math.round(r.right), t: (el.textContent||'').trim().slice(0,30) }; } }
      const h1 = document.querySelector('h1.pfg-sr-only, .pfg-sr-only');
      return { titles: out, srH1: h1 ? (h1.textContent||'').trim().slice(0,40) : null };
    });
    console.log('HERO_'+vw, JSON.stringify(hero, null, 1));
    await ctx.close();
  }

  await browser.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
