# -*- coding: utf-8 -*-
"""
hide_empty_faq.py — детерминированно и идемпотентно убирает из фрагментов
пустые секции FAQ (только заголовок + резервный комментарий [PFG], без Q&A).

Зачем: на сервис-страницах рендерился заголовок «Частые вопросы …» без единого
вопроса — для посетителя это выглядит как сломанный/недоделанный блок. Контент
FAQ отложен до уточнения у клиента (см. комментарий [PFG]), выдумывать Q&A нельзя.
Поэтому секция заменяется одним резервным HTML-комментарием, который сохраняет
тексты подзаголовка/заголовка для последующего восстановления.

Запуск (из корня проекта):
    PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python .gsd-build/hide_empty_faq.py
Идемпотентно: повторный запуск ничего не меняет.
"""
import re
import sys
import pathlib

FRAG = pathlib.Path(__file__).resolve().parent / "frag"
FILES = [
    "accounting.content.html",
    "taxes.content.html",
    "registration.content.html",
    "consulting.content.html",
    "accounting-recovery.content.html",
]

# Якорь пустого FAQ: секция pfg-section--alt c заголовком и резервным
# комментарием [PFG] FAQ, без какого-либо контента между заголовком и </section>.
# Необязательная предшествующая строка-метка <!-- FAQ (резерв) -->.
PATTERN = re.compile(
    r'(?:[ \t]*<!-- FAQ \(резерв\) -->\n)?'
    r'[ \t]*<section class="pfg-section(?: pfg-section--alt)?">\n'
    r'[ \t]*<div class="container">\n'
    r'[ \t]*<div class="pbmit-heading-subheading">\n'
    r'[ \t]*<h4 class="pbmit-subtitle">(?P<sub>.*?)</h4>\n'
    r'[ \t]*<h2 class="pbmit-title">(?P<title>.*?)</h2>\n'
    r'[ \t]*</div>\n'
    r'[ \t]*<!-- \[PFG\] FAQ наполняется после уточнения у клиента -->\n'
    r'[ \t]*</div>\n'
    r'[ \t]*</section>',
    re.UNICODE,
)

MARKER = "[PFG] FAQ-резерв (скрыт до наполнения"


def repl(m):
    sub = m.group("sub").strip()
    title = m.group("title").strip()
    # В тексте комментария недопустима последовательность "--": заменяем на "/".
    safe = lambda s: s.replace("--", "/")
    return (
        '<!-- {marker} контентом): subtitle="{sub}" | title="{title}". '
        'Наполнить Q&A после уточнения у клиента, затем вернуть секцию FAQ '
        '(pfg-section, alt-вариант) с аккордеоном. -->'
    ).format(marker=MARKER, sub=safe(sub), title=safe(title))


def main():
    changed = 0
    for name in FILES:
        p = FRAG / name
        src = p.read_text(encoding="utf-8")
        if MARKER in src:
            print("  skip (уже скрыт): %s" % name)
            continue
        new, n = PATTERN.subn(repl, src, count=1)
        if n == 0:
            print("  WARN: пустой FAQ не найден в %s (структура изменилась?)" % name)
            continue
        if n != 1:
            print("  WARN: %d совпадений в %s (ожидалось 1)" % (n, name))
        p.write_text(new, encoding="utf-8")
        changed += 1
        print("  ok: FAQ скрыт в %s" % name)
    print("Изменено файлов: %d из %d" % (changed, len(FILES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
