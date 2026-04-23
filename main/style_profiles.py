"""
Style Profiles

Distinct visual/structural templates used to generate heterogeneous renderings
of the same document data. Each profile is injected into the generator prompt
so that a single JSON payload yields multiple real-world-looking variants.
"""

from dataclasses import dataclass


@dataclass
class StyleProfile:
    key: str
    name: str
    description: str


STYLE_PROFILES: list[StyleProfile] = [
    StyleProfile(
        key="compact_technical",
        name="Compact Technical",
        description=(
            "Dense layout with small 9pt Arial font, narrow margins, and thin gray lines between sections. "
            "Data in two-column pairs with alternating gray row shading, bold uppercase section headers. "
            "Company name top-left, document number top-right, legal footer at the bottom."
        ),
    ),
    StyleProfile(
        key="table_layout",
        name="Table Layout Style",
        description=(
            "All data organized in bordered tables with a dark header row and white text. "
            "Alternating row colors for readability, bold labels on the left, values on the right. "
            "Centered bold title at the top, nested tables for subsections like address or costs."
        ),
    ),
    StyleProfile(
        key="simple_form",
        name="Simple Form",
        description=(
            "Classic printable form with monospace font and dotted underlines where values go. "
            "Each field on its own line with bold label and generous spacing between fields. "
            "Signature area at the bottom with dotted lines for name, signature, and date."
        ),
    ),
    StyleProfile(
        key="minimal_modern",
        name="Minimal Modern",
        description=(
            "Clean sans-serif design with lots of whitespace and no tables or borders. "
            "Small gray uppercase labels stacked above their values, sections separated by space only. "
            "Thin left-aligned title with a single blue accent line underneath."
        ),
    ),
    StyleProfile(
        key="quick_note",
        name="Quick Note",
        description=(
            "Short summary fitting half a page with a bold title and thin line underneath. "
            "Only essential fields listed one per line in simple label-colon-value format. "
            "Light gray background, no tables or sections, feels like a quick internal memo."
        ),
    ),
]


def get_profiles() -> list[StyleProfile]:
    return STYLE_PROFILES

    