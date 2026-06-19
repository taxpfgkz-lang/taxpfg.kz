# -*- coding: utf-8 -*-
# Общий генератор SEO-блока (@@SEOHEAD@@) для ассемблеров. Единый источник истины,
# совпадает с seo_stage5.py. JSON-LD — только подтверждённые факты.
import json

BASE = "https://taxpfg.kz"
OG_IMAGE = BASE + "/images/slider1-01.jpg"  # [PFG] временный, заменить на Этапе 4

JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "AccountingService",
    "@id": BASE + "/#organization",
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

def canon(slug):
    return BASE + "/" if slug == "index" else "%s/%s.html" % (BASE, slug)

def _attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

def seo_head(slug, title, desc):
    c = canon(slug); ta = _attr(title); da = _attr(desc)
    return "\n".join([
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
    ])
