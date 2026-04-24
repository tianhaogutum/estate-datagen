"""
FastAPI backend for SyntheticDataGeneration UI.

Endpoints:
  GET  /api/meta/doctypes
  GET  /api/meta/systemtypes
  GET  /api/meta/scenarios
  GET  /api/meta/styles
  POST /api/generate/run           SSE stream — full pipeline
  POST /api/fn/schema              generate template schema
  POST /api/fn/data                fill data with LLM
  POST /api/fn/ontology            build ontology
  POST /api/fn/html                generate HTML
  POST /api/fn/fill                fill HTML
  POST /api/fn/pdf                 convert to PDF
  GET  /api/scenarios              list scenario dirs
  GET  /api/scenarios/{name}       return ontology.json for a scenario
  GET  /api/files/{path:path}      download any output file
"""

from __future__ import annotations

import json
import sys
import tempfile
import uuid
from collections.abc import AsyncGenerator
from pathlib import Path

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
MAIN = ROOT / "main"
OUTPUT_SCENARIOS = MAIN / "output_scenarios"
sys.path.insert(0, str(MAIN))

app = FastAPI(title="DataGen API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Meta endpoints ─────────────────────────────────────────────────────────────

DOC_TYPES = [
    {
        "key": "wartungsvertrag",
        "label": "Wartungsvertrag",
        "sub": "Maintenance Contract",
    },
    {
        "key": "wartungsprotokoll",
        "label": "Wartungsprotokoll",
        "sub": "Maintenance Protocol",
    },
]

SYSTEM_TYPES = [
    "KLIMAANLAGE",
    "WAERMEPUMPE",
    "HEIZKESSEL",
    "LUEFTUNGSANLAGE",
    "BRANDMELDEANLAGE",
    "SPRINKLER",
    "AUFZUG_PERSONEN",
    "ELEKTRISCHE_ANLAGE",
    "HEBEANLAGE_ABWASSER",
    "NOTSTROMAGGREGAT",
    "BLITZSCHUTZ",
    "RAUCHMELDER",
    "CO_WARNANLAGE",
    "DRUCKBEHAELTER",
    "ELEKTRISCHE_ANLAGE_MOBIL",
    "FEUERSCHUTZABSCHLUSS",
    "FEUERSCHUTZEINRICHTUNG_MANUELL",
    "FEUERSCHUTZTUER",
    "RAUCHSCHUTZ_RWA",
    "SANITAER_ALLG",
    "SICHERHEITSBELEUCHTUNG",
]

SCENARIOS_META = [
    {
        "key": "normal",
        "label": "Normal",
        "desc": "Fully coherent data, no anomalies",
        "tag": "Baseline",
    },
    {
        "key": "no_protocols",
        "label": "No Protocols",
        "desc": "Active contract but zero maintenance records",
        "tag": "Anomaly",
    },
    {
        "key": "multi_contract",
        "label": "Multi-Contract",
        "desc": "Multiple sequential contracts for same device",
        "tag": "Anomaly",
    },
    {
        "key": "protocol_outside_contract",
        "label": "Protocol Outside Contract",
        "desc": "Orphaned maintenance records without matching contract",
        "tag": "Anomaly",
    },
    {
        "key": "frequency_mismatch",
        "label": "Frequency Mismatch",
        "desc": "Actual maintenance frequency differs from contract",
        "tag": "Anomaly",
    },
    {
        "key": "address_mismatch",
        "label": "Address Mismatch",
        "desc": "Contract and protocol reference different addresses",
        "tag": "Anomaly",
    },
]

STYLES_META = [
    {
        "key": "corporate_formal",
        "label": "Corporate Formal",
        "desc": "Professional German corporate document",
    },
    {
        "key": "field_service_form",
        "label": "Field Service Form",
        "desc": "Printable form for field technicians",
    },
    {
        "key": "municipal_office",
        "label": "Municipal Office",
        "desc": "German public authority aesthetic",
    },
    {
        "key": "modern_saas",
        "label": "Modern SaaS",
        "desc": "Clean digital-first design",
    },
    {
        "key": "handwritten_scan",
        "label": "Handwritten / Scan",
        "desc": "Simulated hand-filled form scan",
    },
]


@app.get("/api/meta/doctypes")
def meta_doctypes():
    return DOC_TYPES


@app.get("/api/meta/systemtypes")
def meta_systemtypes():
    return SYSTEM_TYPES


@app.get("/api/meta/scenarios")
def meta_scenarios():
    return SCENARIOS_META


@app.get("/api/meta/styles")
def meta_styles():
    return STYLES_META


# ── Scenario browser ───────────────────────────────────────────────────────────


@app.get("/api/scenarios")
def list_scenarios():
    result = []
    if not OUTPUT_SCENARIOS.exists():
        return result
    for d in sorted(OUTPUT_SCENARIOS.iterdir()):
        if not d.is_dir():
            continue
        ont_path = d / "ontology.json"
        summary = {}
        if ont_path.exists():
            try:
                ont = json.loads(ont_path.read_text(encoding="utf-8"))
                summary = ont.get("summary", {})
            except Exception:
                pass
        result.append(
            {
                "id": d.name,
                "label": d.name.replace("_", " ").title(),
                "summary": summary,
            }
        )
    return result


@app.get("/api/scenarios/{name}")
def get_scenario(name: str):
    ont_path = OUTPUT_SCENARIOS / name / "ontology.json"
    if not ont_path.exists():
        return {"error": "ontology.json not found for this scenario"}
    return json.loads(ont_path.read_text(encoding="utf-8"))


# ── File download ──────────────────────────────────────────────────────────────


@app.get("/api/files/{path:path}")
def download_file(path: str):
    # only allow files under MAIN
    full = (MAIN / path).resolve()
    if not str(full).startswith(str(MAIN.resolve())):
        return {"error": "forbidden"}
    if not full.exists():
        return {"error": "not found"}
    return FileResponse(str(full), filename=full.name)


# ── Full pipeline (SSE) ────────────────────────────────────────────────────────


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def _run_pipeline(
    doc_types: list[str],
    system_type: str,
    scenario_key: str,
    style_key: str,
    run_id: str,
) -> AsyncGenerator[str, None]:
    import asyncio

    out_dir = MAIN / "output" / "pipeline" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    scenario_spec = MAIN / "scenario_specifications" / f"{scenario_key}.txt"

    def emit(step: str, msg: str, status: str = "running", extra: dict | None = None):
        payload = {"step": step, "msg": msg, "status": status}
        if extra:
            payload.update(extra)
        return _sse("progress", payload)

    # ── Step 1: Generate template schema ──────────────────────────────────────
    yield emit("schema", "Generating template schema…")
    await asyncio.sleep(0)

    from data_schema_generator import generate_template

    template_paths: list[Path] = []
    templates: list[dict] = []
    for doc_key in doc_types:
        try:
            tpl = generate_template(doc_key, system_type)
            tpl_path = out_dir / f"{doc_key}_template.json"
            tpl_path.write_text(
                json.dumps(tpl, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            template_paths.append(tpl_path)
            templates.append(tpl)
        except Exception as e:
            yield emit("schema", f"Error: {e}", "error")
            return

    yield emit("schema", f"Generated {len(templates)} template(s)", "done")
    await asyncio.sleep(0)

    # ── Step 2: Fill data with LLM ─────────────────────────────────────────────
    yield emit("data", "Filling data with LLM (this takes ~20s)…")
    await asyncio.sleep(0)

    from data_samples_generator import generate_data_multi

    try:
        results = await asyncio.get_event_loop().run_in_executor(
            None, generate_data_multi, templates, scenario_spec
        )
    except Exception as e:
        yield emit("data", f"Error: {e}", "error")
        return

    data_paths: list[Path] = []
    for doc_key, res in zip(doc_types, results):
        data_path = out_dir / f"{doc_key}_data.json"
        data_path.write_text(
            json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        data_paths.append(data_path)

    yield emit("data", f"Data filled for {len(results)} document(s)", "done")
    await asyncio.sleep(0)

    # ── Step 3: Build ontology ─────────────────────────────────────────────────
    yield emit("ontology", "Building ontology view…")
    await asyncio.sleep(0)

    from ontology_view import build_ontology

    ont_path = out_dir / "ontology.json"
    try:
        ontology = build_ontology(data_paths)
        ont_path.write_text(
            json.dumps(ontology, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    except Exception as e:
        yield emit("ontology", f"Warning: {e}", "done")
        ontology = {}

    ont_rel = str(ont_path.relative_to(MAIN))
    yield emit(
        "ontology",
        "Ontology tree built",
        "done",
        {"file": ont_rel, "summary": ontology.get("summary", {})},
    )
    await asyncio.sleep(0)

    # ── Step 4: Generate HTML layout ───────────────────────────────────────────
    yield emit("html", f"Generating HTML layout (style: {style_key})…")
    await asyncio.sleep(0)

    from html_generator import generate_html_variants
    from style_profiles import STYLE_PROFILES

    all_style_keys = [p.key for p in STYLE_PROFILES]
    style_keys = all_style_keys if style_key == "all" else [style_key]

    html_paths: list[Path] = []
    # map each html variant back to which doc_key/data it belongs to
    html_to_data: dict[str, Path] = {}

    for doc_key, tpl_path, data_path in zip(doc_types, template_paths, data_paths):
        out_stem = out_dir / f"{doc_key}"
        try:
            variants = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda dk=doc_key, tp=tpl_path, st=out_stem: generate_html_variants(
                    json.loads(tp.read_text(encoding="utf-8")),
                    dk,
                    style_keys,
                    st,
                    use_few_shots=True,
                ),
            )
            for v in variants:
                if v.get("status") == "ok":
                    hp = Path(v["html"])
                    html_paths.append(hp)
                    html_to_data[str(hp)] = data_path
        except Exception as e:
            yield emit("html", f"Error: {e}", "error")
            return

    yield emit("html", f"Generated {len(html_paths)} HTML file(s)", "done")
    await asyncio.sleep(0)

    # ── Step 5: Fill HTML placeholders ─────────────────────────────────────────
    yield emit("fill", "Filling HTML placeholders…")
    await asyncio.sleep(0)

    from fill_html import fill_html

    filled_paths: list[Path] = []
    for html_path in html_paths:
        data_path = html_to_data.get(str(html_path), data_paths[0])
        try:
            data = json.loads(data_path.read_text(encoding="utf-8"))
            raw_html = html_path.read_text(encoding="utf-8")
            filled = fill_html(raw_html, data)
            filled_path = html_path.with_stem(html_path.stem + "_filled")
            filled_path.write_text(filled, encoding="utf-8")
            filled_paths.append(filled_path)
        except Exception as e:
            yield emit("fill", f"Error: {e}", "error")
            return

    yield emit("fill", f"Filled {len(filled_paths)} file(s)", "done")
    await asyncio.sleep(0)

    # ── Step 6: Convert to PDF ─────────────────────────────────────────────────
    yield emit("pdf", "Converting to PDF via Playwright…")
    await asyncio.sleep(0)

    from pdf_converter import convert_html_to_pdf

    pdf_paths: list[Path] = []
    for fp in filled_paths:
        try:
            pdf_path = await asyncio.get_event_loop().run_in_executor(
                None, convert_html_to_pdf, fp
            )
            pdf_paths.append(pdf_path)
        except Exception as e:
            yield emit("pdf", f"PDF conversion error: {e}", "error")
            return

    yield emit("pdf", f"Converted {len(pdf_paths)} PDF(s)", "done")
    await asyncio.sleep(0)

    # ── Done ───────────────────────────────────────────────────────────────────
    files = []
    for p in pdf_paths:
        files.append({"name": p.name, "type": "pdf", "path": str(p.relative_to(MAIN))})
    for p in filled_paths:
        files.append({"name": p.name, "type": "html", "path": str(p.relative_to(MAIN))})
    for p in data_paths:
        files.append({"name": p.name, "type": "json", "path": str(p.relative_to(MAIN))})

    ont_file = {"name": "ontology.json", "type": "ontology", "path": ont_rel}
    files.append(ont_file)

    yield _sse(
        "done",
        {
            "run_id": run_id,
            "files": files,
            "ontology": ontology,
        },
    )


@app.get("/api/generate/run")
async def generate_run(
    doc_types: str,
    system_type: str,
    scenario: str,
    style: str,
):
    run_id = str(uuid.uuid4())[:8]
    doc_list = [d.strip() for d in doc_types.split(",") if d.strip()]

    return StreamingResponse(
        _run_pipeline(doc_list, system_type, scenario, style, run_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Individual function endpoints ─────────────────────────────────────────────


@app.post("/api/fn/schema")
async def fn_schema(doc_type: str = Form(...), system_type: str = Form(...)):
    import asyncio

    from data_schema_generator import generate_template

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, generate_template, doc_type, system_type)
    return result


@app.post("/api/fn/data")
async def fn_data(
    scenario: str = Form(...),
    files: list[UploadFile] = File(...),
):
    import asyncio

    from data_samples_generator import generate_data_multi

    spec_path = MAIN / "scenario_specifications" / f"{scenario}.txt"
    if not spec_path.exists():
        return {"error": f"Scenario spec not found: {scenario}"}

    templates = []
    for f in files:
        content = await f.read()
        templates.append(json.loads(content))

    loop = asyncio.get_event_loop()
    results = await loop.run_in_executor(
        None, generate_data_multi, templates, spec_path
    )
    return {"results": results}


@app.post("/api/fn/ontology")
async def fn_ontology(files: list[UploadFile] = File(...)):
    import asyncio

    from ontology_view import build_ontology

    tmp_dir = Path(tempfile.mkdtemp())
    paths = []
    for f in files:
        content = await f.read()
        p = tmp_dir / f.filename
        p.write_bytes(content)
        paths.append(p)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, build_ontology, paths)
    return result


@app.post("/api/fn/html")
async def fn_html(
    doc_type: str = Form(...),
    style_key: str = Form("all"),
    file: UploadFile = File(...),
):
    import asyncio

    from html_generator import generate_html_variants
    from style_profiles import STYLE_PROFILES

    content = await file.read()
    template = json.loads(content)

    all_style_keys = [p.key for p in STYLE_PROFILES]
    style_keys = all_style_keys if style_key == "all" else [style_key]

    tmp_dir = Path(tempfile.mkdtemp())
    out_stem = tmp_dir / "document"

    loop = asyncio.get_event_loop()
    variants = await loop.run_in_executor(
        None,
        lambda: generate_html_variants(
            template, doc_type, style_keys, out_stem, use_few_shots=True
        ),
    )

    results = []
    for v in variants:
        if v.get("status") == "ok":
            hp = Path(v["html"])
            results.append(
                {
                    "style": v["style"],
                    "name": hp.name,
                    "content": hp.read_text(encoding="utf-8"),
                }
            )
    return {"variants": results}


@app.post("/api/fn/fill")
async def fn_fill(
    data_file: UploadFile = File(...),
    html_file: UploadFile = File(...),
):
    from fill_html import fill_html

    data = json.loads(await data_file.read())
    raw_html = (await html_file.read()).decode("utf-8")
    filled = fill_html(raw_html, data)
    return {"filled_html": filled}


@app.post("/api/fn/pdf")
async def fn_pdf(files: list[UploadFile] = File(...)):
    import asyncio

    from pdf_converter import convert_html_to_pdf

    tmp_dir = Path(tempfile.mkdtemp())
    results = []
    loop = asyncio.get_event_loop()

    for f in files:
        content = await f.read()
        html_path = tmp_dir / f.filename
        html_path.write_bytes(content)
        try:
            pdf_path = await loop.run_in_executor(None, convert_html_to_pdf, html_path)
            results.append({"name": pdf_path.name, "path": str(pdf_path)})
        except Exception as e:
            results.append({"name": f.filename, "error": str(e)})

    return {"pdfs": results}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
