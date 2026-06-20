# -*- coding: utf-8 -*-
# Идемпотентно проставляет loading="lazy" decoding="async" всем <img>, у которых
# ещё нет loading=. Все <img> сайта — ниже первого экрана (LCP-герой титлбара —
# CSS-фон, не <img>), поэтому ленивую загрузку можно включить для всех.
# Источники: index.html (прямой) + .gsd-build/frag/*.content.html → пересборка assemble.py.
import io, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(ROOT, ".gsd-build", "frag")
IMG_RE = re.compile(r'<img(?![^>]*\bloading=)([^>]*?)>', re.IGNORECASE)

targets = [os.path.join(ROOT, "index.html")] + sorted(glob.glob(os.path.join(FRAG, "*.content.html")))
total = 0
for path in targets:
    src = io.open(path, encoding="utf-8").read()
    n = len(IMG_RE.findall(src))
    if n:
        out = IMG_RE.sub(lambda m: '<img loading="lazy" decoding="async"%s>' % m.group(1), src)
        io.open(path, "w", encoding="utf-8").write(out)
        total += n
        print("%-40s img+lazy: %d" % (os.path.relpath(path, ROOT), n))
print("ИТОГО проставлено loading=lazy: %d" % total)
