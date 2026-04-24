# SyntheticDataGeneration — System Flowchart

## Pipeline

```mermaid
flowchart TD
    A["📄 Document Requirements\n+ Entity Schemas\n+ Scenario Spec\n+ Example PDFs"]

    B["① Template Generation\ndata_schema_generator.py\n─────────────────────────\nClaude reads requirements & entity schema\n→ outputs JSON with ‹Label› placeholders"]

    C["② Data Filling\ndata_samples_generator.py\n─────────────────────────\nSingle LLM call fills contract + protocols\ntogether with real German values\n⭐ Cross-document consistency guaranteed"]

    D["③ HTML Layout Generation\nhtml_generator.py\n─────────────────────────\nClaude Vision + few-shot PDFs\n→ 5 style variants in parallel\n⭐ corporate / field / municipal / SaaS / handwritten"]

    E["④ Placeholder Filling\nfill_html.py\n─────────────────────────\nFlatten JSON → key-value dict\nReplace every &lt;Label&gt; in HTML with real data"]

    F["⑤ PDF Conversion\npdf_converter.py\n─────────────────────────\nPlaywright headless Chromium\nHTML → A4 PDF"]

    G["⑥ Ontology Assembly\nontology_view.py\n─────────────────────────\nFuzzy-match protocols → contracts\nBuild 4-level hierarchy tree\n⭐ EconomicUnit→Building→Device→Contract→Protocol"]

    H["📦 Final Output\n• 5 × HTML  • 5 × PDF\n• Filled Data JSON\n• Ontology JSON"]

    A --> B --> C --> D --> E --> F --> G --> H
```

---

## Overall Architecture & Innovations

```mermaid
flowchart TD
    %% ─── Input Layer ─────────────────────────────────────────────────────
    subgraph INPUT["📥  Input Layer"]
        direction LR
        REQ["📄 Document Requirements\ndocument_requirements/\n21+ system types\n(KLIMAANLAGE, AUFZUG…)"]
        META["🗃️ Entity Schemas\nentities_meta/\nfields / enums / FK constraints\n(wartungsvertrag.json…)"]
        SCENARIO["⚠️ Scenario Specs\nscenario_specifications/\nnormal / no_protocols /\naddress_mismatch…"]
        FEWSHOT["🖼️ Example PDFs\nfew_shots/\nReal German documents\n(few-shot visual prompts)"]
    end

    %% ─── Step 1 ──────────────────────────────────────────────────────────
    subgraph STEP1["① Template Generation  ·  data_schema_generator.py"]
        S1["🤖 Claude via AWS Bedrock\nReads requirements + entity schema\n→ Generates JSON skeleton with ‹Label› placeholders"]
        S1_OUT["📋 Template JSON\n{\n  meta: { entity, fields },\n  required: { Anlagentyp: ‹Typ›… },\n  optional: { Reaktionszeit: ‹Wert›… }\n}"]
        S1 --> S1_OUT
    end

    %% ─── Step 2 ──────────────────────────────────────────────────────────
    subgraph STEP2["② Data Filling  ·  data_samples_generator.py"]
        S2["🤖 Claude  ——  Single Batched LLM Call\nAll templates merged into one prompt\nReplaces every ‹Label› with real German values"]
        S2_INN1(["⭐ Innovation ①\nSingle LLM call fills contract\n+ protocols together, guaranteeing\ncross-document data consistency"])
        S2_INN2(["⭐ Innovation ②\nScenario-driven anomaly injection\nControlled defect generation\nfor data quality testing"])
        S2_OUT["📊 Filled Data JSON\n{\n  meta: { device_type: Klimaanlage,\n          contract_start: 2023-01-01… },\n  required: { Typ: Klimaanlage,\n              Hersteller: Mitsubishi… }\n}"]
        S2 --> S2_INN1
        S2 --> S2_INN2
        S2 --> S2_OUT
    end

    %% ─── Step 3 ──────────────────────────────────────────────────────────
    subgraph STEP3["③ HTML Layout Generation  ·  html_generator.py"]
        S3_VIS["🤖 Claude Vision\nReceives base64-encoded PDF example blocks\nLearns layout patterns from real documents"]
        S3_PAR["⚡ ThreadPoolExecutor\n5 style variants generated in parallel\n(same dataset → diverse renderings)"]
        S3_INN3(["⭐ Innovation ③\nFew-shot PDF visual prompting\nGuides LLM to produce more\nrealistic HTML layouts"])
        S3_INN4(["⭐ Innovation ④\n5 declarative style variants\nSame data, different appearance\nCovers diverse real-world use cases"])
        S3_STYLES["🎨 5 × HTML (with ‹Label› placeholders)\n① corporate_formal   — German corporate formal\n② field_service_form  — Technician printout\n③ municipal_office   — Public authority style\n④ modern_saas        — Digital SaaS export\n⑤ handwritten_scan   — Scanned handwritten form"]
        S3_VIS --> S3_PAR
        S3_PAR --> S3_INN3
        S3_PAR --> S3_INN4
        S3_PAR --> S3_STYLES
    end

    %% ─── Step 4 ──────────────────────────────────────────────────────────
    subgraph STEP4["④ Placeholder Filling  ·  fill_html.py"]
        S4["Flatten nested JSON → key→value dict\nReplace every &lt;Label&gt; in HTML\nBooleans → ja / nein (German)"]
        S4_OUT["🌐 Filled HTML\nAll placeholders replaced with real data"]
        S4 --> S4_OUT
    end

    %% ─── Step 5 ──────────────────────────────────────────────────────────
    subgraph STEP5["⑤ PDF Conversion  ·  pdf_converter.py"]
        S5["🖨️ Playwright Headless Chromium\nA4 format / print background enabled\nHTML → PDF rendering"]
        S5_OUT["📄 PDF Document\nPrintable German maintenance file"]
        S5 --> S5_OUT
    end

    %% ─── Ontology Assembly ───────────────────────────────────────────────
    subgraph ONTO["🌳 Ontology Assembly  ·  ontology_view.py"]
        ONT["Load all Filled Data JSONs\nGroup by entity type"]
        ONT_MATCH["Fuzzy protocol ↔ contract matching\n① Exact contract_id\n② device_type + address substring\n③ Fallback: bind to first contract"]
        ONT_INN5(["⭐ Innovation ⑤\nFuzzy matching without full IDs\nRecovers hierarchical semantic\nrelations from flat JSON files"])
        ONT_TREE["Build 4-level hierarchy\nEconomicUnit → Building → Device → Contract → Protocol"]
        ONT_OUT["📦 Ontology JSON\n{\n  summary: { units:2, buildings:4,\n             contracts:8, protocols:16 },\n  economic_units: [ … full hierarchy … ]\n}"]
        ONT --> ONT_MATCH --> ONT_INN5 --> ONT_TREE --> ONT_OUT
    end

    %% ─── Data Flow ───────────────────────────────────────────────────────
    REQ      --> S1
    META     --> S1
    S1_OUT   --> S2
    SCENARIO --> S2
    S1_OUT   --> S3_VIS
    FEWSHOT  --> S3_VIS
    S2_OUT   --> S3_PAR
    S2_OUT   --> S4
    S3_STYLES --> S4
    S4_OUT   --> S5
    S2_OUT   --> ONT

    %% ─── Styles ──────────────────────────────────────────────────────────
    classDef innov fill:#fff9c4,stroke:#f9a825,stroke-width:2px,color:#333
    classDef io    fill:#e8f5e9,stroke:#388e3c,stroke-width:1.5px
    classDef llm   fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef step  fill:#fce4ec,stroke:#c62828,stroke-width:1px
    classDef out   fill:#f3e5f5,stroke:#6a1b9a,stroke-width:1.5px

    class S2_INN1,S2_INN2,S3_INN3,S3_INN4,ONT_INN5 innov
    class REQ,META,SCENARIO,FEWSHOT io
    class S1,S2,S3_VIS llm
    class S4,S5,ONT_MATCH,ONT_TREE step
    class S1_OUT,S2_OUT,S3_STYLES,S4_OUT,S5_OUT,ONT_OUT out
```

---

## Five Key Innovations

```mermaid
mindmap
  root((SyntheticData\nGeneration\nInnovations))
    Innovation① Cross-Document Consistency
      Single LLM call generates multiple documents
      Contract and protocols share one prompt context
      Building address / device type / dates are identical
      Eliminates semantic drift from separate generation calls
    Innovation② Scenario-Driven Anomaly Injection
      6 anomaly scenario specification files
      normal — fully coherent baseline data
      no_protocols — contract with zero maintenance records
      multi_contract — overlapping contracts for same device
      protocol_outside_contract — date outside contract period
      frequency_mismatch — maintenance frequency violation
      address_mismatch — location mismatch between documents
    Innovation③ Few-Shot PDF Visual Prompting
      Real PDFs encoded as base64 injected into prompt
      Claude Vision learns real document layout patterns
      Produces more realistic HTML layouts
    Innovation④ 5 Declarative Style Variants
      ThreadPoolExecutor generates all 5 in parallel
      Styles described in natural language for LLM reasoning
      Same data × 5 appearances = diverse training set
      Covers corporate / field / municipal / SaaS / handwritten
    Innovation⑤ Fuzzy Ontology Matching
      Graceful degradation when IDs are incomplete
      device_type + address substring fuzzy linking
      Recovers hierarchical semantics from flat JSON
      Builds verifiable 4-level knowledge tree
```

---

## Data Model

```mermaid
erDiagram
    EconomicUnit ||--o{ Building : "owns"
    Building     ||--o{ Device   : "hosts"
    Device       ||--o{ MaintenanceContract : "covered by"
    MaintenanceContract ||--o{ MaintenanceProtocol : "produces"

    EconomicUnit {
        string name     "Unit name"
        string contact  "Contact person"
        string phone    "Phone number"
    }
    Building {
        string address  "Street address"
        string type     "Büro/Wohn/Geschäft"
    }
    Device {
        string device_type   "Device type (enum)"
        string manufacturer  "Manufacturer"
        string serial_number "Serial number"
    }
    MaintenanceContract {
        uuid   id                    "Contract ID (PK)"
        uuid   building_id           "Building ID (FK)"
        date   contract_start        "Contract start date"
        date   contract_end          "Contract end date"
        string maintenance_frequency "Jährlich / Halbjährlich"
        float  cost_per_maintenance  "Cost per visit (EUR)"
    }
    MaintenanceProtocol {
        uuid   id               "Protocol ID (PK)"
        uuid   contract_id      "Contract ID (FK)"
        date   maintenance_date "Service date"
        string result           "Maintenance result"
        string technician       "Technician name"
    }
```

---

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| LLM Inference | Claude Sonnet 4.6 via AWS Bedrock | Template generation / data filling / HTML layout |
| Parallelism | `concurrent.futures.ThreadPoolExecutor` | 5 style HTML variants generated concurrently |
| PDF Rendering | Playwright Headless Chromium | HTML → A4 PDF conversion |
| Multimodal Input | Claude Vision + base64 PDF blocks | Few-shot layout learning from real documents |
| Data Serialization | JSON + Python data classes | Templates / data / ontology interchange |
| AWS Integration | boto3 | Bedrock API calls |
