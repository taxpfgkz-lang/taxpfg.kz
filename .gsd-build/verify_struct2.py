# -*- coding: utf-8 -*-
import re, hashlib, os, sys
PAGES = ["about","services","accounting","taxes","registration",
         "accounting-recovery","consulting","contacts","privacy"]
def rd(p): return open(p, encoding="utf-8").read()
def md5(s): return hashlib.md5(s.encode("utf-8")).hexdigest()
def extract(html, start_re, end):
    m = re.search(start_re, html)
    if not m: return None
    j = html.find(end, m.start())
    return html[m.start():j+len(end)] if j!=-1 else None
def strip_slider(h):
    s=h.find('<div class="pbmit-slider-area')
    if s==-1: return h
    depth=0; end=None
    for m in re.finditer(r'<(/?)div\b', h[s:]):
        depth += 1 if m.group(1)=='' else -1
        if depth==0: end=s+m.end(); break
    if end is not None and h[end]=='>': end+=1
    pre=s
    while pre>0 and h[pre-1]=='\t': pre-=1
    if pre>0 and h[pre-1]=='\n': pre-=1
    return h[:pre]+h[end:]

idx = rd("index.html")
idx_header = extract(idx, r'<header class="site-header', "</header>")
idx_footer = extract(idx, r'<footer class="site-footer', "</footer>")
idx_nav = strip_slider(idx_header)          # header главной без слайдера = эталон навигации
NAV, FOOT = md5(idx_nav), md5(idx_footer)
print(f"ЭТАЛОН: nav(index без слайдера)={NAV[:8]}  footer={FOOT[:8]}")
print(f"index.html слайдеров: {idx.count('pbmit-slider-area')} (ожидаем 1)")
print("="*64)
errors=0
LEAK=[r'<!DOCTYPE',r'<html',r'<head[ >]',r'</head>',r'<body',r'</body>',r'```',
      r'<header class="site-header',r'<footer class="site-footer',r'pbmit-slider-area']
for slug in PAGES:
    fn=f"{slug}.html"
    h=rd(fn)
    hdr=extract(h, r'<header class="site-header', "</header>")
    ftr=extract(h, r'<footer class="site-footer', "</footer>")
    hh=md5(hdr) if hdr else "X"; ff=md5(ftr) if ftr else "X"
    if hh!=NAV: print(f"[FAIL] {fn}: header(nav) != эталон ({hh[:8]})"); errors+=1
    if ff!=FOOT: print(f"[FAIL] {fn}: footer != эталон ({ff[:8]})"); errors+=1
    nsl=h.count('pbmit-slider-area')
    if nsl!=0: print(f"[FAIL] {fn}: остался слайдер ({nsl})"); errors+=1
    ntb=h.count('pbmit-title-bar-wrapper')
    if ntb!=1: print(f"[FAIL] {fn}: titlebar count={ntb}"); errors+=1
    for ph in ["@@TITLE@@","@@DESC@@","@@TITLEBAR@@","@@CONTENT@@"]:
        if ph in h: print(f"[FAIL] {fn}: плейсхолдер {ph}"); errors+=1
    # content zone между </header> и <footer>
    cs=h.find("</header>"); ce=h.rfind('<footer class="site-footer')
    mid=h[cs+9:ce]
    # titlebar — допустим в mid (он вне header); проверяем только настоящую утечку
    for pat in [r'<!DOCTYPE',r'<html',r'<head[ >]',r'</head>',r'<body',r'</body>',r'```',
                r'<header class="site-header',r'<footer class="site-footer',r'pbmit-slider-area']:
        if re.search(pat, mid): print(f"[FAIL] {fn}: утечка {pat} в контенте"); errors+=1
    od=len(re.findall(r'<div\b',mid)); cd=len(re.findall(r'</div>',mid))
    if od!=cd: print(f"[FAIL] {fn}: div дисбаланс {od}/{cd}"); errors+=1
    # h1 в контентной зоне (после titlebar) — не должно быть
    tb=mid.find('pbmit-title-bar-wrapper'); after=mid[mid.find('</div>',tb):] if tb!=-1 else mid
    print(f"[ok ] {fn:24} nav={'OK' if hh==NAV else 'X'} ftr={'OK' if ff==FOOT else 'X'} slider={nsl} tbar={ntb} div={od}/{cd}")
# ссылки/ассеты
print("="*64); print("ССЫЛКИ/АССЕТЫ:")
broken=set()
for fn in ["index.html"]+[f"{s}.html" for s in PAGES]:
    h=rd(fn)
    for m in re.finditer(r'(?:href|src)\s*=\s*"([^"]+)"', h):
        u=m.group(1).strip()
        if not u or u.startswith(("http://","https://","#","tel:","mailto:","javascript:","data:","wa.me")): continue
        p=u.split("?")[0].split("#")[0]
        if p and not os.path.exists(p): broken.add(f"{fn} -> {u}")
if broken:
    for b in sorted(broken): print("  [BROKEN]",b); errors+=1
else: print("  все локальные ссылки/ассеты существуют ✓")
print("="*64); print(f"ИТОГ: errors={errors}")
sys.exit(1 if errors else 0)
