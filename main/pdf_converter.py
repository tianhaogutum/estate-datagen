"""
PDF Converter

Converts HTML files to PDF using pdfkit (wkhtmltopdf wrapper).

Usage:
    python pdf_converter.py <html_file_or_directory>
"""

from pathlib import Path

import pdfkit


def convert_html_to_pdf(html_path: Path) -> Path:
    pdf_path = html_path.with_suffix(".pdf")
    pdfkit.from_file(str(html_path), str(pdf_path))
    print(f"PDF saved: {pdf_path}")
    return pdf_path


def convert_variants(variants: list[dict]) -> list[dict]:
    for v in variants:
        if v["status"] != "ok":
            continue
        html_path = Path(v["html"])
        try:
            pdf_path = convert_html_to_pdf(html_path)
            v["pdf"] = str(pdf_path)
        except Exception as e:
            print(f"PDF conversion failed for {v['profile']}: {e}")
            v["pdf_error"] = str(e)
    return variants


if __name__ == "__main__":
    import sys

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

    if target.is_file() and target.suffix == ".html":
        convert_html_to_pdf(target)
    elif target.is_dir():
        html_files = sorted(target.glob("*.html"))
        if not html_files:
            raise SystemExit(f"No HTML files found in {target}")
        for f in html_files:
            try:
                convert_html_to_pdf(f)
            except Exception as e:
                print(f"FAILED {f.name}: {e}")
    else:
        raise SystemExit(f"Expected an HTML file or directory, got: {target}")
