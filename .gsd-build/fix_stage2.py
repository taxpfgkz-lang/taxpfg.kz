# -*- coding: utf-8 -*-
import io, os, re, sys

ROOT = os.getcwd()
BUILD = os.path.join(ROOT, ".gsd-build")
FRAG = os.path.join(BUILD, "frag")
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8").write(s)

log = []
def expect(cond, msg):
    if not cond:
        print("ОШИБКА:", msg); sys.exit(2)
    log.append("ok: "+msg)

def remove_slider(t):
    start = t.find('<div class="pbmit-slider-area')
    expect(start != -1, "найден slider-area")
    depth = 0; end = None
    for m in re.finditer(r'<(/?)div\b', t[start:]):
        if m.group(1) == '': depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = start + m.end(); break
    expect(end is not None, "найден конец slider-блока")
    # включить закрывающий '>'
    if t[end] == '>': end += 1
    # съесть ведущий перевод строки + табы
    pre = start
    while pre > 0 and t[pre-1] in '\t': pre -= 1
    if pre > 0 and t[pre-1] == '\n': pre -= 1
    new = t[:pre] + t[end:]
    expect('pbmit-slider-area' not in new, "slider-area удалён полностью")
    expect(new[pre:pre+12].lstrip().startswith('</header>') or '</header>' in new[pre:pre+40],
           "после удаления слайдера сразу </header>")
    return new

def repl(t, old, new, n):
    c = t.count(old)
    expect(c == n, f"замена {old[:40]!r}: ожидалось {n}, найдено {c}")
    return t.replace(old, new)

SHARED = [
    ('<h1>Нужна консультация?</h1>', '<h2>Нужна консультация?</h2>', 1),
    ('placeholder="Search …"', 'placeholder="Поиск …"', 1),
    ('title="Search"', 'title="Поиск"', 2),
    ('<a href="https://wa.me/77072370050" style="color:inherit">',
     '<a href="https://wa.me/77072370050" style="color:inherit" aria-label="Написать в WhatsApp">', 1),
]

# ---- 1. template.html: slider + shared ----
tp = os.path.join(BUILD, "template.html")
t = rd(tp)
t = remove_slider(t)
for old, new, n in SHARED: t = repl(t, old, new, n)
wr(tp, t)
print("template.html: слайдер вырезан + общие правки применены")

# ---- 2. index.html: shared only (слайдер остаётся!) ----
ip = os.path.join(ROOT, "index.html")
ix = rd(ip)
expect(ix.count('pbmit-slider-area') == 1, "index.html сохраняет hero-слайдер")
for old, new, n in SHARED: ix = repl(ix, old, new, n)
wr(ip, ix)
print("index.html: общие правки применены (слайдер сохранён)")

# ---- 3. contacts fragment: политика + required ----
cf = os.path.join(FRAG, "contacts.content.html")
c = rd(cf)
old_consent = '<label class="pfg-consent"><input type="checkbox" name="consent"> <span>Согласен на обработку персональных данных <!-- [PFG] ссылка на политику конфиденциальности — добавить после данных клиента --></span></label>'
new_consent = '<label class="pfg-consent"><input type="checkbox" name="consent" required> <span>Согласен на обработку персональных данных в соответствии с <a href="#privacy" class="pfg-policy-link">политикой конфиденциальности</a><!-- [PFG] заменить #privacy на реальную страницу/документ политики (Этап 3) --></span></label>'
c = repl(c, old_consent, new_consent, 1)
c = repl(c, '<input type="text" name="name" class="form-control" placeholder="Ваше имя">',
            '<input type="text" name="name" class="form-control" placeholder="Ваше имя" required>', 1)
c = repl(c, '<input type="tel" name="phone" class="form-control" placeholder="+7 ___ ___ __ __">',
            '<input type="tel" name="phone" class="form-control" placeholder="+7 ___ ___ __ __" required>', 1)
wr(cf, c)
print("contacts fragment: ссылка на политику + required (name/phone/consent)")

# ---- 4. services fragment: эйчброу h2 -> h4 ----
sf = os.path.join(FRAG, "services.content.html")
s = rd(sf)
if '<h2 class="pbmit-subtitle">наши услуги</h2>' in s:
    s = repl(s, '<h2 class="pbmit-subtitle">наши услуги</h2>', '<h4 class="pbmit-subtitle">Наши услуги</h4>', 1)
    wr(sf, s); print("services fragment: эйчброу h2->h4 'Наши услуги'")
else:
    print("services fragment: строка эйчброу не найдена дословно — пропуск (проверить вручную)")

print("\nВСЕ ПРАВКИ ПРИМЕНЕНЫ. Проверок пройдено:", len(log))
