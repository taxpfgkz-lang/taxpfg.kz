# -*- coding: utf-8 -*-
# Общий генератор SEO-блока (@@SEOHEAD@@) для ассемблеров. Единый источник истины,
# совпадает с seo_stage5.py. JSON-LD — только подтверждённые факты.
import json

BASE = "https://taxpfg.kz"
OG_IMAGE = BASE + "/images/og-image.jpg"  # брендовый превью 1200x630 (Этап 4)
OG_IMAGE_W = "1200"
OG_IMAGE_H = "630"
OG_IMAGE_ALT = "PrimeFinance Group — бухгалтерия, налоги и право в Алматы"

JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "AccountingService",
    "@id": BASE + "/#organization",
    "name": "PrimeFinance Group",
    "url": BASE + "/",
    "image": OG_IMAGE,
    "telephone": "+77072370050",
    "areaServed": "Алматы",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "проспект Абая, 68/74, БЦ «AVENUE CITY», офис 39",
        "addressLocality": "Алматы",
        "addressCountry": "KZ"
    }
}, ensure_ascii=False, separators=(",", ":"))

def canon(slug):
    return BASE + "/" if slug == "index" else "%s/%s.html" % (BASE, slug)

def _attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

def breadcrumb_jsonld(crumbs):
    # crumbs: список (name, url) — порядок = видимые хлебные крошки (Главная / … / Текущая).
    items = [{"@type": "ListItem", "position": i, "name": name, "item": url}
             for i, (name, url) in enumerate(crumbs, start=1)]
    data = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": items}, ensure_ascii=False, separators=(",", ":"))
    return '\t\t<script type="application/ld+json">%s</script>' % data

def seo_head(slug, title, desc, crumbs=None):
    c = canon(slug); ta = _attr(title); da = _attr(desc)
    lines = [
        '\t\t<!-- SEO: canonical / OpenGraph / Twitter / JSON-LD (Этап 5) -->',
        '\t\t<link rel="canonical" href="%s">' % c,
        '\t\t<meta property="og:type" content="website">',
        '\t\t<meta property="og:site_name" content="PrimeFinance Group">',
        '\t\t<meta property="og:locale" content="ru_RU">',
        '\t\t<meta property="og:title" content="%s">' % ta,
        '\t\t<meta property="og:description" content="%s">' % da,
        '\t\t<meta property="og:url" content="%s">' % c,
        '\t\t<meta property="og:image" content="%s">' % OG_IMAGE,
        '\t\t<meta property="og:image:width" content="%s">' % OG_IMAGE_W,
        '\t\t<meta property="og:image:height" content="%s">' % OG_IMAGE_H,
        '\t\t<meta property="og:image:alt" content="%s">' % _attr(OG_IMAGE_ALT),
        '\t\t<meta name="twitter:card" content="summary_large_image">',
        '\t\t<meta name="twitter:title" content="%s">' % ta,
        '\t\t<meta name="twitter:description" content="%s">' % da,
        '\t\t<meta name="twitter:image" content="%s">' % OG_IMAGE,
        '\t\t<script type="application/ld+json">%s</script>' % JSONLD,
    ]
    if crumbs:
        lines.append(breadcrumb_jsonld(crumbs))
    return "\n".join(lines)
