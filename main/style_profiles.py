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
            "Professional German corporate document style. "
            "White background, serif font (Georgia or Times New Roman) at 10pt. "
            "Company letterhead at the top with logo placeholder (gray rectangle, top-left), "
            "company name bold 14pt, address line in gray 8pt beside it. "
            "Document title centered, bold, 13pt, with a 2px solid dark-blue line beneath. "
            "Section headings bold 10pt with a thin bottom border. "
            "Data rendered as two-column label/value pairs inside a borderless table, "
            "label column width 40%, gray color; value column normal weight black. "
            "Signature block at the bottom: two columns (Auftraggeber / Auftragnehmer), "
            "each with a 60px dotted underline for the signature, name, and date beneath. "
            "Footer: thin top border, document number left, page number right, 8pt gray."
        ),
    ),
    StyleProfile(
        key="field_service_form",
        name="Field Service Form",
        description=(
            "Practical printable form used by field technicians. "
            "Clean Arial 10pt on white, narrow margins (1.5cm all sides). "
            "Bold document title top-center with document number and date top-right in a small box. "
            "Each section is a bordered box (1px solid #555) with a dark-gray filled header bar "
            "(white text, bold, 9pt uppercase) and content rows inside. "
            "Each field is a row with the label left-aligned (bold, 35% width) and a light-gray "
            "underlined input area on the right taking the remaining width. "
            "Checklist items rendered as checkbox squares (□) followed by the item text. "
            "Signature section at bottom: three side-by-side boxes for Techniker, Kunde, Datum "
            "each with a dotted line and small label beneath. "
            "Compact — designed to fit on 1–2 A4 pages."
        ),
    ),
    StyleProfile(
        key="municipal_office",
        name="Municipal / Authority Office",
        description=(
            "German public-authority document aesthetic. "
            "Strict grid layout, Helvetica/Arial 10pt. "
            "Top header band: full-width light-blue (#dce8f5) bar containing the issuing "
            "authority name (bold, left) and a coat-of-arms placeholder circle (right). "
            "Document type and reference number on the next line, left-aligned, gray. "
            "Main content in a two-column HTML table with alternating row shading "
            "(white / #f2f5f9). Left column: bold field label with field code in brackets "
            "(e.g. 'Anlagentyp [AT]'), right column: value. "
            "Multi-value fields (lists) shown as numbered sub-rows inside the cell. "
            "Bottom section: stamped 'Geprüft' placeholder box (dashed border, gray text) "
            "beside the signature area. "
            "Footer: full-width gray bar with office address, phone, Aktenzeichen."
        ),
    ),
    StyleProfile(
        key="modern_saas",
        name="Modern SaaS / Digital Platform",
        description=(
            "Clean digital-first design as exported from a modern German property-management SaaS. "
            "White page, system font stack (Inter, Segoe UI, sans-serif) 10pt. "
            "Top navigation bar: solid #1a1a2e background, company name white bold left, "
            "document ID and status badge (green rounded pill 'Aktiv') right. "
            "Document title below nav: large 18pt bold, subtitle in gray 11pt. "
            "Content split into cards: each card has a white background, 8px border-radius, "
            "subtle box-shadow, 16px internal padding, and a colored left accent bar (4px, #4a90d9). "
            "Card headers bold 11pt #1a1a2e. Fields inside: small gray label (8pt uppercase tracking), "
            "value below in 10pt black. Lists rendered as pill tags (#e8f0fe background, #1a56db text). "
            "Signature section: two styled input boxes with dashed bottom border only. "
            "No outer page border. Bottom: thin gray line, generated timestamp right-aligned 8pt."
        ),
    ),
    StyleProfile(
        key="handwritten_scan",
        name="Handwritten / Scanned Form",
        description=(
            "Simulate a pre-printed paper form that has been partially filled by hand and scanned. "
            "Off-white (#faf8f3) background with very subtle paper texture (use CSS noise via "
            "box-shadow or background-image pattern). "
            "Pre-printed sections in Arial 9pt dark gray. "
            "Filled-in values rendered in a slightly imperfect handwriting-style font "
            "(use 'Caveat', 'Patrick Hand', or cursive fallback) at 11pt dark-blue (#1a237e), "
            "slightly rotated (transform: rotate(-0.3deg)) to mimic real handwriting. "
            "Form fields are underlined lines (border-bottom 1px solid #aaa) with the handwritten "
            "value sitting on top. "
            "Checkboxes shown as hand-drawn X marks inside square boxes. "
            "A faint diagonal 'KOPIE' watermark in light gray across the page center. "
            "Signature areas show a cursive placeholder squiggle. "
            "Overall effect: authentic scanned maintenance record."
        ),
    ),
]


def get_profiles() -> list[StyleProfile]:
    return STYLE_PROFILES
