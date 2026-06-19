# -*- coding: utf-8 -*-
import re, os
PAGES=["about","services","accounting","taxes","registration","accounting-recovery","consulting","contacts"]

def content_of(html):
    cs=html.find("</header>"); ce=html.rfind('<footer class="site-footer')
    return html[cs+9:ce] if (cs!=-1 and ce!=-1) else html

def visible_text(frag):
    # убрать комментарии, скрипты, теги
    frag=re.sub(r'<!--.*?-->','',frag,flags=re.S)
    frag=re.sub(r'<(script|style)[^>]*>.*?</\1>','',frag,flags=re.S|re.I)
    frag=re.sub(r'<[^>]+>',' ',frag)
    frag=re.sub(r'&[a-z]+;',' ',frag)
    return frag

FORBIDDEN=["нулев","гарантиру","без проверок","100%","возврат гарант","лучшие в","№1","номер 1"]
ENGLISH_FILLER=["lorem","ipsum","read more","continue reading","learn more","dolor sit","consectetur"]

print("СТР                       | рез.ком | смеш.слов | англ.filler | запрещ.фразы")
print("-"*82)
for s in PAGES:
    fn=f"{s}.html"
    html=open(fn,encoding="utf-8").read()
    reserve=len(re.findall(r'\[PFG\]',html))
    cont=content_of(html)
    vt=visible_text(cont)
    low=vt.lower()
    # смешанные латиница+кириллица в одном слове (видимый текст)
    mixed=set()
    for w in re.findall(r'[A-Za-zА-Яа-яЁё]{3,}', vt):
        if re.search(r'[A-Za-z]',w) and re.search(r'[А-Яа-яЁё]',w):
            mixed.add(w)
    fillers=[e for e in ENGLISH_FILLER if e in low]
    forb=[f for f in FORBIDDEN if f in low]
    print(f"{fn:25} | {reserve:7} | {len(mixed):9} | {len(fillers):11} | {len(forb)}")
    if mixed: print("      смеш.слова:", sorted(mixed)[:10])
    if fillers: print("      англ.filler:", fillers)
    if forb: print("      запрещ.фразы:", forb)

print("\n=== CONTACTS форма ===")
c=open("contacts.html",encoding="utf-8").read()
for need in ['pfg-form','name="name"','name="phone"','name="biztype"','name="message"','name="consent"','pfg-form-status','type="submit"','политик']:
    print(f"  {'OK ' if need in c else 'НЕТ'} {need}")

print("\n=== выдуманные числа (видимый текст) на всех стр ===")
for s in PAGES:
    html=open(f"{s}.html",encoding="utf-8").read()
    vt=visible_text(content_of(html))
    # числа вида 25+, 1500+, проценты, годы, БИН-подобные 12 цифр
    nums=re.findall(r'\b\d{2,}\+|\b\d{1,3}\s?%|\b\d{12}\b|\bс\s?\d{4}\s?год|\bсвыше\s?\d+|\b\d+\s?(?:лет|года|клиент)',vt)
    if nums: print(f"  {s}: {nums}")
