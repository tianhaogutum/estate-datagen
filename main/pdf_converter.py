"""
PDF Converter

Converts HTML files to PDF using Playwright (headless Chromium).

Usage:
    python pdf_converter.py <html_file_or_directory>
"""

from pathlib import Path

from playwright.sync_api import sync_playwright


def convert_html_to_pdf(html_path: Path) -> Path:
    pdf_path = html_path.with_suffix(".pdf")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path.resolve()}")
        page.pdf(path=str(pdf_path), format="A4", print_background=True)
        browser.close()
    print(f"PDF saved: {pdf_path}")
    return pdf_path


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
