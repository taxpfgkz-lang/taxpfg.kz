# -*- coding: utf-8 -*-
import re, hashlib, os, sys, glob

PAGES = ["about","services","accounting","taxes","registration",
         "accounting-recovery","consulting","contacts"]

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

def md5(s): return hashlib.md5(s.encode("utf-8")).hexdigest()

def extract(html, start_re, end_marker):
    m = re.search(start_re, html)
    if not m: return None
    i = m.start()
    j = html.find(end_marker, i)
    if j == -1: return None
    return html[i:j+len(end_marker)]

idx = read("index.html")
# header: from <header ...id="masthead"> до конца </header>
idx_header = extract(idx, r'<header class="site-header', "</header>")
idx_footer = extract(idx, r'<footer class="site-footer', "</footer>")
assert idx_header and idx_footer, "не нашёл эталонный header/footer в index.html"
H, F = md5(idx_header), md5(idx_footer)
print(f"ЭТАЛОН index.html: header={H[:8]} footer={F[:8]}")
print("="*60)

# собрать список существующих файлов для проверки ссылок
existing_files = set(os.listdir("."))
errors = 0
warnings = 0

# регэкспы для shell-утечки в контенте
LEAK = [r'<!DOCTYPE', r'<html', r'<head[ >]', r'</head>', r'<body', r'</body>',
        r'```', r'<header class="site-header', r'<footer class="site-footer']

for slug in PAGES:
    fn = f"{slug}.html"
    if not os.path.exists(fn):
        print(f"[FAIL] {fn}: файл отсутствует"); errors+=1; continue
    html = read(fn)
    row = [fn]

    # 1. header/footer идентичность
    h = extract(html, r'<header class="site-header', "</header>")
    f_ = extract(html, r'<footer class="site-footer', "</footer>")
    hh = md5(h) if h else "MISSING"
    ff = md5(f_) if f_ else "MISSING"
    hok = (hh==H); fok=(ff==F)
    if not hok: print(f"[FAIL] {fn}: header отличается ({hh[:8]})"); errors+=1
    if not fok: print(f"[FAIL] {fn}: footer отличается ({ff[:8]})"); errors+=1

    # 2. ровно один header / footer / title-bar
    nh = len(re.findall(r'<header class="site-header', html))
    nf = len(re.findall(r'<footer class="site-footer', html))
    ntb = len(re.findall(r'pbmit-title-bar-wrapper', html))
    if nh!=1: print(f"[FAIL] {fn}: header count={nh}"); errors+=1
    if nf!=1: print(f"[FAIL] {fn}: footer count={nf}"); errors+=1
    if ntb<1: print(f"[FAIL] {fn}: нет titlebar"); errors+=1

    # 3. плейсхолдеры не остались
    for ph in ["@@TITLE@@","@@DESC@@","@@TITLEBAR@@","@@CONTENT@@"]:
        if ph in html: print(f"[FAIL] {fn}: остался плейсхолдер {ph}"); errors+=1

    # 4. shell-утечка внутри content (между </header> и <footer>)
    cs = html.find("</header>"); ce = html.rfind('<footer class="site-footer')
    body_mid = html[cs+9:ce] if (cs!=-1 and ce!=-1) else ""
    for pat in LEAK:
        if re.search(pat, body_mid):
            print(f"[FAIL] {fn}: shell-утечка в контенте: {pat}"); errors+=1

    # 5. баланс div в полном документе
    od = len(re.findall(r'<div\b', html)); cd = len(re.findall(r'</div>', html))
    if od!=cd: print(f"[WARN] {fn}: div баланс open={od} close={cd}"); warnings+=1

    # 6. div баланс ВНУТРИ контента (между </header> и <footer>)
    od2 = len(re.findall(r'<div\b', body_mid)); cd2 = len(re.findall(r'</div>', body_mid))
    if od2!=cd2: print(f"[FAIL] {fn}: div дисбаланс в контенте open={od2} close={cd2}"); errors+=1

    print(f"[ok ] {fn:24} hdr={'OK' if hok else 'X'} ftr={'OK' if fok else 'X'} "
          f"tbar={ntb} div(content)={od2}/{cd2}")

print("="*60)
# проверка всех внутренних ссылок и локальных ассетов на всех страницах + index
print("ПРОВЕРКА ССЫЛОК И АССЕТОВ:")
broken = set()
all_pages = ["index.html"]+[f"{s}.html" for s in PAGES]
for fn in all_pages:
    if not os.path.exists(fn): continue
    html = read(fn)
    # href и src, только локальные (не http, не #, не tel/mailto/wa)
    for m in re.finditer(r'(?:href|src)\s*=\s*"([^"]+)"', html):
        url = m.group(1).strip()
        if not url or url.startswith(("http://","https://","#","tel:","mailto:","javascript:","data:","wa.me")):
            continue
        path = url.split("?")[0].split("#")[0]
        if path == "" : continue
        if not os.path.exists(path):
            broken.add(f"{fn} -> {url}")

if broken:
    for b in sorted(broken): print(f"  [BROKEN] {b}"); errors+=1
else:
    print("  все локальные ссылки/ассеты существуют ✓")

print("="*60)
print(f"ИТОГ: errors={errors} warnings={warnings}")
sys.exit(1 if errors else 0)
