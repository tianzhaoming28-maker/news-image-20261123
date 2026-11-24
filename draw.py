#!/usr/bin/env python3
"""Front page for Monday 23 November 2026.

Eight stories from the day, drawn as a newspaper front page with
Pillow primitives only — no photos, no outside assets. The lead panel
carries Ukraine sinking the Russian corvette Merkury off Libya; three
panels below it cover the Indonesian factory fire, the US sanctions on
Iran's shadow-banking networks, and the COP31 aftermath; the bottom
row covers India's Nepal package, Shuri Castle reopening, the Thai
court ruling and China's 2030 care plan.

Run from this directory: writes entry.png next to itself.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (16, 16, 18)
MUTE = (96, 90, 82)
CARD = (255, 253, 246)
SAND = (236, 230, 214)
RED = (176, 32, 38)
NAVY = (26, 70, 138)
TEAL = (13, 112, 104)
GOLD = (188, 132, 16)
GREEN = (36, 106, 50)
PLUM = (92, 50, 138)
RUST = (206, 92, 18)
CREAM = (240, 220, 150)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


def strong(size):
    return font("DejaVuSans-Bold.ttf", size)


def regular(size):
    return font("DejaVuSans.ttf", size)


def split_lines(d, text, fnt, max_w):
    """Break text into lines no wider than max_w pixels."""
    out = []
    words = text.split()
    i = 0
    while i < len(words):
        line = words[i]
        i += 1
        while i < len(words):
            nxt = line + " " + words[i]
            if d.textlength(nxt, font=fnt) > max_w:
                break
            line = nxt
            i += 1
        out.append(line)
    return out


def write_lines(d, x, y, text, fnt, fill, max_w, gap=4):
    """Draw wrapped text starting at (x, y); return the y below it."""
    for ln in split_lines(d, text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + gap
    return y


class Canvas:
    """A blank front page plus the panel-drawing helpers."""

    def __init__(self):
        self.image = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.image)

    def box(self, x0, y0, x1, y1, accent):
        self.d.rectangle([x0, y0, x1, y1], fill=CARD, outline=INK, width=2)
        self.d.line([x0, y0 + 3, x1, y0 + 3], fill=accent, width=7)

    def tag(self, x, y, text, color):
        self.d.text((x, y), text, font=strong(14), fill=color)
        return y + 22

    def title(self, x, y, text, size, max_w):
        return write_lines(self.d, x, y, text, strong(size), INK, max_w,
                           gap=2)

    def body(self, x, y, text, size, max_w):
        return write_lines(self.d, x, y, text, regular(size), MUTE, max_w,
                           gap=3)

    def pill(self, x, y, text):
        w = self.d.textlength(text, font=strong(14)) + 22
        self.d.rectangle([x, y, x + w, y + 30], fill=SAND, outline=INK,
                         width=2)
        self.d.text((x + 11, y + 8), text, font=strong(14), fill=INK)
        return x + w + 10


def warship(d, cx, cy):
    """A corvette at anchor, hit by a sea drone, smoke rising."""
    d.polygon([(cx - 62, cy - 6), (cx + 62, cy - 6), (cx + 48, cy + 16),
               (cx - 48, cy + 16)], fill=NAVY, outline=INK)
    d.rectangle([cx - 34, cy - 30, cx + 10, cy - 6], fill=NAVY,
                outline=INK, width=2)
    d.line([cx - 8, cy - 30, cx - 8, cy - 52], fill=INK, width=4)
    d.polygon([(cx - 8, cy - 52), (cx + 14, cy - 46), (cx - 8, cy - 40)],
              fill=RED)
    d.ellipse([cx - 46, cy - 58, cx - 26, cy - 38], fill=MUTE)
    d.ellipse([cx - 36, cy - 70, cx - 14, cy - 50], fill=MUTE)
    d.polygon([(cx - 40, cy - 40), (cx - 28, cy - 66), (cx - 18, cy - 44),
               (cx - 6, cy - 60), (cx - 10, cy - 36)], fill=RUST)
    d.rectangle([cx + 34, cy + 20, cx + 58, cy + 28], fill=INK)
    d.line([cx + 34, cy + 32, cx + 58, cy + 32], fill=TEAL, width=2)
    d.line([cx - 62, cy + 34, cx + 62, cy + 34], fill=INK, width=2)


def factory_fire(d, cx, cy):
    """A candy factory with a slanted roof, twin chimneys, flame."""
    d.polygon([(cx - 52, cy + 30), (cx - 52, cy - 8), (cx, cy - 26),
               (cx + 52, cy - 8), (cx + 52, cy + 30)], fill=SAND,
              outline=INK)
    d.rectangle([cx - 52, cy + 26, cx + 52, cy + 30], fill=INK)
    d.rectangle([cx - 44, cy - 38, cx - 30, cy - 12], fill=INK)
    d.rectangle([cx + 30, cy - 44, cx + 44, cy - 12], fill=INK)
    d.ellipse([cx - 50, cy - 56, cx - 28, cy - 34], fill=MUTE)
    d.ellipse([cx + 26, cy - 62, cx + 48, cy - 40], fill=MUTE)
    d.polygon([(cx - 16, cy - 10), (cx - 4, cy - 34), (cx + 6, cy - 14),
               (cx + 16, cy - 30), (cx + 14, cy - 10)], fill=RUST)
    d.rectangle([cx - 34, cy + 6, cx - 18, cy + 20], fill=RED)
    d.rectangle([cx - 6, cy + 6, cx + 10, cy + 20], fill=RED)
    d.rectangle([cx + 20, cy + 6, cx + 36, cy + 20], fill=RED)


def vault_slash(d, cx, cy):
    """A bank front with columns, crossed out in red: sanctions."""
    d.polygon([(cx - 52, cy - 30), (cx, cy - 52), (cx + 52, cy - 30)],
              fill=NAVY, outline=INK)
    d.rectangle([cx - 48, cy - 30, cx + 48, cy + 34], fill=CARD,
                outline=INK, width=3)
    for xx in (-36, -12, 12, 36):
        d.rectangle([cx + xx - 5, cy - 22, cx + xx + 5, cy + 26],
                    fill=NAVY)
    d.line([cx - 48, cy + 34, cx + 48, cy + 34], fill=INK, width=3)
    d.text((cx - 8, cy - 24), "$", font=strong(18), fill=INK)
    d.line([cx - 56, cy - 44, cx + 56, cy + 44], fill=RED, width=6)


def globe_crack(d, cx, cy):
    """A cracked globe: the climate talks broke apart."""
    d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], outline=INK, width=4)
    d.arc([cx - 52, cy - 52, cx + 52, cy + 52], 200, 340, fill=INK,
          width=2)
    d.ellipse([cx - 26, cy - 52, cx + 26, cy + 52], outline=INK, width=2)
    d.line([cx - 52, cy, cx + 52, cy], fill=INK, width=2)
    crack = [(cx + 4, cy - 52), (cx - 8, cy - 24), (cx + 10, cy - 4),
             (cx - 6, cy + 20), (cx + 2, cy + 52)]
    d.line(crack, fill=RED, width=5)
    d.line([cx + 66, cy - 44, cx + 66, cy + 34], fill=INK, width=4)
    d.ellipse([cx + 56, cy + 26, cx + 76, cy + 46], fill=RED, outline=INK,
              width=3)
    d.line([cx + 66, cy + 30, cx + 66, cy - 30], fill=RED, width=4)


def money_bill(d, cx, cy):
    """A banknote stamped with the aid figure."""
    d.rectangle([cx - 56, cy - 26, cx + 56, cy + 26], fill=GREEN,
                outline=INK, width=3)
    d.rectangle([cx - 46, cy - 18, cx + 46, cy + 18], outline=CARD,
                width=2)
    d.ellipse([cx - 16, cy - 14, cx + 16, cy + 14], outline=CARD, width=3)
    d.text((cx - 7, cy - 12), "$", font=strong(20), fill=CARD)
    d.text((cx - 30, cy + 32), "1.62 BN", font=strong(15), fill=INK)


def castle(d, cx, cy):
    """Shuri Castle's vermilion main hall, rebuilt and reopened."""
    d.rectangle([cx - 46, cy + 20, cx + 46, cy + 36], fill=RED,
                outline=INK, width=3)
    d.line([cx - 46, cy + 28, cx + 46, cy + 28], fill=INK, width=2)
    for xx in (-34, -12, 10, 32):
        d.line([cx + xx, cy + 20, cx + xx, cy + 36], fill=INK, width=2)
    d.polygon([(cx - 58, cy + 20), (cx, cy + 2), (cx + 58, cy + 20)],
              fill=RED, outline=INK)
    d.rectangle([cx - 28, cy - 14, cx + 28, cy + 2], fill=RED,
                outline=INK, width=3)
    d.polygon([(cx - 38, cy - 14), (cx, cy - 30), (cx + 38, cy - 14)],
              fill=RED, outline=INK)
    d.line([cx - 54, cy + 42, cx + 54, cy + 42], fill=INK, width=3)
    d.line([cx - 46, cy + 48, cx + 46, cy + 48], fill=INK, width=3)


def scales(d, cx, cy):
    """Balance scales: justice, tilted."""
    d.line([cx, cy - 44, cx, cy + 34], fill=INK, width=4)
    d.line([cx - 44, cy - 36, cx + 44, cy - 36], fill=INK, width=3)
    d.line([cx - 44, cy - 36, cx - 52, cy - 8], fill=INK, width=2)
    d.line([cx - 44, cy - 36, cx - 36, cy - 8], fill=INK, width=2)
    d.polygon([(cx - 56, cy - 8), (cx - 32, cy - 8), (cx - 44, cy + 8)],
              fill=GOLD, outline=INK)
    d.line([cx + 44, cy - 36, cx + 36, cy - 14], fill=INK, width=2)
    d.line([cx + 44, cy - 36, cx + 52, cy - 14], fill=INK, width=2)
    d.polygon([(cx + 32, cy - 14), (cx + 56, cy - 14), (cx + 44, cy + 2)],
              fill=GOLD, outline=INK)
    d.ellipse([cx - 8, cy - 50, cx + 8, cy - 36], fill=INK)
    d.rectangle([cx - 44, cy + 34, cx + 44, cy + 42], fill=INK)


def family(d, cx, cy):
    """Two figures and a heart: care for the old and the young."""
    d.ellipse([cx - 34, cy - 40, cx - 18, cy - 24], fill=INK)
    d.rectangle([cx - 36, cy - 22, cx - 16, cy + 22], fill=NAVY)
    d.ellipse([cx + 8, cy - 28, cx + 20, cy - 16], fill=INK)
    d.rectangle([cx + 6, cy - 14, cx + 22, cy + 22], fill=TEAL)
    d.ellipse([cx + 30, cy - 8, cx + 40, cy + 2], fill=INK)
    d.rectangle([cx + 29, cy + 4, cx + 41, cy + 22], fill=RUST)
    d.polygon([(cx - 8, cy - 46), (cx - 2, cy - 38), (cx + 4, cy - 46),
               (cx + 10, cy - 38), (cx + 2, cy - 28), (cx - 8, cy - 38)],
              fill=RED)
    d.line([cx - 44, cy + 30, cx + 44, cy + 30], fill=INK, width=3)


ICONS = {"warship": warship, "factory": factory_fire,
         "vault": vault_slash, "globe": globe_crack,
         "money": money_bill, "castle": castle, "scales": scales,
         "family": family}

# (box, accent, kicker, headline, subline, icon, head size, sub size,
#  text width, icon centre)
TOP3 = [
    ((24, 396, 336, 652), RUST, "DISASTER  ·  BANTEN, INDONESIA",
     "FACTORY FIRE: 24 DEAD, 30 MISSING",
     "Blaze guts a candy plant in Cikande; rescuers hunt for the "
     "missing in the unstable wreckage.", "factory", 21, 15, 276,
     (180, 596)),
    ((348, 396, 660, 652), NAVY, "ECONOMY  ·  WASHINGTON",
     "US HITS IRAN'S 'SHADOW BANKS'",
     "Treasury sanctions 20+ exchange houses and front firms moving "
     "billions for Tehran.", "vault", 21, 15, 276, (504, 596)),
    ((672, 396, 1000, 652), TEAL, "CLIMATE  ·  AFTERMATH OF COP31",
     "COP FLOP: PACIFIC IN DESPAIR",
     "Australia's minister faces calls to quit; island states say "
     "they were 'let down on all sides'.", "globe", 21, 15, 292,
     (836, 596)),
]

BOTTOM4 = [
    ((24, 664, 270, 924), GOLD, "AID  ·  NEW DELHI",
     "INDIA GIVES NEPAL $1.62BN",
     "Modi pledges the biggest relief yet for August's flood-hit "
     "neighbour.", "money", 20, 14, 210, (147, 872)),
    ((282, 664, 528, 924), GREEN, "CULTURE  ·  OKINAWA",
     "SHURI CASTLE REOPENS",
     "Seven years after the 2019 fire, the royal hall opens its "
     "doors again at noon.", "castle", 20, 14, 210, (405, 872)),
    ((540, 664, 786, 924), PLUM, "JUSTICE  ·  BANGKOK",
     "THAI COURT CUTS MP'S JAIL TERM",
     "Lèse-majesté sentence halved from six years to three; bail "
     "granted, appeal to follow.", "scales", 20, 14, 210, (663, 872)),
    ((798, 664, 1000, 924), RED, "CHINA  ·  BEIJING",
     "CHINA'S 2030 CARE PLAN",
     "Eldercare for 70% of communities, more nurseries — an answer "
     "to ageing and low births.", "family", 20, 14, 170, (899, 872)),
]


def render():
    p = Canvas()
    d = p.d

    # Masthead: black band, paper title, red date.
    d.rectangle([0, 0, 1024, 140], fill=INK)
    d.text((34, 12), "THE WORLD IN ONE IMAGE  ·  GLOBAL FRONT PAGE",
           font=strong(18), fill=CREAM)
    d.text((32, 36), "MONDAY", font=serif(52), fill=(255, 255, 255))
    d.text((32, 92), "23 NOVEMBER 2026", font=serif(38),
           fill=(255, 96, 96))
    d.text((700, 44), "ONE DAY.", font=serif(30), fill=(255, 255, 255))
    d.text((700, 82), "EIGHT STORIES.", font=serif(30),
           fill=(255, 255, 255))
    d.rectangle([0, 140, 1024, 148], fill=RED)

    # Lead: Ukraine sinks the Russian corvette Merkury off Libya.
    p.box(24, 160, 1000, 384, RED)
    y = p.tag(44, 174, "LEAD  ·  WAR  ·  BENGHAZI, LIBYA", RED)
    y = p.title(44, y, "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
                30, 560)
    y = p.body(44, y + 6,
               "Seven sea drones sink the corvette Merkury at its "
               "Libyan berth and hit a weapons cargo ship — Kyiv's war "
               "reaches 2,400 km from the front.", 17, 560)
    warship(d, 852, 268)
    x = 44
    for chip in ("7 SEA DRONES", "MERKURY SUNK", "KA-27 DOWN"):
        x = p.pill(x, 322, chip)
    d.text((44, 362), "ZELENSKYY: 'WE HIT BACK WHEN RUSSIA ATTACKS US'",
           font=strong(13), fill=MUTE)

    # Three mid-size stories.
    for box, accent, kick, head, sub, icon, hs, ss, w, (ix, iy) in TOP3:
        p.box(*box, accent)
        y = p.tag(box[0] + 18, box[1] + 12, kick, accent)
        y = p.title(box[0] + 18, y, head, hs, w)
        p.body(box[0] + 18, y + 2, sub, ss, w)
        ICONS[icon](d, ix, iy)

    # Four bottom stories.
    for box, accent, kick, head, sub, icon, hs, ss, w, (ix, iy) in BOTTOM4:
        p.box(*box, accent)
        y = p.tag(box[0] + 16, box[1] + 12, kick, accent)
        y = p.title(box[0] + 16, y, head, hs, w)
        p.body(box[0] + 16, y + 2, sub, ss, w)
        ICONS[icon](d, ix, iy)

    # Footer: black band repeating the date and the story list.
    d.rectangle([0, 936, 1024, 1024], fill=INK)
    d.text((34, 948), "MONDAY 23 NOVEMBER 2026 -- THE DAY IN ONE IMAGE",
           font=strong(19), fill=(255, 255, 255))
    d.text((34, 978),
           "Libya  ·  Factory fire  ·  Nepal  ·  Iran sanctions  ·  "
           "COP31  ·  Shuri Castle  ·  Bangkok  ·  China care",
           font=regular(15), fill=(220, 214, 195))
    return p.image


if __name__ == "__main__":
    target = Path(__file__).with_name("entry.png")
    render().save(target, format="PNG", optimize=True)
    print(target, target.stat().st_size)
