# -*- coding: utf-8 -*-
# Этап 4: патч og:image/twitter:image/JSON-LD в index.html (ручная страница со слайдером).
# Идемпотентно: повторный запуск — no-op. Отступ берётся из существующей строки og:image.
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "index.html")
NEW = "https://taxpfg.kz/images/og-image.jpg"
OLD = "https://taxpfg.kz/images/slider1-01.jpg"
ALT = "PrimeFinance Group — бухгалтерия, налоги и право в Алматы"

s = io.open(P, encoding="utf-8").read()
orig = s

if ('property="og:image" content="%s"' % NEW) in s:
    print("index.html: уже пропатчен (og-image.jpg) — пропуск")
    sys.exit(0)

# отступ строки og:image
m = re.search(r'^([ \t]*)<meta property="og:image" content="%s">' % re.escape(OLD), s, re.M)
if not m:
    print("index.html: не найдена строка og:image со slider1-01 — НЕ ОЖИДАНО"); sys.exit(1)
ind = m.group(1)

# 1) убрать временный [PFG]-комментарий над og:image
s = re.sub(r'[ \t]*<!-- \[PFG\] og:image[^\n]*-->\n', '', s, count=1)

# 2) og:image -> брендовый + width/height/alt
old_og = '%s<meta property="og:image" content="%s">' % (ind, OLD)
new_og = "\n".join([
    '%s<meta property="og:image" content="%s">' % (ind, NEW),
    '%s<meta property="og:image:width" content="1200">' % ind,
    '%s<meta property="og:image:height" content="630">' % ind,
    '%s<meta property="og:image:alt" content="%s">' % (ind, ALT),
])
assert s.count(old_og) == 1, "og:image: ожидалось 1 вхождение"
s = s.replace(old_og, new_og)

# 3) twitter:image
tw_old = '<meta name="twitter:image" content="%s">' % OLD
tw_new = '<meta name="twitter:image" content="%s">' % NEW
assert s.count(tw_old) == 1, "twitter:image: ожидалось 1 вхождение"
s = s.replace(tw_old, tw_new)

# 4) JSON-LD: image после url
ld_old = '"url":"https://taxpfg.kz/","telephone"'
ld_new = '"url":"https://taxpfg.kz/","image":"%s","telephone"' % NEW
assert s.count(ld_old) == 1, "JSON-LD url->telephone: ожидалось 1 вхождение"
s = s.replace(ld_old, ld_new)

assert OLD not in s.split("<body")[0], "в <head> остался slider1-01 (og)"
io.open(P, "w", encoding="utf-8").write(s)
print("index.html: og:image -> og-image.jpg (+width/height/alt), twitter:image, JSON-LD image — OK")
