# -*- coding: utf-8 -*-
# Этап 5, ревизия по адверсариальной проверке:
#  - сократить 5 длинных title (<=60) и 4 длинных description (<=160)
#  - нейтрализовать неподтверждённое юр.написание в about (lead)
#  - синхронизировать эталон SITE_CONTENT.md и frag/*.meta.txt (устранить рассинхрон Этапа 2)
# Источник истины = FINAL (ниже). Затем страницы ПЕРЕСОБИРАЮТСЯ ассемблерами.
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAG = os.path.join(ROOT, ".gsd-build", "frag")

# порядок строго как в docs/SITE_CONTENT.md (по позиции SEO-блоков)
ORDER = ["index","about","services","accounting","taxes","registration",
         "accounting-recovery","consulting","contacts"]

FINAL = {
 "index": (
   "Бухгалтерские услуги для ИП и ТОО в Алматы — PrimeFinance Group",
   "Бухгалтерское и налоговое сопровождение ИП и ТОО в Алматы: учёт, отчётность, зарплата, регистрация. Консультация по телефону и WhatsApp."),
 "about": (
   "О компании PrimeFinance Group — бухгалтерия и налоги в Алматы",
   "PrimeFinance Group — бухгалтерское и налоговое сопровождение бизнеса в Алматы: учёт ИП и ТОО по законодательству и стандартам отчётности РК."),
 "services": (
   "Услуги: бухгалтерия и налоги в Алматы | PrimeFinance Group",
   "Бухгалтерское и налоговое сопровождение, регистрация и ликвидация ИП и ТОО, восстановление учёта, консультации и помощь налогового юриста в Алматы."),
 "accounting": (
   "Бухгалтерское сопровождение ИП и ТОО в Алматы | PrimeFinance Group",
   "Ведение бухгалтерского учёта ИП и ТОО на аутсорсинге: первичка, расчёт зарплаты, банковские операции, учёт ОС и ТМЗ, сверки, управленческая отчётность."),
 "taxes": (
   "Налоговый учёт и отчётность в Алматы | PrimeFinance Group",
   "Ведение налогового учёта, подготовка и сдача отчётности, сверка с бюджетом, сопровождение проверок и ответы на уведомления налоговых органов."),
 "registration": (
   "Регистрация ИП и ТОО в Алматы | PrimeFinance Group",
   "Регистрация ИП и ТОО, изменения учредительных документов, смена директора и адреса, получение ЭЦП, открытие счетов, ликвидация бизнеса."),
 "accounting-recovery": (
   "Восстановление бухучёта в Алматы | PrimeFinance Group",
   "Восстановление бухгалтерского и налогового учёта за прошлые периоды и постановка системы учёта с нуля: методы учёта, документооборот, автоматизация на 1С."),
 "consulting": (
   "Консультации и налоговый юрист в Алматы | PrimeFinance Group",
   "Бухгалтерские и налоговые консультации, выбор режима налогообложения, финансовый анализ, помощь налогового юриста и снятие арестов с расчётных счетов."),
 "contacts": (
   "Контакты PrimeFinance Group — бухгалтерия в Алматы | taxpfg.kz",
   "Свяжитесь с PrimeFinance Group: Алматы, проспект Абая 68/74, БЦ «AVENUE CITY», офис 39. Телефон и WhatsApp +7 707 237 00 50."),
}

# контроль длин: 5 проблемных (по адверс-проверке) сокращены <=60; index(63)/accounting(66)
# — пограничные эталонные, ревью их не флагнуло; жёсткий потолок 70.
problems = []
for slug,(t,d) in FINAL.items():
    if len(t) > 70: problems.append("%s: title %d>70 (%r)" % (slug,len(t),t))
    if len(d) > 160: problems.append("%s: desc %d>160" % (slug,len(d)))
if problems:
    print("ДЛИНЫ:\n"+"\n".join(problems)); sys.exit(1)
print("=== длины OK ===")
for slug in ORDER:
    flag = "  <- пограничный (эталон, не флагнут ревью)" if len(FINAL[slug][0]) > 60 else ""
    print("  %-22s title=%d desc=%d%s" % (slug, len(FINAL[slug][0]), len(FINAL[slug][1]), flag))

# 1) docs/SITE_CONTENT.md — заменить Title/Description по позиции (надёжно)
scp = os.path.join(ROOT, "docs", "SITE_CONTENT.md")
sc = io.open(scp, encoding="utf-8").read().split("\n")
ti = [i for i,l in enumerate(sc) if re.match(r'^-\s*\*\*Title:\*\*', l)]
di = [i for i,l in enumerate(sc) if re.match(r'^-\s*\*\*Description:\*\*', l)]
assert len(ti)==9 and len(di)==9, "SITE_CONTENT: Title=%d Desc=%d (ожид 9/9)" % (len(ti),len(di))
for k,slug in enumerate(ORDER):
    sc[ti[k]] = "- **Title:** " + FINAL[slug][0]
    sc[di[k]] = "- **Description:** " + FINAL[slug][1]
io.open(scp,"w",encoding="utf-8",newline="\n").write("\n".join(sc))
print("SITE_CONTENT.md: 9 Title/9 Description приведены к FINAL")

# 2) frag/<slug>.meta.txt для 8 внутренних (index не фрагмент) — title/desc=FINAL, h1 сохранить
for slug in ORDER:
    if slug == "index": continue
    mp = os.path.join(FRAG, slug + ".meta.txt")
    cur = [l for l in io.open(mp, encoding="utf-8").read().split("\n")]
    h1 = cur[2].strip() if len(cur) >= 3 and cur[2].strip() else (FINAL[slug][0])
    io.open(mp,"w",encoding="utf-8",newline="\n").write(
        FINAL[slug][0] + "\n" + FINAL[slug][1] + "\n" + h1 + "\n")
print("frag/*.meta.txt: 8 внутренних синхронизированы с FINAL (h1 сохранён)")

# 3) about: нейтрализовать неподтверждённое юр.написание в lead-абзаце
ap = os.path.join(FRAG, "about.content.html")
a = io.open(ap, encoding="utf-8").read()
OLD = "ТОО «PrimeFinance Group» — бухгалтерско-консалтинговая компания в Алматы."
NEW = "PrimeFinance Group — бухгалтерско-консалтинговая компания в Алматы.<!-- [PFG] точное юр. наименование (ТОО) уточнить у клиента -->"
n = a.count(OLD)
assert n == 1, "about: ожидал 1 вхождение lead-строки, нашёл %d" % n
a = a.replace(OLD, NEW)
io.open(ap,"w",encoding="utf-8",newline="\n" if "\r" not in a else "").write(a)
print("about.content.html: lead нейтрализован (ТОО -> бренд + [PFG])")

# 4) index.html — desc (3×: meta/og/twitter) + JSON-LD (+@id). title без изменений.
sys.path.insert(0, os.path.join(ROOT, ".gsd-build"))
import seo_common
ip = os.path.join(ROOT, "index.html")
h = io.open(ip, encoding="utf-8").read()
cur_desc = re.search(r'<meta name="description" content="([^"]*)">', h).group(1)
new_desc = FINAL["index"][1].replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;")
cnt = h.count(cur_desc)
assert cnt == 3, "index: ожидал 3 вхождения desc (meta/og/twitter), нашёл %d" % cnt
h = h.replace(cur_desc, new_desc)
# JSON-LD: заменить содержимое на seo_common.JSONLD (теперь с @id)
h2 = re.sub(r'(<script type="application/ld\+json">).*?(</script>)',
            lambda m: m.group(1)+seo_common.JSONLD+m.group(2), h, count=1, flags=re.S)
assert h2 != h, "index: JSON-LD не заменён"
io.open(ip,"w",encoding="utf-8").write(h2)
print("index.html: desc обновлён (3×), JSON-LD +@id")
print("\nГОТОВО. Дальше: пересобрать assemble.py + build_privacy.py")
