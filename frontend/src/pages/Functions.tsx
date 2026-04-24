import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

const SYSTEM_TYPES = [
  'KLIMAANLAGE', 'WAERMEPUMPE', 'HEIZKESSEL', 'LUEFTUNGSANLAGE',
  'BRANDMELDEANLAGE', 'SPRINKLER', 'AUFZUG_PERSONEN', 'ELEKTRISCHE_ANLAGE',
  'HEBEANLAGE_ABWASSER', 'NOTSTROMAGGREGAT', 'BLITZSCHUTZ', 'RAUCHMELDER',
  'CO_WARNANLAGE', 'DRUCKBEHAELTER', 'ELEKTRISCHE_ANLAGE_MOBIL',
  'FEUERSCHUTZABSCHLUSS', 'FEUERSCHUTZEINRICHTUNG_MANUELL', 'FEUERSCHUTZTUER',
  'RAUCHSCHUTZ_RWA', 'SANITAER_ALLG', 'SICHERHEITSBELEUCHTUNG',
]

const SCENARIO_SPECS = ['normal', 'no_protocols', 'multi_contract', 'protocol_outside_contract', 'frequency_mismatch', 'address_mismatch']
const STYLES = ['corporate_formal', 'field_service_form', 'municipal_office', 'modern_saas', 'handwritten_scan']

const FUNCTIONS = [
  {
    key: 'schema',
    icon: '🧩',
    label: 'Generate Template',
    sub: 'data_schema_generator.py',
    desc: 'Generate a placeholder-only JSON template for a specific document and system type using the LLM.',
    color: '#5ac8fa',
  },
  {
    key: 'data',
    icon: '🤖',
    label: 'Generate Data',
    sub: 'data_samples_generator.py',
    desc: 'Fill one or more template JSONs with realistic German data in a single LLM call, ensuring cross-document consistency.',
    color: '#0071e3',
  },
  {
    key: 'ontology',
    icon: '🌳',
    label: 'Build Ontology',
    sub: 'ontology_view.py',
    desc: 'Assemble data JSON files into a hierarchical ontology tree: EconomicUnit → Building → Device → Contract → Protocol.',
    color: '#34c759',
  },
  {
    key: 'html',
    icon: '🎨',
    label: 'Generate HTML',
    sub: 'html_generator.py',
    desc: 'Generate HTML document layouts with placeholder labels using the LLM and optional few-shot PDF examples.',
    color: '#ff9500',
  },
  {
    key: 'fill',
    icon: '✏️',
    label: 'Fill HTML',
    sub: 'fill_html.py',
    desc: 'Replace all <label> placeholders in an HTML template with real values from a data JSON.',
    color: '#af52de',
  },
  {
    key: 'pdf',
    icon: '📄',
    label: 'Convert to PDF',
    sub: 'pdf_converter.py',
    desc: 'Convert filled HTML files to A4 PDFs using a headless Chromium browser via Playwright.',
    color: '#ff3b30',
  },
]

function Spinner() {
  return (
    <div
      className="animate-spin-slow"
      style={{
        width: 18,
        height: 18,
        borderRadius: '50%',
        border: '2px solid #0071e3',
        borderTopColor: 'transparent',
        display: 'inline-block',
      }}
    />
  )
}

function OutputBlock({ data, loading }: { data: Record<string, unknown> | null; loading: boolean }) {
  if (loading) return (
    <div style={{ padding: 24, display: 'flex', alignItems: 'center', gap: 10, color: '#6e6e73', fontSize: 14 }}>
      <Spinner /> Running…
    </div>
  )
  if (!data) return (
    <div style={{ padding: 24, color: '#86868b', fontSize: 14 }}>
      Output will appear here after you run the function.
    </div>
  )
  return (
    <div className="code-block" style={{ maxHeight: 360, overflowY: 'auto', borderRadius: '0 0 14px 14px' }}>
      {JSON.stringify(data, null, 2)}
    </div>
  )
}

function FnSchema() {
  const [docType, setDocType] = useState('wartungsvertrag')
  const [sysType, setSysType] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [error, setError] = useState('')

  async function run() {
    setLoading(true); setError('')
    try {
      const fd = new FormData()
      fd.append('doc_type', docType)
      fd.append('system_type', sysType)
      const res = await fetch('/api/fn/schema', { method: 'POST', body: fd })
      const data = await res.json()
      if (data.error) { setError(data.error); setResult(null) } else { setResult(data) }
    } catch (e) { setError(String(e)) }
    setLoading(false)
  }

  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
        <div>
          <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Document type</label>
          <select className="input" value={docType} onChange={(e) => setDocType(e.target.value)}>
            <option value="wartungsvertrag">Wartungsvertrag</option>
            <option value="wartungsprotokoll">Wartungsprotokoll</option>
          </select>
        </div>
        <div>
          <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>System type</label>
          <select className="input" value={sysType} onChange={(e) => setSysType(e.target.value)}>
            <option value="">Select…</option>
            {SYSTEM_TYPES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
      </div>
      <button className="btn btn-primary btn-sm" onClick={run} disabled={!sysType || loading}>
        {loading ? <><Spinner /> Running</> : 'Run'}
      </button>
      {error && <div style={{ marginTop: 8, color: '#ff3b30', fontSize: 13 }}>{error}</div>}
      <div style={{ marginTop: 16, background: '#1c1c1e', borderRadius: 14 }}>
        <div style={{ padding: '12px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 12, color: '#86868b', fontFamily: 'monospace' }}>output / template.json</span>
          {result && (
            <button className="btn btn-sm" style={{ background: 'rgba(255,255,255,0.1)', color: '#fff', fontSize: 12 }}
              onClick={() => { const a = document.createElement('a'); a.href = 'data:application/json,' + encodeURIComponent(JSON.stringify(result, null, 2)); a.download = 'template.json'; a.click() }}>
              Download
            </button>
          )}
        </div>
        <OutputBlock data={result} loading={loading} />
      </div>
    </div>
  )
}

function FnData() {
  const [scenario, setScenario] = useState('normal')
  const [files, setFiles] = useState<FileList | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [error, setError] = useState('')

  async function run() {
    if (!files?.length) return
    setLoading(true); setError('')
    try {
      const fd = new FormData()
      fd.append('scenario', scenario)
      Array.from(files).forEach((f) => fd.append('files', f))
      const res = await fetch('/api/fn/data', { method: 'POST', body: fd })
      const data = await res.json()
      if (data.error) { setError(data.error); setResult(null) } else { setResult(data) }
    } catch (e) { setError(String(e)) }
    setLoading(false)
  }

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Upload template JSON(s)</label>
        <input type="file" className="input" accept=".json" multiple style={{ cursor: 'pointer' }} onChange={(e) => setFiles(e.target.files)} />
      </div>
      <div style={{ marginBottom: 16 }}>
        <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Scenario specification</label>
        <select className="input" value={scenario} onChange={(e) => setScenario(e.target.value)}>
          {SCENARIO_SPECS.map((s) => <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>)}
        </select>
      </div>
      <button className="btn btn-primary btn-sm" onClick={run} disabled={loading || !files?.length}>
        {loading ? <><Spinner /> Running LLM</> : 'Run'}
      </button>
      {error && <div style={{ marginTop: 8, color: '#ff3b30', fontSize: 13 }}>{error}</div>}
      <div style={{ marginTop: 16, background: '#1c1c1e', borderRadius: 14 }}>
        <div style={{ padding: '12px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 12, color: '#86868b', fontFamily: 'monospace' }}>output / data.json</span>
          {result && (
            <button className="btn btn-sm" style={{ background: 'rgba(255,255,255,0.1)', color: '#fff', fontSize: 12 }}
              onClick={() => { const a = document.createElement('a'); a.href = 'data:application/json,' + encodeURIComponent(JSON.stringify(result, null, 2)); a.download = 'data.json'; a.click() }}>
              Download
            </button>
          )}
        </div>
        <OutputBlock data={result} loading={loading} />
      </div>
    </div>
  )
}

function FnOntology() {
  const [files, setFiles] = useState<FileList | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [error, setError] = useState('')

  async function run() {
    if (!files?.length) return
    setLoading(true); setError('')
    try {
      const fd = new FormData()
      Array.from(files).forEach((f) => fd.append('files', f))
      const res = await fetch('/api/fn/ontology', { method: 'POST', body: fd })
      const data = await res.json()
      if (data.error) { setError(data.error); setResult(null) } else { setResult(data) }
    } catch (e) { setError(String(e)) }
    setLoading(false)
  }

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Upload data JSON files (Contract + Protocol)</label>
        <input type="file" className="input" accept=".json" multiple style={{ cursor: 'pointer' }} onChange={(e) => setFiles(e.target.files)} />
      </div>
      <button className="btn btn-primary btn-sm" onClick={run} disabled={loading || !files?.length}>
        {loading ? <><Spinner /> Building</> : 'Run'}
      </button>
      {error && <div style={{ marginTop: 8, color: '#ff3b30', fontSize: 13 }}>{error}</div>}
      <div style={{ marginTop: 16, background: '#1c1c1e', borderRadius: 14 }}>
        <div style={{ padding: '12px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 12, color: '#86868b', fontFamily: 'monospace' }}>output / ontology.json</span>
          {result && (
            <button className="btn btn-sm" style={{ background: 'rgba(255,255,255,0.1)', color: '#fff', fontSize: 12 }}
              onClick={() => { const a = document.createElement('a'); a.href = 'data:application/json,' + encodeURIComponent(JSON.stringify(result, null, 2)); a.download = 'ontology.json'; a.click() }}>
              Download
            </button>
          )}
        </div>
        <OutputBlock data={result} loading={loading} />
      </div>
    </div>
  )
}

function FnHtml() {
  const [docType, setDocType] = useState('wartungsvertrag')
  const [styleKey, setStyleKey] = useState('all')
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [error, setError] = useState('')

  async function run() {
    if (!file) return
    setLoading(true); setError('')
    try {
      const fd = new FormData()
      fd.append('doc_type', docType)
      fd.append('style_key', styleKey)
      fd.append('file', file)
      const res = await fetch('/api/fn/html', { method: 'POST', body: fd })
      const data = await res.json()
      if (data.error) { setError(data.error); setResult(null) } else { setResult(data) }
    } catch (e) { setError(String(e)) }
    setLoading(false)
  }

  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
        <div>
          <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Upload template JSON</label>
          <input type="file" className="input" accept=".json" style={{ cursor: 'pointer' }} onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        </div>
        <div>
          <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Document type</label>
          <select className="input" value={docType} onChange={(e) => setDocType(e.target.value)}>
            <option value="wartungsvertrag">Wartungsvertrag</option>
            <option value="wartungsprotokoll">Wartungsprotokoll</option>
          </select>
        </div>
      </div>
      <div style={{ marginBottom: 16 }}>
        <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Style</label>
        <select className="input" value={styleKey} onChange={(e) => setStyleKey(e.target.value)} style={{ maxWidth: 300 }}>
          <option value="all">All styles</option>
          {STYLES.map((s) => <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>)}
        </select>
      </div>
      <button className="btn btn-primary btn-sm" onClick={run} disabled={loading || !file}>
        {loading ? <><Spinner /> Running LLM</> : 'Run'}
      </button>
      {error && <div style={{ marginTop: 8, color: '#ff3b30', fontSize: 13 }}>{error}</div>}
      <div style={{ marginTop: 16, background: '#1c1c1e', borderRadius: 14 }}>
        <div style={{ padding: '12px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
          <span style={{ fontSize: 12, color: '#86868b', fontFamily: 'monospace' }}>output / html/</span>
        </div>
        <OutputBlock data={result} loading={loading} />
      </div>
    </div>
  )
}

function FnFill() {
  const [dataFile, setDataFile] = useState<File | null>(null)
  const [htmlFile, setHtmlFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [error, setError] = useState('')

  async function run() {
    if (!dataFile || !htmlFile) return
    setLoading(true); setError('')
    try {
      const fd = new FormData()
      fd.append('data_file', dataFile)
      fd.append('html_file', htmlFile)
      const res = await fetch('/api/fn/fill', { method: 'POST', body: fd })
      const data = await res.json()
      if (data.error) { setError(data.error); setResult(null) } else { setResult(data) }
    } catch (e) { setError(String(e)) }
    setLoading(false)
  }

  return (
    <div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
        <div>
          <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Data JSON</label>
          <input type="file" className="input" accept=".json" style={{ cursor: 'pointer' }} onChange={(e) => setDataFile(e.target.files?.[0] ?? null)} />
        </div>
        <div>
          <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>HTML template</label>
          <input type="file" className="input" accept=".html" style={{ cursor: 'pointer' }} onChange={(e) => setHtmlFile(e.target.files?.[0] ?? null)} />
        </div>
      </div>
      <button className="btn btn-primary btn-sm" onClick={run} disabled={loading || !dataFile || !htmlFile}>
        {loading ? <><Spinner /> Filling</> : 'Run'}
      </button>
      {error && <div style={{ marginTop: 8, color: '#ff3b30', fontSize: 13 }}>{error}</div>}
      <div style={{ marginTop: 16, background: '#1c1c1e', borderRadius: 14 }}>
        <div style={{ padding: '12px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: 12, color: '#86868b', fontFamily: 'monospace' }}>output / filled.html</span>
          {result?.filled_html && <div style={{ display: 'flex', gap: 8 }}>
            <button className="btn btn-sm" style={{ background: 'rgba(255,255,255,0.1)', color: '#fff', fontSize: 12 }}
              onClick={() => { const w = window.open(); w?.document.write(result.filled_html as string) }}>
              Preview
            </button>
            <button className="btn btn-sm" style={{ background: 'rgba(255,255,255,0.1)', color: '#fff', fontSize: 12 }}
              onClick={() => { const a = document.createElement('a'); a.href = 'data:text/html,' + encodeURIComponent(result.filled_html as string); a.download = 'filled.html'; a.click() }}>
              Download
            </button>
          </div>}
        </div>
        <OutputBlock data={result?.filled_html ? { filled_html: '(HTML content ready — use Preview/Download above)' } : result} loading={loading} />
      </div>
    </div>
  )
}

function FnPdf() {
  const [files, setFiles] = useState<FileList | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [error, setError] = useState('')

  async function run() {
    if (!files?.length) return
    setLoading(true); setError('')
    try {
      const fd = new FormData()
      Array.from(files).forEach((f) => fd.append('files', f))
      const res = await fetch('/api/fn/pdf', { method: 'POST', body: fd })
      const data = await res.json()
      if (data.error) { setError(data.error); setResult(null) } else { setResult(data) }
    } catch (e) { setError(String(e)) }
    setLoading(false)
  }

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <label style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f', display: 'block', marginBottom: 6 }}>Upload filled HTML file(s)</label>
        <input type="file" className="input" accept=".html" multiple style={{ cursor: 'pointer' }} onChange={(e) => setFiles(e.target.files)} />
      </div>
      <button className="btn btn-primary btn-sm" onClick={run} disabled={loading || !files?.length}>
        {loading ? <><Spinner /> Converting</> : 'Run'}
      </button>
      {error && <div style={{ marginTop: 8, color: '#ff3b30', fontSize: 13 }}>{error}</div>}
      <div style={{ marginTop: 16, background: '#1c1c1e', borderRadius: 14 }}>
        <div style={{ padding: '12px 18px', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
          <span style={{ fontSize: 12, color: '#86868b', fontFamily: 'monospace' }}>output / pdfs/</span>
        </div>
        <OutputBlock data={result} loading={loading} />
      </div>
    </div>
  )
}

const FN_PANELS: Record<string, React.ReactNode> = {
  schema: <FnSchema />,
  data: <FnData />,
  ontology: <FnOntology />,
  html: <FnHtml />,
  fill: <FnFill />,
  pdf: <FnPdf />,
}

export default function Functions() {
  const { fn } = useParams<{ fn: string }>()
  const nav = useNavigate()
  const active = fn || FUNCTIONS[0].key

  const activeFn = FUNCTIONS.find((f) => f.key === active) ?? FUNCTIONS[0]

  return (
    <div style={{ maxWidth: 1120, margin: '0 auto', padding: '48px 24px', display: 'flex', gap: 32 }}>
      {/* Sidebar */}
      <aside style={{ width: 220, flexShrink: 0 }}>
        <p className="label-eyebrow" style={{ marginBottom: 16 }}>Functions</p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
          {FUNCTIONS.map((f) => (
            <button
              key={f.key}
              onClick={() => nav(`/functions/${f.key}`)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                padding: '10px 14px',
                borderRadius: 10,
                border: 'none',
                background: active === f.key ? 'rgba(0,113,227,0.10)' : 'transparent',
                color: active === f.key ? '#0071e3' : '#1d1d1f',
                fontWeight: active === f.key ? 600 : 400,
                fontSize: 14,
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'all 0.15s',
                letterSpacing: '-0.01em',
              }}
            >
              <span style={{ fontSize: 16 }}>{f.icon}</span>
              {f.label}
            </button>
          ))}
        </div>
      </aside>

      {/* Main panel */}
      <main style={{ flex: 1, minWidth: 0 }}>
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
            <div
              style={{
                width: 40,
                height: 40,
                borderRadius: 12,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 20,
                background: `${activeFn.color}18`,
              }}
            >
              {activeFn.icon}
            </div>
            <div>
              <h1 style={{ fontSize: 26, fontWeight: 700, letterSpacing: '-0.03em', color: '#1d1d1f' }}>
                {activeFn.label}
              </h1>
              <code style={{ fontSize: 12, color: '#86868b', background: 'rgba(0,0,0,0.05)', padding: '2px 8px', borderRadius: 6 }}>
                {activeFn.sub}
              </code>
            </div>
          </div>
          <p style={{ fontSize: 15, color: '#6e6e73', lineHeight: 1.6 }}>{activeFn.desc}</p>
        </div>

        <div className="card" style={{ padding: 28 }}>
          {FN_PANELS[active] ?? <p style={{ color: '#86868b' }}>Select a function from the sidebar.</p>}
        </div>

        {/* Use as input chain hint */}
        {active !== FUNCTIONS[FUNCTIONS.length - 1].key && (
          <div
            style={{
              marginTop: 16,
              padding: '12px 16px',
              background: 'rgba(0,113,227,0.06)',
              borderRadius: 10,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <span style={{ fontSize: 13, color: '#0071e3' }}>
              Use the output of this step as input for the next function
            </span>
            <button
              className="btn btn-sm"
              style={{ background: 'rgba(0,113,227,0.12)', color: '#0071e3', fontSize: 13 }}
              onClick={() => {
                const idx = FUNCTIONS.findIndex((f) => f.key === active)
                if (idx < FUNCTIONS.length - 1) nav(`/functions/${FUNCTIONS[idx + 1].key}`)
              }}
            >
              Next: {FUNCTIONS[(FUNCTIONS.findIndex((f) => f.key === active) + 1) % FUNCTIONS.length].label} →
            </button>
          </div>
        )}
      </main>
    </div>
  )
}
