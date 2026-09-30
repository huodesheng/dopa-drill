"""Draw a launcher icon from the lulu head, no SVG renderer required."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "android" / "app" / "src" / "main" / "res"
PINK = (255, 151, 191, 255)
CREAM = (255, 243, 228, 255)
INK = (0, 0, 0, 255)
BG = (59, 107, 255, 255)


def icon(size: int) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size / 192
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(42 * s), fill=BG)

    def e(cx, cy, rx, ry, fill, width=0):
        box = [
            (cx - rx) * s,
            (cy - ry) * s,
            (cx + rx) * s,
            (cy + ry) * s,
        ]
        d.ellipse(box, fill=fill, outline=INK if width else None, width=max(1, int(width * s)) if width else 0)

    # ears
    e(28, 58, 22, 22, PINK, 3.2)
    e(28, 58, 14, 15, (255, 230, 240, 255))
    e(164, 58, 22, 22, PINK, 3.2)
    e(164, 58, 14, 15, (255, 230, 240, 255))
    # head
    e(96, 108, 58, 52, PINK, 3.6)
    e(96, 112, 46, 40, CREAM)
    # eyes
    e(72, 108, 10, 12, (255, 255, 255, 255), 2)
    e(72, 110, 6, 7, PINK)
    e(120, 108, 10, 12, (255, 255, 255, 255), 2)
    e(120, 110, 6, 7, PINK)
    # smile
    d.arc(
        [78 * s, 118 * s, 114 * s, 142 * s],
        start=20,
        end=160,
        fill=INK,
        width=max(2, int(3 * s)),
    )
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
