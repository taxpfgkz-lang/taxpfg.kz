# -*- coding: utf-8 -*-
# Сборка кастомной 404.html из общего template.html (шапка/подвал = как у сайта).
# Особенности 404: robots=noindex и <base href="/"> — чтобы относительные пути
# к CSS/JS/ссылкам разрешались от корня, даже если хостинг отдаёт 404.html
# по произвольному «глубокому» несуществующему URL.
import io, os, html as _html
from seo_common import seo_head

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, ".gsd-build")
TPL = io.open(os.path.join(BUILD, "template.html"), encoding="utf-8").read()

SLUG = "404"
TITLE = "Страница не найдена (404) — PrimeFinance Group"
DESC = "Запрошенная страница не найдена. Вернитесь на главную PrimeFinance Group или выберите нужный раздел."
H1 = "Страница не найдена"

def esc_title(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def esc_attr(s):  return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

def titlebar(h1):
    crumbs = [
        '<span><a href="index.html">Главная</a></span>',
        '<span class="sep"> / </span>',
        '<span>404</span>',
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

def btn(href, text, variant=""):
    cls = "pbmit-btn" + ((" " + variant) if variant else "")
    return ('<a href="%s" class="%s"><span class="pbmit-button-content-wrapper">'
            '<span class="pbmit-button-text-wrap"><span class="pbmit-button-text">'
            '<span>%s</span></span></span></span></a>' % (href, cls, _html.escape(text)))

CONTENT = (
    '\t\t\t<section class="pfg-section" style="text-align:center;">\n'
    '\t\t\t\t<div class="container">\n'
    '\t\t\t\t\t<div class="pfg-prose" style="max-width:720px;margin:0 auto;">\n'
    '\t\t\t\t\t\t<div class="pbmit-heading-subheading"><p class="pbmit-subtitle" style="justify-content:center;">Ошибка 404</p></div>\n'
    '\t\t\t\t\t\t<div style="font-size:96px;line-height:1;font-weight:800;color:var(--pbmit-global-color);margin:8px 0 18px;">404</div>\n'
    '\t\t\t\t\t\t<h2 style="margin-bottom:16px;">Такой страницы не существует</h2>\n'
    '\t\t\t\t\t\t<p class="pfg-lead">Возможно, ссылка устарела или адрес введён с ошибкой. '
    'Вернитесь на главную или выберите нужный раздел.</p>\n'
    '\t\t\t\t\t\t<div class="pfg-cta-actions" style="justify-content:center;">\n'
    '\t\t\t\t\t\t\t%s\n\t\t\t\t\t\t\t%s\n\t\t\t\t\t\t\t%s\n'
    '\t\t\t\t\t\t</div>\n'
    '\t\t\t\t\t</div>\n'
    '\t\t\t\t</div>\n'
    '\t\t\t</section>'
) % (btn("index.html", "На главную"),
     btn("services.html", "Все услуги", "white"),
     btn("contacts.html", "Контакты", "white"))

page = TPL
page = page.replace("@@TITLE@@", esc_title(TITLE))
page = page.replace("@@DESC@@", esc_attr(DESC))
page = page.replace("@@SEOHEAD@@", seo_head(SLUG, TITLE, DESC))  # без BreadcrumbList
page = page.replace("@@TITLEBAR@@", titlebar(H1))
page = page.replace("@@CONTENT@@", CONTENT)

# 404-специфика: noindex + <base href="/"> для разрешения относительных путей от корня.
page = page.replace('<meta name="robots" content="index, follow">',
                    '<meta name="robots" content="noindex, follow">')
page = page.replace('<meta charset="utf-8">',
                    '<meta charset="utf-8">\n\t\t<base href="/">', 1)

leftover = [p for p in ("@@TITLE@@","@@DESC@@","@@SEOHEAD@@","@@TITLEBAR@@","@@CONTENT@@") if p in page]
assert not leftover, "остались плейсхолдеры %s" % leftover
assert 'content="noindex, follow"' in page, "robots noindex не применён"
assert '<base href="/">' in page, "<base> не вставлен"

io.open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(page)
print("=== СОБРАНО ===\n404.html  noindex=да  base=да  кнопок=3")
