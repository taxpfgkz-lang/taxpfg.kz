# -*- coding: utf-8 -*-
# Этап 5 (SEO/техничка): синхронизация title/description под эталон SITE_CONTENT.md
# + canonical/OpenGraph/Twitter/JSON-LD на все страницы. Идемпотентно (пропускает уже обработанные).
import io, os, re, sys, json, html as _H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SC = io.open(os.path.join(ROOT, "docs", "SITE_CONTENT.md"), encoding="utf-8").read()
BASE = "https://taxpfg.kz"
OG_IMAGE = BASE + "/images/slider1-01.jpg"  # [PFG] временный, см. коммент в head

# --- эталонные SEO из SITE_CONTENT.md в порядке появления ---
titles = re.findall(r'^-\s*\*\*Title:\*\*\s*(.+?)\s*$', SC, re.M)
descs  = re.findall(r'^-\s*\*\*Description:\*\*\s*(.+?)\s*$', SC, re.M)
assert len(titles) == 9 and len(descs) == 9, "Ожидал 9 Title/9 Description, нашёл %d/%d" % (len(titles), len(descs))
CONTENT_PAGES = ["index","about","services","accounting","taxes","registration",
                 "accounting-recovery","consulting","contacts"]
SEO = {slug: (titles[i], descs[i]) for i, slug in enumerate(CONTENT_PAGES)}
# privacy в SITE_CONTENT нет — оставляем уже имеющиеся title/desc страницы
ALL_PAGES = CONTENT_PAGES + ["privacy"]

def canon(slug):
    return BASE + "/" if slug == "index" else "%s/%s.html" % (BASE, slug)

def esc_text(s):  # текстовый узел <title>
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def esc_attr(s):  # значение content="..."
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

# единый JSON-LD: только подтверждённые факты (без БИН/e-mail/часов)
JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "AccountingService",
    "name": "PrimeFinance Group",
    "url": BASE + "/",
    "telephone": "+77072370050",
    "areaServed": "Алматы",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "проспект Абая, 68/74, БЦ «AVENUE CITY», офис 39",
        "addressLocality": "Алматы",
        "addressCountry": "KZ"
    }
}, ensure_ascii=False, separators=(",", ":"))

VIEWPORT = '\t\t<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">'

def seo_block(slug, title, desc):
    c = canon(slug); ta = esc_attr(title); da = esc_attr(desc)
    L = [
        '\t\t<!-- SEO: canonical / OpenGraph / Twitter / JSON-LD (Этап 5) -->',
        '\t\t<link rel="canonical" href="%s">' % c,
        '\t\t<meta property="og:type" content="website">',
        '\t\t<meta property="og:site_name" content="PrimeFinance Group">',
        '\t\t<meta property="og:locale" content="ru_RU">',
        '\t\t<meta property="og:title" content="%s">' % ta,
        '\t\t<meta property="og:description" content="%s">' % da,
        '\t\t<meta property="og:url" content="%s">' % c,
        '\t\t<!-- [PFG] og:image временный (кадр hero); заменить на брендовый 1200x630 на Этапе 4 -->',
        '\t\t<meta property="og:image" content="%s">' % OG_IMAGE,
        '\t\t<meta name="twitter:card" content="summary_large_image">',
        '\t\t<meta name="twitter:title" content="%s">' % ta,
        '\t\t<meta name="twitter:description" content="%s">' % da,
        '\t\t<meta name="twitter:image" content="%s">' % OG_IMAGE,
        '\t\t<script type="application/ld+json">%s</script>' % JSONLD,
    ]
    return "\n".join(L)

report = []
for slug in ALL_PAGES:
    fn = os.path.join(ROOT, slug + ".html")
    h = io.open(fn, encoding="utf-8").read()
    changed = []

    # 1) title/description под эталон (если страница есть в SITE_CONTENT)
    if slug in SEO:
        t, d = SEO[slug]
        nt = re.subn(r'<title>.*?</title>', '<title>%s</title>' % esc_text(t), h, count=1, flags=re.S)
        h, c1 = nt
        assert c1 == 1, "%s: <title> не найден" % slug
        nd = re.subn(r'<meta name="description" content="[^"]*">',
                     '<meta name="description" content="%s">' % esc_attr(d), h, count=1)
        h, c2 = nd
        assert c2 == 1, "%s: meta description не найден" % slug
        changed.append("title+desc")

    # 2) SEO-блок (идемпотентно): только если canonical ещё нет
    if 'rel="canonical"' in h:
        report.append("%-26s ПРОПУСК (canonical уже есть)%s" % (slug+".html", " [+"+",".join(changed)+"]" if changed else ""))
        if changed:  # title/desc всё равно могли обновиться — записываем
            io.open(fn, "w", encoding="utf-8").write(h)
        continue
    # для title/desc блока берём актуальные значения из файла (privacy — свои)
    mt = re.search(r'<title>(.*?)</title>', h, re.S); md = re.search(r'<meta name="description" content="([^"]*)">', h)
    cur_title = _H.unescape(mt.group(1)) if mt else ""
    cur_desc  = _H.unescape(md.group(1)) if md else ""
    block = seo_block(slug, cur_title, cur_desc)
    nb = h.replace(VIEWPORT, VIEWPORT + "\n" + block, 1)
    assert nb != h, "%s: якорь viewport не найден (вставка SEO-блока)" % slug
    h = nb
    changed.append("seo-block")
    io.open(fn, "w", encoding="utf-8").write(h)
    report.append("%-26s OK [%s]" % (slug+".html", ",".join(changed)))

print("=== SEO применён ===")
print("\n".join(report))
print("\nJSON-LD:", JSONLD[:80], "...")
