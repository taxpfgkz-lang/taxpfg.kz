# -*- coding: utf-8 -*-
"""
Генерация безликих графических ассетов для taxpfg.kz (PrimeFinance Group).
Заменяет два изображения, содержавшие узнаваемые лица, чистыми флэт-иллюстрациями
в бренд-палитре. Идемпотентно: повторный запуск перезаписывает результат.

  infobox-img.png      120x40  RGBA  — бейдж «много клиентов» (был: 3 лица-аватара + «+»)
  service-left-img.png 482x740 RGBA  — иллюстрация «фин. услуги» (был: вырез человека с планшетом)

Запуск:
  PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python .gsd-build/gen_faceless.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter

# ---- бренд-палитра (css/base.css) ----
GOLD   = (236, 171, 35, 255)   # #ecab23  --pbmit-global-color
AMBER  = (245, 159, 70, 255)   # #f59f46  акцент SVG-иконок
NAVY   = (22, 34, 45, 255)     # #16222d  --pbmit-blackish-color
BLUEGREY = (139, 157, 175, 255)
SOFT   = (199, 210, 221, 255)
LIGHT  = (236, 240, 244, 255)  # #ecf0f4
WHITE  = (255, 255, 255, 255)
INK    = (82, 93, 98, 255)     # #525d62 текст

OUT = os.environ.get("OUT_DIR", "images")


def rrect(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def soft_shadow(size, draw_fn, blur=18, offset=(0, 14), alpha=70, color=(22, 34, 45)):
    """Вернуть RGBA-слой с мягкой тенью под фигурой, нарисованной draw_fn(d)."""
    sh = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    draw_fn(d)
    # перекрасить непрозрачные пиксели в цвет тени с заданной альфой
    r, g, b, a = sh.split()
    a = a.point(lambda v: int(v * alpha / 255))
    sh = Image.merge("RGBA", (Image.new("L", size, color[0]),
                              Image.new("L", size, color[1]),
                              Image.new("L", size, color[2]), a))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    shifted = Image.new("RGBA", size, (0, 0, 0, 0))
    shifted.paste(sh, offset, sh)
    return shifted


# =========================================================================
# 1) infobox-img.png — кластер из 4 кружков (аватары без лиц) + «+»
# =========================================================================
def gen_infobox():
    S = 4
    W, H = 120 * S, 40 * S
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = 17 * S
    ring = 3 * S
    cy = H // 2
    xs = [20 * S, 40 * S, 60 * S, 82 * S]
    fills = [NAVY, BLUEGREY, AMBER]
    # три «аватара» — заливка + кольцо; рисуем слева направо (правый поверх)
    for i, cx in enumerate(xs[:3]):
        d.ellipse([cx - r - ring, cy - r - ring, cx + r + ring, cy + r + ring], fill=WHITE)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fills[i])
    # четвёртый — «+N» кружок (золото)
    cx = xs[3]
    d.ellipse([cx - r - ring, cy - r - ring, cx + r + ring, cy + r + ring], fill=WHITE)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    pl = 7 * S
    d.line([cx - pl, cy, cx + pl, cy], fill=WHITE, width=3 * S)
    d.line([cx, cy - pl, cx, cy + pl], fill=WHITE, width=3 * S)

    img = img.resize((120, 40), Image.LANCZOS)
    img.save(os.path.join(OUT, "infobox-img.png"))
    print("infobox-img.png ->", img.size, img.mode)


# =========================================================================
# 2) service-left-img.png — флэт-иллюстрация «фин. услуги», прозрачный фон
# =========================================================================
def gen_service_left():
    S = 2
    W, H = 482 * S, 740 * S
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def px(v):
        return int(v * S)

    # --- мягкая восходящая «линия роста» позади (амбер) ---
    growth = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(growth)
    pts = [(px(40), px(560)), (px(150), px(470)), (px(250), px(520)),
           (px(360), px(360)), (px(450), px(300))]
    gd.line(pts, fill=(245, 159, 70, 90), width=px(6), joint="curve")
    for x, y in pts:
        gd.ellipse([x - px(7), y - px(7), x + px(7), y + px(7)], fill=(245, 159, 70, 130))
    img.alpha_composite(growth)

    # --- главная карточка-дашборд (белая, тень) ---
    card = [px(70), px(250), px(372), px(620)]

    def draw_card(dd):
        rrect(dd, card, px(26), fill=(0, 0, 0, 255))
    img.alpha_composite(soft_shadow((W, H), draw_card, blur=px(16), offset=(0, px(16)), alpha=60))
    d = ImageDraw.Draw(img)
    rrect(d, card, px(26), fill=WHITE)
    # шапка карточки
    rrect(d, [px(70), px(250), px(372), px(312)], px(26), fill=NAVY)
    d.rectangle([px(70), px(286), px(372), px(312)], fill=NAVY)
    # точки «окна»
    for i, c in enumerate((AMBER, GOLD, SOFT)):
        d.ellipse([px(92) + i * px(22) - px(6), px(275), px(92) + i * px(22) + px(6), px(287)], fill=c)
    # заголовочные строки
    rrect(d, [px(96), px(336), px(250), px(352)], px(8), fill=SOFT)
    rrect(d, [px(96), px(366), px(200), px(378)], px(6), fill=LIGHT)
    # столбцы бар-чарта
    base = px(560)
    bx = px(104)
    heights = [px(70), px(120), px(95), px(150)]
    cols = [BLUEGREY, AMBER, BLUEGREY, GOLD]
    for h, c in zip(heights, cols):
        rrect(d, [bx, base - h, bx + px(40), base], px(10), fill=c)
        bx += px(62)
    # ось
    d.line([px(96), base + px(14), px(352), base + px(14)], fill=SOFT, width=px(3))

    # --- кольцевая диаграмма (донат) вверху справа, перекрывает карточку ---
    cx, cy, rO, rI = px(372), px(250), px(74), px(44)

    def draw_donut_shadow(dd):
        dd.ellipse([cx - rO, cy - rO, cx + rO, cy + rO], fill=(0, 0, 0, 255))
    img.alpha_composite(soft_shadow((W, H), draw_donut_shadow, blur=px(14), offset=(0, px(12)), alpha=55))
    d = ImageDraw.Draw(img)
    d.ellipse([cx - rO, cy - rO, cx + rO, cy + rO], fill=WHITE)
    d.pieslice([cx - rO + px(8), cy - rO + px(8), cx + rO - px(8), cy + rO - px(8)], 0, 360, fill=LIGHT)
    d.pieslice([cx - rO + px(8), cy - rO + px(8), cx + rO - px(8), cy + rO - px(8)], -90, 130, fill=GOLD)
    d.pieslice([cx - rO + px(8), cy - rO + px(8), cx + rO - px(8), cy + rO - px(8)], 130, 210, fill=AMBER)
    d.ellipse([cx - rI, cy - rI, cx + rI, cy + rI], fill=WHITE)

    # --- значок-галочка (навигационный кружок) слева вверху ---
    bx, by, br = px(120), px(176), px(50)

    def draw_check_shadow(dd):
        dd.ellipse([bx - br, by - br, bx + br, by + br], fill=(0, 0, 0, 255))
    img.alpha_composite(soft_shadow((W, H), draw_check_shadow, blur=px(12), offset=(0, px(10)), alpha=55))
    d = ImageDraw.Draw(img)
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=NAVY)
    d.line([bx - px(20), by, bx - px(6), by + px(16)], fill=GOLD, width=px(8), joint="curve")
    d.line([bx - px(6), by + px(16), bx + px(22), by - px(16)], fill=GOLD, width=px(8), joint="curve")

    # --- стопка монет у основания (золото) ---
    coin_cx, coin_cy, cw, ch = px(250), px(648), px(54), px(16)
    for i in range(4):
        y = coin_cy - i * px(13)
        d.ellipse([coin_cx - cw, y - ch, coin_cx + cw, y + ch], fill=GOLD, outline=AMBER, width=px(2))
    d.ellipse([coin_cx - cw, coin_cy - 3 * px(13) - ch, coin_cx + cw, coin_cy - 3 * px(13) + ch], fill=(245, 200, 110, 255), outline=AMBER, width=px(2))

    # --- «земля»: мягкая тень-эллипс под композицией ---
    floor = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(floor)
    fd.ellipse([px(70), px(680), px(412), px(720)], fill=(22, 34, 45, 45))
    floor = floor.filter(ImageFilter.GaussianBlur(px(10)))
    img.alpha_composite(floor)

    img = img.resize((482, 740), Image.LANCZOS)
    img.save(os.path.join(OUT, "service-left-img.png"))
    print("service-left-img.png ->", img.size, img.mode)


if __name__ == "__main__":
    gen_infobox()
    gen_service_left()
    print("done")
