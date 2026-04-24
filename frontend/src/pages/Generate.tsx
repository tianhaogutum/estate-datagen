import { useState, useRef } from 'react'

const DOC_TYPES = [
  { key: 'wartungsvertrag', label: 'Wartungsvertrag', sub: 'Maintenance Contract', icon: '📄' },
  { key: 'wartungsprotokoll', label: 'Wartungsprotokoll', sub: 'Maintenance Protocol', icon: '📋' },
]

const STYLES = [
  { key: 'corporate_formal', label: 'Corporate Formal', desc: 'Professional German corporate document' },
  { key: 'field_service_form', label: 'Field Service Form', desc: 'Printable form for field technicians' },
  { key: 'municipal_office', label: 'Municipal Office', desc: 'German public authority aesthetic' },
  { key: 'modern_saas', label: 'Modern SaaS', desc: 'Clean digital-first design' },
  { key: 'handwritten_scan', label: 'Handwritten / Scan', desc: 'Simulated hand-filled form scan' },
]

const STEPS = ['Documents', 'Style', 'Generate']

type StepStatus = 'done' | 'active' | 'pending'

function StepIndicator({ current }: { current: number }) {
  const statuses: StepStatus[] = STEPS.map((_, i) => {
    if (i < current) return 'done'
    if (i === current) return 'active'
    return 'pending'
  })

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 0, marginBottom: 48 }}>
      {STEPS.map((label, i) => (
        <div
          key={label}
          style={{ display: 'flex', alignItems: 'center', flex: i < STEPS.length - 1 ? 1 : 'none' }}
        >
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6 }}>
            <div
              style={{
                width: 28, height: 28, borderRadius: '50%', display: 'flex', alignItems: 'center',
                justifyContent: 'center', fontSize: 12, fontWeight: 600,
                background: statuses[i] !== 'pending' ? '#0071e3' : 'rgba(0,0,0,0.08)',
                color: statuses[i] === 'pending' ? '#6e6e73' : '#fff',
                transition: 'all 0.3s',
              }}
            >
              {statuses[i] === 'done' ? (
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <path d="M2 6l3 3 5-5" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              ) : (
                i + 1
              )}
            </div>
            <span style={{ fontSize: 11, color: statuses[i] === 'pending' ? '#86868b' : '#1d1d1f', fontWeight: statuses[i] === 'active' ? 600 : 400, whiteSpace: 'nowrap' }}>
              {label}
            </span>
          </div>
          {i < STEPS.length - 1 && (
            <div style={{ flex: 1, height: 2, marginBottom: 18, background: statuses[i] === 'done' ? '#0071e3' : 'rgba(0,0,0,0.08)', transition: 'background 0.3s' }} />
          )}
        </div>
      ))}
    </div>
  )
}

type JobStep = { label: string; status: 'pending' | 'running' | 'done' | 'error'; msg?: string }

function ProgressPanel({ steps }: { steps: JobStep[] }) {
  return (
    <div className="card" style={{ padding: 32 }}>
      <h3 style={{ fontSize: 20, fontWeight: 600, letterSpacing: '-0.02em', marginBottom: 24 }}>Generating…</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {steps.map((s, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            <div style={{
              width: 28, height: 28, borderRadius: '50%', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
              background: s.status === 'done' ? 'rgba(52,199,89,0.15)' : s.status === 'running' ? 'rgba(0,113,227,0.12)' : s.status === 'error' ? 'rgba(255,59,48,0.12)' : 'rgba(0,0,0,0.06)',
            }}>
              {s.status === 'done' && (
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                  <path d="M2 6.5l3.5 3.5 5.5-5.5" stroke="#34c759" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
              {s.status === 'running' && (
                <div className="animate-spin-slow" style={{ width: 14, height: 14, borderRadius: '50%', border: '2px solid #0071e3', borderTopColor: 'transparent' }} />
              )}
              {s.status === 'error' && (
                <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
                  <path d="M3 3l7 7M10 3l-7 7" stroke="#ff3b30" strokeWidth="1.8" strokeLinecap="round" />
                </svg>
              )}
              {s.status === 'pending' && <div style={{ width: 6, height: 6, borderRadius: '50%', background: '#c7c7cc' }} />}
            </div>
            <div>
              <div style={{ fontSize: 15, fontWeight: s.status === 'running' ? 500 : 400, color: s.status === 'pending' ? '#86868b' : '#1d1d1f' }}>{s.label}</div>
              {s.msg && <div style={{ fontSize: 13, color: '#6e6e73', marginTop: 2 }}>{s.msg}</div>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Ontology tree components ────────────────────────────────────────────────

type Protocol = { maintenance_date: string; result_deficiency: string; performed_by: string }
type Contract = {
  contract_id: string; service_provider: string; contract_date: string;
  contract_start: string; contract_end: string; maintenance_frequency: string;
  cost_per_maintenance: number; protocols: { count: number; entries: Protocol[] }
}
type Device = { device_type: string; contract: Contract }
type Building = { address: string; device_count: number; devices: Device[] }
type EconomicUnit = { name: string; building_count: number; buildings: Building[] }
type OntologyData = {
  summary?: Record<string, number>
  economic_units?: EconomicUnit[]
}

function ProtocolRow({ p }: { p: Protocol }) {
  return (
    <div style={{ padding: '10px 14px', background: 'rgba(0,0,0,0.02)', borderRadius: 8, marginTop: 6 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 3 }}>
        <span style={{ fontSize: 13, fontWeight: 500, color: '#1d1d1f' }}>{p.maintenance_date}</span>
        <span className="tag tag-green" style={{ fontSize: 11 }}>Protocol</span>
      </div>
      <div style={{ fontSize: 12, color: '#6e6e73', lineHeight: 1.5 }}>{p.result_deficiency}</div>
      <div style={{ fontSize: 11, color: '#86868b', marginTop: 2 }}>by {p.performed_by}</div>
    </div>
  )
}

function ContractNode({ contract, deviceType }: { contract: Contract; deviceType: string }) {
  const [open, setOpen] = useState(false)
  return (
    <div style={{ border: '1px solid rgba(0,113,227,0.15)', borderRadius: 12, overflow: 'hidden', marginTop: 8 }}>
      <button onClick={() => setOpen((v) => !v)} style={{ width: '100%', background: open ? 'rgba(0,113,227,0.06)' : '#fff', border: 'none', cursor: 'pointer', padding: '12px 16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', textAlign: 'left', transition: 'background 0.15s' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ width: 24, height: 24, borderRadius: 6, background: 'rgba(0,113,227,0.10)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 12 }}>📄</div>
          <div>
            <div style={{ fontSize: 13, fontWeight: 600, color: '#1d1d1f' }}>{deviceType}</div>
            <div style={{ fontSize: 11, color: '#86868b' }}>{contract.contract_id} · {contract.service_provider}</div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span className="tag tag-blue" style={{ fontSize: 11 }}>{contract.maintenance_frequency}</span>
          <span style={{ fontSize: 11, color: '#86868b' }}>€{contract.cost_per_maintenance?.toLocaleString()}</span>
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s', color: '#6e6e73' }}>
            <path d="M2 4l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </button>
      {open && (
        <div style={{ padding: '4px 16px 16px', borderTop: '1px solid rgba(0,0,0,0.06)' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 8, marginTop: 10 }}>
            {[
              ['Period', `${contract.contract_start} – ${contract.contract_end}`],
              ['Signed', contract.contract_date],
              ['Provider', contract.service_provider],
            ].map(([k, v]) => (
              <div key={k}>
                <div style={{ fontSize: 11, color: '#86868b', marginBottom: 2 }}>{k}</div>
                <div style={{ fontSize: 13, color: '#1d1d1f' }}>{v}</div>
              </div>
            ))}
          </div>
          {contract.protocols.count > 0 ? (
            <div>
              <div style={{ fontSize: 12, fontWeight: 600, color: '#0071e3', marginTop: 8, marginBottom: 4 }}>
                {contract.protocols.count} Protocol{contract.protocols.count !== 1 ? 's' : ''}
              </div>
              {contract.protocols.entries.map((p, i) => <ProtocolRow key={i} p={p} />)}
            </div>
          ) : (
            <div style={{ fontSize: 12, color: '#86868b', marginTop: 8 }}>No protocols recorded</div>
          )}
        </div>
      )}
    </div>
  )
}

function BuildingNode({ building }: { building: Building }) {
  const [open, setOpen] = useState(true)
  return (
    <div style={{ marginTop: 12, border: '1px solid rgba(0,0,0,0.08)', borderRadius: 14, overflow: 'hidden' }}>
      <button onClick={() => setOpen((v) => !v)} style={{ width: '100%', background: '#f9f9fb', border: 'none', cursor: 'pointer', padding: '14px 18px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', textAlign: 'left' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ width: 28, height: 28, borderRadius: 8, background: 'rgba(52,199,89,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 14 }}>🏢</div>
          <div>
            <div style={{ fontSize: 14, fontWeight: 600, color: '#1d1d1f' }}>{building.address}</div>
            <div style={{ fontSize: 12, color: '#86868b' }}>{building.device_count} device{building.device_count !== 1 ? 's' : ''}</div>
          </div>
        </div>
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s', color: '#6e6e73' }}>
          <path d="M2 4l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
      {open && (
        <div style={{ padding: '8px 18px 18px' }}>
          {building.devices.map((d, i) => <ContractNode key={i} deviceType={d.device_type} contract={d.contract} />)}
        </div>
      )}
    </div>
  )
}

function UnitNode({ unit }: { unit: EconomicUnit }) {
  const [open, setOpen] = useState(true)
  return (
    <div className="card" style={{ marginBottom: 16, overflow: 'hidden', padding: 0 }}>
      <button onClick={() => setOpen((v) => !v)} style={{ width: '100%', background: 'transparent', border: 'none', cursor: 'pointer', padding: '20px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', textAlign: 'left' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: 'linear-gradient(135deg,#0071e3,#34aadc)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 17 }}>🏗</div>
          <div>
            <div style={{ fontSize: 17, fontWeight: 600, color: '#1d1d1f', letterSpacing: '-0.01em' }}>{unit.name}</div>
            <div style={{ fontSize: 13, color: '#86868b' }}>{unit.building_count} building{unit.building_count !== 1 ? 's' : ''}</div>
          </div>
        </div>
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" style={{ transform: open ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s', color: '#6e6e73' }}>
          <path d="M2 5l5 5 5-5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </button>
      {open && (
        <div style={{ padding: '0 24px 24px', borderTop: '1px solid rgba(0,0,0,0.06)' }}>
          {unit.buildings.map((b, i) => <BuildingNode key={i} building={b} />)}
        </div>
      )}
    </div>
  )
}

// ── Main component ──────────────────────────────────────────────────────────

type OutputFile = { name: string; type: string; path: string }

const STEP_KEYS = ['schema', 'data', 'ontology', 'html', 'fill', 'pdf']
const STEP_LABELS: Record<string, string> = {
  schema: 'Generate template schema',
  data: 'Fill data with LLM',
  ontology: 'Build ontology view',
  html: 'Generate HTML layout',
  fill: 'Fill HTML placeholders',
  pdf: 'Convert to PDF',
}

export default function Generate() {
  const [step, setStep] = useState(0)
  const [docTypes, setDocTypes] = useState<string[]>([])
  const [style, setStyle] = useState('')
  const [running, setRunning] = useState(false)
  const [done, setDone] = useState(false)
  const [jobSteps, setJobSteps] = useState<JobStep[]>(
    STEP_KEYS.map((k) => ({ label: STEP_LABELS[k], status: 'pending' }))
  )
  const [outputFiles, setOutputFiles] = useState<OutputFile[]>([])
  const [ontology, setOntology] = useState<OntologyData | null>(null)
  const esRef = useRef<EventSource | null>(null)

  const toggleDoc = (key: string) =>
    setDocTypes((prev) => prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key])

  const canNext = [docTypes.length > 0, !!style][step] ?? true

  function reset() {
    esRef.current?.close()
    setRunning(false); setDone(false); setStep(0)
    setDocTypes([]); setStyle('')
    setOutputFiles([]); setOntology(null)
    setJobSteps(STEP_KEYS.map((k) => ({ label: STEP_LABELS[k], status: 'pending' })))
  }

  function runPipeline() {
    setRunning(true)
    setJobSteps(STEP_KEYS.map((k) => ({ label: STEP_LABELS[k], status: 'pending' })))

    const params = new URLSearchParams({
      doc_types: docTypes.join(','),
      system_type: 'KLIMAANLAGE',
      scenario: 'normal',
      style,
    })
    const es = new EventSource(`/api/generate/run?${params}`)
    esRef.current = es

    es.addEventListener('progress', (e: MessageEvent) => {
      const data = JSON.parse(e.data) as { step: string; msg: string; status: string }
      const stepIdx = STEP_KEYS.indexOf(data.step)
      if (stepIdx === -1) return
      setJobSteps((prev) =>
        prev.map((s, i) =>
          i === stepIdx ? { ...s, status: data.status as JobStep['status'], msg: data.msg }
            : i < stepIdx ? { ...s, status: 'done' }
            : s
        )
      )
    })

    es.addEventListener('done', (e: MessageEvent) => {
      es.close()
      const data = JSON.parse(e.data) as { files: OutputFile[]; ontology: OntologyData }
      setOutputFiles(data.files ?? [])
      setOntology(data.ontology ?? null)
      setDone(true)
      setJobSteps((prev) => prev.map((s) => ({ ...s, status: 'done' })))
    })

    es.onerror = () => {
      es.close()
      setJobSteps((prev) =>
        prev.map((s) => s.status === 'running' ? { ...s, status: 'error', msg: 'Connection lost' } : s)
      )
    }
  }

  if (running) {
    return (
      <div style={{ maxWidth: 800, margin: '60px auto', padding: '0 24px' }}>
        <div style={{ marginBottom: 28 }}>
          <p className="label-eyebrow" style={{ marginBottom: 8 }}>Full Pipeline</p>
          <h1 style={{ fontSize: 'clamp(24px,3.5vw,40px)', fontWeight: 700, letterSpacing: '-0.03em', color: '#1d1d1f' }}>
            {done ? 'Generation complete' : 'Generating…'}
          </h1>
        </div>

        <ProgressPanel steps={jobSteps} />

        {done && (
          <div className="animate-fade-up" style={{ marginTop: 28, display: 'flex', flexDirection: 'column', gap: 20 }}>

            {/* PDF downloads */}
            {outputFiles.filter((f) => f.type === 'pdf').length > 0 && (
              <div className="card" style={{ padding: 28 }}>
                <h3 style={{ fontSize: 18, fontWeight: 600, letterSpacing: '-0.02em', marginBottom: 16 }}>
                  Generated PDFs
                </h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                  {outputFiles.filter((f) => f.type === 'pdf').map((f) => (
                    <div key={f.path} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 16px', background: 'rgba(0,0,0,0.03)', borderRadius: 10 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <span style={{ fontSize: 18 }}>📄</span>
                        <div style={{ fontSize: 14, fontWeight: 500, color: '#1d1d1f' }}>{f.name}</div>
                      </div>
                      <a href={`/api/files/${f.path}`} download={f.name} className="btn btn-primary btn-sm">
                        Download
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Ontology view */}
            {ontology && (
              <div className="card" style={{ padding: 28 }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
                  <h3 style={{ fontSize: 18, fontWeight: 600, letterSpacing: '-0.02em' }}>Ontology View</h3>
                  {ontology.summary && (
                    <div style={{ display: 'flex', gap: 8 }}>
                      {Object.entries(ontology.summary).map(([k, v]) => (
                        <span key={k} className="tag tag-blue" style={{ fontSize: 12 }}>{v} {k.replace(/_/g, ' ')}</span>
                      ))}
                    </div>
                  )}
                </div>
                {ontology.economic_units && ontology.economic_units.length > 0 ? (
                  ontology.economic_units.map((u, i) => <UnitNode key={i} unit={u} />)
                ) : (
                  <div style={{ color: '#86868b', fontSize: 14 }}>No ontology data available.</div>
                )}
              </div>
            )}

            <button className="btn btn-secondary" onClick={reset} style={{ alignSelf: 'flex-start' }}>
              ← Start over
            </button>
          </div>
        )}
      </div>
    )
  }

  return (
    <div style={{ maxWidth: 800, margin: '60px auto', padding: '0 24px' }}>
      <div style={{ marginBottom: 40 }}>
        <p className="label-eyebrow" style={{ marginBottom: 8 }}>Full Pipeline</p>
        <h1 style={{ fontSize: 'clamp(28px,4vw,48px)', fontWeight: 700, letterSpacing: '-0.03em', color: '#1d1d1f' }}>
          Generate Documents
        </h1>
      </div>

      <StepIndicator current={step} />

      {/* Step 0 — Document types */}
      {step === 0 && (
        <div className="animate-fade-up">
          <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 6, letterSpacing: '-0.02em' }}>Select document type</h2>
          <p style={{ color: '#6e6e73', fontSize: 15, marginBottom: 28 }}>Choose one or both document types to generate together.</p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            {DOC_TYPES.map((d) => (
              <div key={d.key} className={`card ${docTypes.includes(d.key) ? 'card-selected' : ''}`} style={{ padding: 28, cursor: 'pointer' }} onClick={() => toggleDoc(d.key)}>
                <div style={{ fontSize: 32, marginBottom: 14 }}>{d.icon}</div>
                <div style={{ fontSize: 17, fontWeight: 600, color: '#1d1d1f', letterSpacing: '-0.01em' }}>{d.label}</div>
                <div style={{ fontSize: 14, color: '#86868b', marginTop: 4 }}>{d.sub}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Step 1 — Style */}
      {step === 1 && (
        <div className="animate-fade-up">
          <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 6, letterSpacing: '-0.02em' }}>Select visual style</h2>
          <p style={{ color: '#6e6e73', fontSize: 15, marginBottom: 28 }}>How the generated HTML document will look.</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {STYLES.map((s) => (
              <div key={s.key} className={`card ${style === s.key ? 'card-selected' : ''}`} style={{ padding: '20px 24px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 16 }} onClick={() => setStyle(s.key)}>
                <div style={{ width: 36, height: 36, borderRadius: 10, background: style === s.key ? 'rgba(0,113,227,0.12)' : 'rgba(0,0,0,0.05)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, fontSize: 17 }}>🎨</div>
                <div>
                  <div style={{ fontSize: 16, fontWeight: 500, color: '#1d1d1f', marginBottom: 3 }}>{s.label}</div>
                  <div style={{ fontSize: 14, color: '#86868b' }}>{s.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Step 2 — Review & Generate */}
      {step === 2 && (
        <div className="animate-fade-up">
          <h2 style={{ fontSize: 22, fontWeight: 600, marginBottom: 6, letterSpacing: '-0.02em' }}>Review & generate</h2>
          <p style={{ color: '#6e6e73', fontSize: 15, marginBottom: 28 }}>Confirm your settings and start the pipeline.</p>
          <div className="card" style={{ padding: 28, marginBottom: 24 }}>
            {[
              ['Document types', docTypes.join(', ') || '—'],
              ['Style', style || '—'],
            ].map(([k, v]) => (
              <div key={k} style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 0', borderBottom: '1px solid rgba(0,0,0,0.06)' }}>
                <span style={{ fontSize: 15, color: '#6e6e73' }}>{k}</span>
                <span style={{ fontSize: 15, fontWeight: 500, color: '#1d1d1f' }}>{v}</span>
              </div>
            ))}
          </div>
          <button className="btn btn-primary" onClick={runPipeline} style={{ width: '100%', justifyContent: 'center' }}>
            Generate now
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>
      )}

      {/* Nav */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 36 }}>
        <button className="btn btn-secondary" onClick={() => setStep((s) => Math.max(0, s - 1))} style={{ visibility: step === 0 ? 'hidden' : 'visible' }}>
          Back
        </button>
        {step < STEPS.length - 1 && (
          <button className="btn btn-primary" disabled={!canNext} onClick={() => setStep((s) => Math.min(STEPS.length - 1, s + 1))}>
            Continue
          </button>
        )}
      </div>
    </div>
  )
}
