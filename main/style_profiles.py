"""
Style Profiles

Distinct visual/structural templates used to generate heterogeneous renderings
of the same document data. Each profile is injected into the generator prompt
so that a single JSON payload yields multiple real-world-looking variants.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class StyleProfile:
    key: str
    name: str
    description: str


STYLE_PROFILES: List[StyleProfile] = [
    StyleProfile(
        key="corporate_formal",
        name="Corporate Formal",
        description=(
            "Classic corporate letter style. Serif headings (Georgia/Times), "
            "bold section titles in ALL CAPS, dense multi-column tables for "
            "field/value pairs, subtle horizontal rules between sections, "
            "right-aligned page numbers, footer with company contact block. "
            "Feels like a printed enterprise document from a large utility company."
        ),
    ),
    StyleProfile(
        key="minimal_modern",
        name="Minimal Modern",
        description=(
            "Minimalist contemporary layout. Sans-serif throughout (Helvetica/Inter), "
            "lots of whitespace, thin 1px dividers, left-aligned labels in light gray "
            "with bold dark values, NO table borders, section headings as oversized "
            "lightweight numerals (01, 02, ...). Looks like a modern startup PDF."
        ),
    ),
    StyleProfile(
        key="classical_legal",
        name="Classical Legal",
        description=(
            "Traditional German legal document style. Serif body text justified, "
            "numbered paragraphs (§ 1, § 2, ...), bold paragraph titles, indented "
            "sub-clauses, Fraktur-feel heading at top, signature lines at bottom "
            "with dotted leaders, centered document title. Feels like a notary contract."
        ),
    ),
    StyleProfile(
        key="compact_form",
        name="Compact Technical Form",
        description=(
            "Dense technical form with checkbox grids. Monospace or condensed "
            "sans-serif, small font size (9-10pt), heavy use of bordered tables, "
            "checkboxes (☐/☑) for pass/fail results, labeled input fields with "
            "underlines, top-right revision/form number, dark header bar with "
            "white text. Feels like a field technician service report."
        ),
    ),
    StyleProfile(
        key="letterhead_branded",
        name="Branded Letterhead",
        description=(
            "Branded letterhead style. Colored header band (muted blue or green) "
            "with a placeholder logo block on the left and contractor address on "
            "the right, body in a friendly sans-serif, callout boxes for key data "
            "(dates, costs), two-tone color scheme, footer with horizontal brand bar. "
            "Feels like a mid-size service company's customer-facing document."
        ),
    ),
]


def get_profiles() -> List[StyleProfile]:
    return STYLE_PROFILES
