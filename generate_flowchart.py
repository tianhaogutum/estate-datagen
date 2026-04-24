import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(11, 18))
ax.set_xlim(0, 10)
ax.set_ylim(0, 18)
ax.axis("off")
fig.patch.set_facecolor("#FAFAFA")

# ── color palette ──────────────────────────────────────────────
C_INPUT = "#E3F2FD"  # blue-50
C_LLM = "#EDE7F6"  # purple-50
C_PROC = "#E8F5E9"  # green-50
C_OUT = "#FFF8E1"  # amber-50
C_BORDER = "#546E7A"
C_ARROW = "#37474F"
C_BADGE = "#FF8F00"


def box(ax, x, y, w, h, title, lines, color, title_color="#1A237E", badge=None):
    rect = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.08",
        linewidth=1.5,
        edgecolor=C_BORDER,
        facecolor=color,
        zorder=2,
    )
    ax.add_patch(rect)

    # title
    ty = y + h / 2 - 0.22
    ax.text(
        x,
        ty,
        title,
        ha="center",
        va="top",
        fontsize=9.5,
        fontweight="bold",
        color=title_color,
        zorder=3,
    )

    # divider line
    ax.plot(
        [x - w / 2 + 0.15, x + w / 2 - 0.15],
        [ty - 0.26, ty - 0.26],
        color=C_BORDER,
        lw=0.8,
        alpha=0.5,
        zorder=3,
    )

    # body text
    body = "\n".join(lines)
    ax.text(
        x,
        ty - 0.36,
        body,
        ha="center",
        va="top",
        fontsize=7.8,
        color="#263238",
        zorder=3,
        linespacing=1.5,
    )

    # innovation badge
    if badge:
        ax.text(
            x + w / 2 - 0.12,
            y + h / 2 - 0.12,
            badge,
            ha="right",
            va="top",
            fontsize=7.5,
            color=C_BADGE,
            fontweight="bold",
            zorder=4,
        )


def arrow(ax, y_top, y_bot, label=""):
    mx = 5.0
    ax.annotate(
        "",
        xy=(mx, y_bot + 0.01),
        xytext=(mx, y_top - 0.01),
        arrowprops=dict(arrowstyle="-|>", color=C_ARROW, lw=1.6, mutation_scale=14),
        zorder=3,
    )
    if label:
        ax.text(
            mx + 0.18,
            (y_top + y_bot) / 2,
            label,
            ha="left",
            va="center",
            fontsize=7,
            color="#546E7A",
            style="italic",
        )


# ── Y positions (top of each box) ──────────────────────────────
Y = [17.0, 14.5, 11.8, 9.0, 6.4, 3.8, 1.2]
H = [1.4, 1.8, 2.0, 2.0, 1.7, 1.5, 1.2]
cx = 5.0
W = 8.5

centers = [y - h / 2 for y, h in zip(Y, H)]  # vertical center of each box

# ── Box 0 — Inputs ─────────────────────────────────────────────
box(
    ax,
    cx,
    centers[0],
    W,
    H[0],
    "INPUT",
    ["Document Requirements  ·  Entity Schemas  ·  Scenario Specs  ·  Example PDFs"],
    C_INPUT,
    title_color="#0D47A1",
)

# ── Box 1 — Template Generation ────────────────────────────────
box(
    ax,
    cx,
    centers[1],
    W,
    H[1],
    "① Generate Template Schema",
    [
        "data_schema_generator.py",
        "Claude (AWS Bedrock) reads requirements + entity schema",
        "→ Outputs JSON skeleton with <Label> placeholders",
    ],
    C_LLM,
    title_color="#4527A0",
)

# ── Box 2 — Data Filling ───────────────────────────────────────
box(
    ax,
    cx,
    centers[2],
    W,
    H[2],
    "② Fill Data with LLM",
    [
        "data_samples_generator.py",
        "Single LLM call fills contract + protocols together",
        "→ Real German values replacing all placeholders",
        "Scenario spec injected to control anomaly type",
    ],
    C_LLM,
    title_color="#4527A0",
    badge="[*] Cross-doc Consistency",
)

# ── Box 3 — HTML Layout ────────────────────────────────────────
box(
    ax,
    cx,
    centers[3],
    W,
    H[3],
    "③ Generate HTML Layout",
    [
        "html_generator.py",
        "Claude Vision + base64 few-shot PDFs → learns real layout",
        "5 style variants generated in parallel (ThreadPoolExecutor)",
        "corporate · field · municipal · SaaS · handwritten",
    ],
    C_LLM,
    title_color="#4527A0",
    badge="[*] Few-shot Vision + 5 Styles",
)

# ── Box 4 — Fill HTML ──────────────────────────────────────────
box(
    ax,
    cx,
    centers[4],
    W,
    H[4],
    "④ Fill HTML Placeholders",
    [
        "fill_html.py",
        "Flatten nested JSON → key-value dict",
        "Replace every <Label> in HTML with real data value",
    ],
    C_PROC,
    title_color="#1B5E20",
)

# ── Box 5 — PDF ────────────────────────────────────────────────
box(
    ax,
    cx,
    centers[5],
    W,
    H[5],
    "⑤ Convert to PDF",
    [
        "pdf_converter.py",
        "Playwright headless Chromium  ·  A4 format",
        "→ Printable German maintenance document",
    ],
    C_PROC,
    title_color="#1B5E20",
)

# ── Box 6 — Ontology ───────────────────────────────────────────
box(
    ax,
    cx,
    centers[6],
    W,
    H[6],
    "⑥ Build Ontology View",
    [
        "ontology_view.py  ·  Fuzzy protocol ↔ contract matching",
        "EconomicUnit → Building → Device → Contract → Protocol",
    ],
    C_OUT,
    title_color="#E65100",
    badge="[*] Fuzzy Matching",
)

# ── Arrows ─────────────────────────────────────────────────────
labels = [
    "Template JSON",
    "Filled Data JSON",
    "HTML + Filled Data",
    "Filled HTML",
    "PDF + JSON",
]
for i in range(len(centers) - 1):
    y_top = centers[i] - H[i] / 2
    y_bot = centers[i + 1] + H[i + 1] / 2
    lbl = labels[i] if i < len(labels) else ""
    arrow(ax, y_top, y_bot, lbl)

# ── Title ──────────────────────────────────────────────────────
ax.text(
    cx,
    17.8,
    "SyntheticDataGeneration — Pipeline",
    ha="center",
    va="center",
    fontsize=13,
    fontweight="bold",
    color="#212121",
)

plt.tight_layout(pad=0.3)
plt.savefig(
    "flowchart.png", dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor()
)
print("Saved: flowchart.png")
