"""Render the lulu drawing into Android launcher icons."""
from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "android" / "app" / "src" / "main" / "res"
SVG = ROOT.parent / "docs" / "lulu.svg"
BG = (255, 248, 236, 255)


def source() -> Image.Image:
    drawing = svg2rlg(str(SVG))
    png = renderPM.drawToPIL(drawing, dpi=144, bg=0xFFF8EC)
    # The drawing sits in a square canvas with empty margins. Crop to the figure.
    box = png.getbbox()
    figure = png.crop(box).convert("RGBA")
    pad = int(max(figure.size) * 0.08)
    side = max(figure.size) + pad * 2
    canvas = Image.new("RGBA", (side, side), BG)
    canvas.paste(figure, ((side - figure.width) // 2, (side - figure.height) // 2))
    return canvas


def icon(art: Image.Image, size: int) -> Image.Image:
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    radius = int(size * 0.22)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=BG)
    inset = int(size * 0.08)
    fitted = art.resize((size - inset * 2, size - inset * 2), Image.Resampling.LANCZOS)
    im.alpha_composite(fitted, (inset, inset))
    return im


def main() -> None:
    art = source()
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
        icon(art, size).save(out)
        print(out, size)


if __name__ == "__main__":
    main()