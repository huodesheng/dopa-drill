"""Draw a launcher icon of the orange lulu, no SVG renderer required."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "android" / "app" / "src" / "main" / "res"
YELLOW = (255, 209, 90, 255)
ORANGE = (255, 154, 50, 255)
SHORTS = (255, 122, 18, 255)
FRUIT = (255, 138, 26, 255)
LEAF = (63, 163, 77, 255)
IRIS = (59, 124, 255, 255)
PUPIL = (27, 63, 168, 255)
INK = (0, 0, 0, 255)
BG = (255, 248, 236, 255)


def icon(size: int) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size / 192
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(42 * s), fill=BG)

    def e(cx, cy, rx, ry, fill, width=0):
        box = [(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s]
        d.ellipse(box, fill=fill, outline=INK if width else None, width=max(1, int(width * s)) if width else 0)

    # fruit
    e(96, 28, 16, 16, FRUIT, 2.4)
    d.polygon([(96 * s, 16 * s), (108 * s, 8 * s), (100 * s, 20 * s)], fill=LEAF)
    # ears
    e(46, 62, 16, 20, YELLOW, 2.6)
    e(46, 64, 9, 12, (255, 177, 90, 255))
    e(146, 62, 16, 20, YELLOW, 2.6)
    e(146, 64, 9, 12, (255, 177, 90, 255))
    # head
    e(96, 96, 62, 54, YELLOW, 3)
    # muzzle
    e(96, 112, 40, 28, ORANGE, 2.4)
    # eyes
    e(74, 90, 13, 15, (255, 255, 255, 255), 2)
    e(74, 93, 8, 9, IRIS)
    e(74, 95, 4, 4, PUPIL)
    e(118, 90, 13, 15, (255, 255, 255, 255), 2)
    e(118, 93, 8, 9, IRIS)
    e(118, 95, 4, 4, PUPIL)
    # smile
    d.arc([78 * s, 108 * s, 114 * s, 132 * s], start=15, end=165, fill=INK, width=max(2, int(3 * s)))
    # shorts
    d.rounded_rectangle([74 * s, 150 * s, 118 * s, 176 * s], radius=int(10 * s), fill=SHORTS, outline=INK, width=max(1, int(2.4 * s)))
    return im


def main() -> None:
    sizes = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    for folder, size in sizes.items():
        out = RES / folder / "ic_launcher.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        icon(size).save(out)
        print(out, size)


if __name__ == "__main__":
    main()
