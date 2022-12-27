import argparse
import os
import tempfile
from pathlib import Path
from typing import List

from PyPDF2 import PdfWriter
from reportlab.graphics import renderPDF  # type: ignore
from svglib.svglib import svg2rlg  # type: ignore

from parse import parse
from render import render


def svg2pdf(svg: Path, pdf: Path) -> None:
    drawing = svg2rlg(svg)
    renderPDF.drawToFile(drawing, str(pdf))


def merge_pdf(output: Path, pdfs: List[Path]) -> None:
    merger = PdfWriter()
    for path in pdfs:
        merger.append(str(path))
    merger.write(str(output))
    merger.close()


def replace_suffix(path: Path, suffix: str) -> Path:
    return Path(os.path.splitext(path)[0] + suffix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("title")
    parser.add_argument("--yratio", type=float, default=1.414)  # A4
    parser.add_argument("--pdf", type=Path)
    args = parser.parse_args()

    subtitle, title = args.title.split("{sub}", 1)

    svgs = render(parse(args.file), title, subtitle, args.yratio)

    if args.pdf:
        with tempfile.TemporaryDirectory() as _tmpdir:
            tmpdir = Path(_tmpdir)
            pdf_paths = []

            for i, svg in enumerate(svgs):
                page_path = tmpdir / f"tmp_{i}.svg"
                pdf_page_path = tmpdir / f"tmp_{i}.pdf"
                pdf_paths.append(pdf_page_path)
                page_path.write_text(str(svg))
                svg2pdf(page_path, pdf_page_path)

            merge_pdf(args.pdf, pdf_paths)
    else:
        # One line per page
        print("\n".join(str(svg) for svg in svgs))


if __name__ == "__main__":
    main()
