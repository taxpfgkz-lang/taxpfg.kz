# -*- coding: utf-8 -*-
# Идемпотентные a11y-правки в ИСХОДНИКАХ (Track A, 2026-06-20):
#  1) heading-order: декоративные подзаголовки-эйбрау .pbmit-subtitle, размеченные
#     как заголовки <h2>/<h4>, превращаем в <p> (стиль задан КЛАССОМ → вид 1:1).
#  2) label-content-name-mismatch: aria-label у телефонной WhatsApp-ссылки должен
#     содержать видимый текст «+7 707 237 00 50».
# Трогаем: index.html (прямой) + .gsd-build/frag/*.content.html (источники сборки).
# index.html правится здесь же; внутренние страницы пересобирает assemble.py.
import io, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(ROOT, ".gsd-build", "frag")

SUBTITLE_RE = re.compile(r'<(h[24])(\b[^>]*\bpbmit-subtitle\b[^>]*)>(.*?)</\1>', re.DOTALL)
ARIA_OLD = 'aria-label="Написать в WhatsApp"'
ARIA_NEW = 'aria-label="+7 707 237 00 50 — написать в WhatsApp"'

def fix(text):
    n_sub = len(SUBTITLE_RE.findall(text))
    text = SUBTITLE_RE.sub(lambda m: '<p%s>%s</p>' % (m.group(2), m.group(3)), text)
    n_aria = text.count(ARIA_OLD)
    text = text.replace(ARIA_OLD, ARIA_NEW)
    return text, n_sub, n_aria

# landmark-one-main для index.html (внутренние пейджи получают <main> из template.html).
# Идемпотентно: оборачиваем .page-content в <main id="content"> ровно один раз.
def wrap_main_index(text):
    if '<main id="content">' in text:
        return text, 0
    op_old = '\t\t<!-- page content -->\n\t\t<div class="page-content">'
    op_new = '\t\t<!-- page content -->\n\t\t<main id="content">\n\t\t<div class="page-content">'
    cl_old = '\t\t</div>\n\t\t<!-- page content End -->'
    cl_new = '\t\t</div>\n\t\t</main>\n\t\t<!-- page content End -->'
    if op_old in text and cl_old in text:
        text = text.replace(op_old, op_new, 1).replace(cl_old, cl_new, 1)
        return text, 1
    return text, 0

targets = [os.path.join(ROOT, "index.html")] + sorted(glob.glob(os.path.join(FRAG, "*.content.html")))
total_sub = total_aria = 0
for path in targets:
    src = io.open(path, encoding="utf-8").read()
    out, n_sub, n_aria = fix(src)
    n_main = 0
    if os.path.basename(path) == "index.html":
        out, n_main = wrap_main_index(out)
    if out != src:
        io.open(path, "w", encoding="utf-8").write(out)
    total_sub += n_sub; total_aria += n_aria
    rel = os.path.relpath(path, ROOT)
    extra = ("  <main>:%d" % n_main) if os.path.basename(path) == "index.html" else ""
    print("%-40s subtitle→p: %d  aria-label: %d%s%s" % (rel, n_sub, n_aria, extra, "  (изменён)" if out != src else ""))

print("\nИТОГО: подзаголовков конвертировано %d, aria-label исправлено %d" % (total_sub, total_aria))
