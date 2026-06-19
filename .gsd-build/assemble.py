# -*- coding: utf-8 -*-
# Детерминированная сборка внутренних страниц: template.html + фрагменты -> <slug>.html
import io, os, re, sys, html as _html
from seo_common import seo_head

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, ".gsd-build")
FRAG = os.path.join(BUILD, "frag")
TPL = io.open(os.path.join(BUILD, "template.html"), encoding="utf-8").read()

# parent breadcrumb: service-detail -> Услуги
SERVICE_DETAIL = {"accounting", "taxes", "registration", "accounting-recovery", "consulting"}
PAGES = ["about", "services", "accounting", "taxes", "registration",
         "accounting-recovery", "consulting", "contacts"]

def esc_title(s):  # для <title> (текстовый узел)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def esc_attr(s):   # для content="..."
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

def titlebar(h1, slug):
    crumbs = ['<span><a href="index.html">Главная</a></span>']
    if slug in SERVICE_DETAIL:
        crumbs.append('<span class="sep"> / </span>')
        crumbs.append('<span><a href="services.html">Услуги</a></span>')
    crumbs.append('<span class="sep"> / </span>')
    crumbs.append('<span>%s</span>' % _html.escape(h1))
    return (
        '<!-- Titlebar -->\n'
        '\t\t<div class="pbmit-title-bar-wrapper">\n'
        '\t\t\t<div class="pbmit-title-bar-content">\n'
        '\t\t\t\t<div class="container">\n'
        '\t\t\t\t\t<div class="pbmit-title-bar-content-inner">\n'
        '\t\t\t\t\t\t<div class="pbmit-tbar"><h1 class="pbmit-tbar-title">%s</h1></div>\n'
        '\t\t\t\t\t\t<div class="pbmit-breadcrumb">%s</div>\n'
        '\t\t\t\t\t</div>\n'
        '\t\t\t\t</div>\n'
        '\t\t\t</div>\n'
        '\t\t</div>' % (_html.escape(h1), "".join(crumbs))
    )

def clean_fragment(s):
    s = s.strip()
    # снять случайные markdown-ограждения
    s = re.sub(r'^```[a-zA-Z]*\n', '', s)
    s = re.sub(r'\n```$', '', s)
    return s.strip()

problems = []
built = []
for slug in PAGES:
    cpath = os.path.join(FRAG, slug + ".content.html")
    mpath = os.path.join(FRAG, slug + ".meta.txt")
    if not os.path.exists(cpath) or not os.path.exists(mpath):
        problems.append("%s: НЕТ фрагмента (content=%s meta=%s)" % (slug, os.path.exists(cpath), os.path.exists(mpath)))
        continue
    content = clean_fragment(io.open(cpath, encoding="utf-8").read())
    meta = [l.strip() for l in io.open(mpath, encoding="utf-8").read().splitlines() if l.strip()]
    if len(meta) < 3:
        problems.append("%s: meta.txt < 3 непустых строк (%d)" % (slug, len(meta)))
        continue
    title, desc, h1 = meta[0], meta[1], meta[2]
    # запрет «протёкшей» оболочки в контенте
    for bad in ["<!doctype", "<html", "<head", "<body", "<header", "<footer", "pbmit-title-bar-wrapper"]:
        if bad in content.lower():
            problems.append("%s: в контенте обнаружен запрещённый фрагмент оболочки %r" % (slug, bad))
    page = TPL
    assert page.count("@@TITLE@@") == 1 and page.count("@@DESC@@") == 1
    assert page.count("@@TITLEBAR@@") == 1 and page.count("@@CONTENT@@") == 1
    assert page.count("@@SEOHEAD@@") == 1
    page = page.replace("@@TITLE@@", esc_title(title))
    page = page.replace("@@DESC@@", esc_attr(desc))
    page = page.replace("@@SEOHEAD@@", seo_head(slug, title, desc))
    page = page.replace("@@TITLEBAR@@", titlebar(h1, slug))
    page = page.replace("@@CONTENT@@", content)
    # не должно остаться плейсхолдеров
    leftover = [p for p in ("@@TITLE@@","@@DESC@@","@@SEOHEAD@@","@@TITLEBAR@@","@@CONTENT@@") if p in page]
    if leftover:
        problems.append("%s: остались плейсхолдеры %s" % (slug, leftover)); continue
    io.open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8").write(page)
    built.append("%-22s title=%r words≈%d" % (slug + ".html", title[:48], len(content.split())))

print("=== СОБРАНО ===")
print("\n".join(built) if built else "(ничего)")
if problems:
    print("\n=== ПРОБЛЕМЫ ===")
    print("\n".join(problems))
    sys.exit(1 if len(built) < len(PAGES) else 0)
print("\nИтого страниц: %d/%d" % (len(built), len(PAGES)))
