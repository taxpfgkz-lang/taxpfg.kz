# -*- coding: utf-8 -*-
# Генерация sitemap.xml с ПЕР-ФАЙЛОВЫМ lastmod.
# Источник даты: последний git-коммит, затронувший файл (git log -1 --format=%cs),
# fallback — mtime файла. Идемпотентно: повторный прогон при тех же датах не меняет файл.
import io, os, subprocess, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://taxpfg.kz"

# (файл, loc, changefreq, priority) — порядок и приоритеты сохранены из прежнего sitemap.
PAGES = [
    ("index.html",               BASE + "/",                         "monthly", "1.0"),
    ("services.html",            BASE + "/services.html",            "monthly", "0.9"),
    ("contacts.html",            BASE + "/contacts.html",            "monthly", "0.9"),
    ("accounting.html",          BASE + "/accounting.html",          "monthly", "0.8"),
    ("taxes.html",               BASE + "/taxes.html",               "monthly", "0.8"),
    ("registration.html",        BASE + "/registration.html",        "monthly", "0.8"),
    ("accounting-recovery.html", BASE + "/accounting-recovery.html", "monthly", "0.8"),
    ("consulting.html",          BASE + "/consulting.html",          "monthly", "0.8"),
    ("about.html",               BASE + "/about.html",               "monthly", "0.7"),
    ("privacy.html",             BASE + "/privacy.html",             "monthly", "0.3"),
]

def lastmod(fname):
    path = os.path.join(ROOT, fname)
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", fname],
            cwd=ROOT, stderr=subprocess.DEVNULL).decode("utf-8", "replace").strip()
        if out:
            return out
    except Exception:
        pass
    return time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(path)))

rows = []
for fname, loc, freq, pri in PAGES:
    lm = lastmod(fname)
    rows.append(
        "  <url>\n"
        "    <loc>%s</loc>\n"
        "    <lastmod>%s</lastmod>\n"
        "    <changefreq>%s</changefreq>\n"
        "    <priority>%s</priority>\n"
        "  </url>" % (loc, lm, freq, pri))

xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
       + "\n".join(rows) + "\n</urlset>\n")

out_path = os.path.join(ROOT, "sitemap.xml")
prev = io.open(out_path, encoding="utf-8").read() if os.path.exists(out_path) else ""
if xml != prev:
    io.open(out_path, "w", encoding="utf-8", newline="\n").write(xml)
    print("sitemap.xml ОБНОВЛЁН")
else:
    print("sitemap.xml без изменений")
for fname, loc, freq, pri in PAGES:
    print("  %-28s lastmod=%s" % (fname, lastmod(fname)))
