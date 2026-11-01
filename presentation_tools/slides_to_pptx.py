#!/usr/bin/env python3
"""
slides_to_pptx.py
=================
Rebuild a PowerPoint (.pptx) from a set of slide images.

This is the LEGITIMATE recovery path for a presentation you are allowed to
view (owner / licensed viewer): export each visible slide as an image, put
them in a folder, and run this script. It produces a 16:9 .pptx with one
image per slide, centered and aspect-preserved, plus a fade transition on
each slide.

Usage
-----
    # Install dependencies once:
    pip install python-pptx pymupdf

    # Basic: turn C:\\slides\\*.png|jpg into my_deck.pptx
    python slides_to_pptx.py C:\\slides my_deck.pptx

    # From a PDF you exported yourself: each page becomes a slide image,
    # then a .pptx (no manual screenshotting needed).
    python slides_to_pptx.py my_deck.pdf my_deck.pptx

    # Want the slides as a PDF instead of a PPTX? End the output with .pdf:
    #   python slides_to_pptx.py C:\\slides my_deck.pdf
    #   python slides_to_pptx.py my_deck.pdf my_deck_out.pdf

    # Optional: download slides from a text file of image URLs, then build.
    #   urls.txt content (one URL per line):
    #       https://cdn.example.com/slide-1.png
    #       https://cdn.example.com/slide-2.png
    python slides_to_pptx.py urls.txt my_deck.pptx --download-first

NOTE: use this only for presentations you may legitimately view (your own, or
ones you have rights to). It does not bypass any password or paywall.

Exit codes: 0 = success, 1 = error (prints a clear message).
"""

import os
import re
import sys
import argparse
import zipfile
import urllib.request
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Emu
except ImportError:  # pragma: no cover
    sys.exit(
        "Missing dependency. Run:  pip install python-pptx\n"
        "Then re-run this script."
    )


# ---------------------------------------------------------------------------
# Add a real Unicode "fade" transition to every slide by post-processing the
# saved .pptx (a ZIP). A <p:transition> element is valid as a direct child of
# <p:sld>, so we insert it just before the slide root closes. This gives the
# output PPTX a working fade between slides (approximating simple animation).
# ---------------------------------------------------------------------------
_FADE_XML = (
    b'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/'
    b'main" spd="med"><p:fade/></p:transition>'
)


def add_fade_transitions(pptx_path: Path) -> None:
    """Inject a fade transition into each slide of the finished .pptx (in place)."""
    tmp = pptx_path.with_suffix(pptx_path.suffix + ".tmp")
    try:
        with zipfile.ZipFile(str(pptx_path), "r") as zin, zipfile.ZipFile(
            str(tmp), "w", zipfile.ZIP_DEFLATED
        ) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if (
                    item.filename.startswith("ppt/slides/slide")
                    and item.filename.endswith(".xml")
                    and b"<p:transition" not in data
                ):
                    data = data.replace(b"</p:sld>", _FADE_XML + b"</p:sld>")
                zout.writestr(item, data)
        tmp.replace(pptx_path)
    except Exception:
        tmp.unlink(missing_ok=True)  # safety: never destroy the user's file


def natural_key(path: Path):
    """Sort so slide-2.png comes before slide-10.png."""
    return [
        int(part) if part.isdigit() else part
        for part in re.split(r"(\d+)", path.stem.lower())
    ]


_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff"}


def collect_images(folder: Path):
    """All slide images in `folder`, in natural order (slide-2 before slide-10)."""
    images = sorted(
        [p for p in folder.rglob("*") if p.suffix.lower() in _IMAGE_EXTS],
        key=natural_key,
    )
    if not images:
        sys.exit(f"No slide images found in: {folder}")
    return images


def build_from_folder(folder: Path, out_path: Path) -> int:
    images = collect_images(folder)

    print(f"Found {len(images)} slide image(s).")

    prs = Presentation()
    prs.slide_width = Emu(12192000)  # 16:9 -> 13.333in x 7.5in
    prs.slide_height = Emu(6858000)
    blank = prs.slide_layouts[6]

    sw, sh = prs.slide_width, prs.slide_height
    for idx, img in enumerate(images, start=1):
        slide = prs.slides.add_slide(blank)
        pic = slide.shapes.add_picture(str(img), 0, 0, sw, sh)
        pic.left = 0
        pic.top = 0
        # Aspect-preserve + center using the picture's native size.
        try:
            iw, ih = pic.width, pic.height
            scale = min(sw / iw, sh / ih)
            new_w, new_h = int(iw * scale), int(ih * scale)
            pic.width, pic.height = new_w, new_h
            pic.left = (sw - new_w) // 2
            pic.top = (sh - new_h) // 2
        except Exception:
            pass
        print(f"  [{idx}/{len(images)}] {img.name}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out_path))
    add_fade_transitions(out_path)
    print(f"\nDone! => {out_path.resolve()}")
    return 0


def build_pdf_from_folder(
    folder: Path, out_pdf: Path, page_width_pt: float = 960.0
) -> int:
    """One PDF page per slide image, each page sized to the image's aspect ratio."""
    try:
        import pymupdf  # type: ignore
    except ImportError:
        try:
            import fitz as pymupdf  # type: ignore
        except ImportError:
            sys.exit("PDF output needs PyMuPDF. Run:  pip install pymupdf")
    from PIL import Image

    images = collect_images(folder)
    print(f"Found {len(images)} slide image(s).")

    doc = pymupdf.open()
    for idx, img in enumerate(images, start=1):
        with Image.open(img) as im:
            w, h = im.size
        page_h = page_width_pt * h / w
        page = doc.new_page(width=page_width_pt, height=page_h)
        page.insert_image(
            pymupdf.Rect(0, 0, page_width_pt, page_h), filename=str(img)
        )
        print(f"  [{idx}/{len(images)}] {img.name}")

    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_pdf))
    doc.close()
    print(f"\nDone! => {out_pdf.resolve()}")
    return 0


def build_from_urls(url_file: Path, out_path: Path, image_dir: Path) -> int:
    """Download each URL in `url_file` into image_dir, then build the deck."""
    urls = [ln.strip() for ln in url_file.read_text().splitlines() if ln.strip()]
    if not urls:
        sys.exit("URL file is empty.")

    image_dir.mkdir(parents=True, exist_ok=True)
    local_paths = []
    for i, url in enumerate(urls, start=1):
        suffix = Path(url.rstrip("?")).suffix.lower()
        ext = suffix if suffix in (".png", ".jpg", ".jpeg", ".gif", ".webp") else ".png"
        dest = image_dir / f"slide-{i:03d}{ext}"
        print(f"Downloading {url} -> {dest}")
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (recovery-tool)"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                dest.write_bytes(resp.read())
        except Exception as exc:  # noqa: BLE001
            print(f"  ! failed to download {url}: {exc}", file=sys.stderr)
            continue
        local_paths.append(dest)

    if not local_paths:
        sys.exit("No images could be downloaded; nothing to build.")
    return build_images(image_dir, out_path)


def build_images(folder: Path, out_path: Path) -> int:
    """Dispatch on the output extension: .pdf -> PDF, anything else -> .pptx."""
    if out_path.suffix.lower() == ".pdf":
        return build_pdf_from_folder(folder, out_path)
    return build_from_folder(folder, out_path)


def render_pdf_to_images(pdf_path: Path, out_dir: Path, dpi: int = 200) -> int:
    """Rasterize every PDF page to a PNG (PyMuPDF; no external Poppler needed).

    Intended for a PDF you exported yourself from the presentation platform,
    so each page becomes one slide image.
    """
    try:
        import pymupdf  # type: ignore
    except ImportError:
        try:
            import fitz as pymupdf  # type: ignore
        except ImportError:
            sys.exit("PDF support needs PyMuPDF. Run:  pip install pymupdf")

    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(str(pdf_path))
    total = doc.page_count
    zoom = dpi / 72.0
    mat = pymupdf.Matrix(zoom, zoom)
    for i in range(total):
        pix = doc.load_page(i).get_pixmap(matrix=mat, alpha=False)
        dest = out_dir / f"slide-{i + 1:03d}.png"
        pix.save(str(dest))
        print(f"  page {i + 1}/{total} -> {dest.name}")
    doc.close()
    return total


def build_from_pdf(pdf_path: Path, out_path: Path, image_dir: Path) -> int:
    """Render a PDF's pages to images, then assemble them into a .pptx or .pdf."""
    print(f"Rendering PDF pages to images: {pdf_path}")
    render_pdf_to_images(pdf_path, image_dir)
    return build_from_folder(image_dir, out_path)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "source",
        help=(
            "Folder of slide images  OR  a .txt list of slide-image URLs  "
            "OR  a .pdf (e.g. a deck you exported yourself)"
        ),
    )
    ap.add_argument(
        "output",
        nargs="?",
        default="recovered_presentation.pptx",
        help="Output file; .pptx (default) or .pdf (one page per slide)",
    )
    ap.add_argument(
        "--download-first",
        action="store_true",
        help="When source is a .txt URL list, download the images before building",
    )
    ap.add_argument(
        "--image-dir",
        default="downloads",
        help="Folder where URL-downloaded images are stored",
    )
    ap.add_argument(
        "--pdf-image-dir",
        default="pdf_slides",
        help="Folder where PDF pages are rendered as PNGs",
    )
    ap.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="Resolution when rendering PDF pages (default 200)",
    )
    args = ap.parse_args(argv)

    src = Path(args.source)
    out = Path(args.output)

    if src.suffix.lower() == ".pdf":
        if not src.is_file():
            sys.exit(f"PDF not found: {src}")
        render_pdf_to_images(src, Path(args.pdf_image_dir), dpi=args.dpi)
        return build_images(Path(args.pdf_image_dir), out)

    if src.suffix.lower() == ".txt":
        if not args.download_first:
            sys.exit(
                "source is a URL list; pass --download-first to fetch images first"
            )
        return build_from_urls(src, out, Path(args.image_dir))

    if not src.is_dir():
        sys.exit(f"Source folder does not exist: {src}")
    return build_images(src, out)


if __name__ == "__main__":
    raise SystemExit(main())