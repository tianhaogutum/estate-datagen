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
]


def get_profiles() -> list[StyleProfile]:
    return STYLE_PROFILES
