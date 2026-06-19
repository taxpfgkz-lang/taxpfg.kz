# -*- coding: utf-8 -*-
# Автономная сборка ОДНОЙ страницы privacy.html из эталонного template.html.
# Не трогает остальные страницы. Header/footer берутся из template (= index.html).
import io, os, re, sys, html as _html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, ".gsd-build")
FRAG = os.path.join(BUILD, "frag")
TPL = io.open(os.path.join(BUILD, "template.html"), encoding="utf-8").read()

SLUG = "privacy"

def esc_title(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def esc_attr(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

def titlebar(h1):
    # Обычная страница: Главная / <H1>  (без родителя «Услуги»)
    crumbs = [
        '<span><a href="index.html">Главная</a></span>',
        '<span class="sep"> / </span>',
        '<span>%s</span>' % _html.escape(h1),
    ]
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
    s = re.sub(r'^```[a-zA-Z]*\n', '', s)
    s = re.sub(r'\n```$', '', s)
    return s.strip()

cpath = os.path.join(FRAG, SLUG + ".content.html")
mpath = os.path.join(FRAG, SLUG + ".meta.txt")
assert os.path.exists(cpath), "НЕТ %s" % cpath
assert os.path.exists(mpath), "НЕТ %s" % mpath

content = clean_fragment(io.open(cpath, encoding="utf-8").read())
meta = [l.strip() for l in io.open(mpath, encoding="utf-8").read().splitlines() if l.strip()]
assert len(meta) >= 3, "meta.txt < 3 непустых строк (%d)" % len(meta)
title, desc, h1 = meta[0], meta[1], meta[2]

problems = []
for bad in ["<!doctype", "<html", "<head", "<body", "<header", "<footer", "pbmit-title-bar-wrapper"]:
    if bad in content.lower():
        problems.append("в контенте обнаружен запрещённый фрагмент оболочки %r" % bad)
if problems:
    print("=== ПРОБЛЕМЫ ===\n" + "\n".join(problems)); sys.exit(1)

page = TPL
assert page.count("@@TITLE@@") == 1 and page.count("@@DESC@@") == 1
assert page.count("@@TITLEBAR@@") == 1 and page.count("@@CONTENT@@") == 1
page = page.replace("@@TITLE@@", esc_title(title))
page = page.replace("@@DESC@@", esc_attr(desc))
page = page.replace("@@TITLEBAR@@", titlebar(h1))
page = page.replace("@@CONTENT@@", content)
leftover = [p for p in ("@@TITLE@@","@@DESC@@","@@TITLEBAR@@","@@CONTENT@@") if p in page]
assert not leftover, "остались плейсхолдеры %s" % leftover

io.open(os.path.join(ROOT, SLUG + ".html"), "w", encoding="utf-8").write(page)
print("=== СОБРАНО ===")
print("%-14s title=%r words=%d" % (SLUG + ".html", title[:60], len(content.split())))
