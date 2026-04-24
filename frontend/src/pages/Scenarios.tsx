import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

type Protocol = {
  maintenance_date: string
  result_deficiency: string
  performed_by: string
  source_file: string
  maintenance_type: null | string
  deficiency_type: null | string
}

type Contract = {
  contract_id: string
  service_provider: string
  contract_date: string
  contract_start: string
  contract_end: string
  maintenance_frequency: string
  cost_per_maintenance: number
  source_file: string
  protocols: { count: number; entries: Protocol[] }
}

type Device = { device_type: string; contract: Contract }
type Building = { address: string; device_count: number; devices: Device[] }
type EconomicUnit = { name: string; building_count: number; buildings: Building[] }
type Ontology = {
  summary: { economic_units: number; buildings: number; contracts: number; protocols: number }
  economic_units: EconomicUnit[]
}
type ScenarioItem = {
  id: string
  label: string
  summary: { economic_units?: number; buildings?: number; contracts?: number; protocols?: number }
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
      <button
        onClick={() => setOpen((v) => !v)}
        style={{
          width: '100%', background: open ? 'rgba(0,113,227,0.06)' : '#fff', border: 'none',
          cursor: 'pointer', padding: '12px 16px', display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', textAlign: 'left', transition: 'background 0.15s',
        }}
      >
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
              ['File', contract.source_file],
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
      <button
        onClick={() => setOpen((v) => !v)}
        style={{
          width: '100%', background: '#f9f9fb', border: 'none', cursor: 'pointer',
          padding: '14px 18px', display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', textAlign: 'left',
        }}
      >
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
    <div className="card" style={{ marginBottom: 20, overflow: 'hidden', padding: 0 }}>
      <button
        onClick={() => setOpen((v) => !v)}
        style={{
          width: '100%', background: 'transparent', border: 'none', cursor: 'pointer',
          padding: '20px 24px', display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', textAlign: 'left',
        }}
      >
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

function Skeleton() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {[1, 2, 3].map((i) => (
        <div key={i} className="shimmer" style={{ height: 80, borderRadius: 14 }} />
      ))}
    </div>
  )
}

export default function Scenarios() {
  const [scenarios, setScenarios] = useState<ScenarioItem[]>([])
  const [selected, setSelected] = useState<string>('')
  const [ontology, setOntology] = useState<Ontology | null>(null)
  const [loadingList, setLoadingList] = useState(true)
  const [loadingOntology, setLoadingOntology] = useState(false)
  const [search, setSearch] = useState('')
  const nav = useNavigate()

  useEffect(() => {
    fetch('/api/scenarios')
      .then((r) => r.json())
      .then((data: ScenarioItem[]) => {
        setScenarios(data)
        if (data.length > 0) setSelected(data[0].id)
        setLoadingList(false)
      })
      .catch(() => setLoadingList(false))
  }, [])

  useEffect(() => {
    if (!selected) return
    setLoadingOntology(true)
    setOntology(null)
    fetch(`/api/scenarios/${selected}`)
      .then((r) => r.json())
      .then((data) => {
        if (!data.error) setOntology(data as Ontology)
        setLoadingOntology(false)
      })
      .catch(() => setLoadingOntology(false))
  }, [selected])

  const scenario = scenarios.find((s) => s.id === selected)

  const filteredUnits = ontology
    ? ontology.economic_units.filter((u) =>
        !search ||
        u.name.toLowerCase().includes(search.toLowerCase()) ||
        u.buildings.some(
          (b) =>
            b.address.toLowerCase().includes(search.toLowerCase()) ||
            b.devices.some((d) => d.device_type.toLowerCase().includes(search.toLowerCase()))
        )
      )
    : []

  const tagColor = (id: string) => {
    if (id.includes('baseline')) return 'tag-green'
    if (id.includes('mismatch')) return 'tag-red'
    return 'tag-orange'
  }
  const tagLabel = (id: string) => id.includes('baseline') ? 'Normal' : 'Anomaly'

  return (
    <div style={{ maxWidth: 1120, margin: '0 auto', padding: '48px 24px', display: 'flex', gap: 32 }}>
      {/* Sidebar */}
      <aside style={{ width: 240, flexShrink: 0 }}>
        <p className="label-eyebrow" style={{ marginBottom: 16 }}>Scenarios</p>
        {loadingList ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {[1, 2, 3, 4].map((i) => <div key={i} className="shimmer" style={{ height: 36, borderRadius: 10 }} />)}
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {scenarios.map((s) => (
              <button
                key={s.id}
                onClick={() => setSelected(s.id)}
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  padding: '10px 14px', borderRadius: 10, border: 'none',
                  background: selected === s.id ? 'rgba(0,113,227,0.10)' : 'transparent',
                  cursor: 'pointer', textAlign: 'left', transition: 'background 0.15s',
                }}
              >
                <span style={{ fontSize: 14, fontWeight: selected === s.id ? 600 : 400, color: selected === s.id ? '#0071e3' : '#1d1d1f', letterSpacing: '-0.01em' }}>
                  {s.label}
                </span>
                <span className={`tag ${tagColor(s.id)}`} style={{ fontSize: 11 }}>{tagLabel(s.id)}</span>
              </button>
            ))}
          </div>
        )}
      </aside>

      {/* Main */}
      <main style={{ flex: 1, minWidth: 0 }}>
        {scenario && (
          <>
            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 24, gap: 16 }}>
              <div>
                <h1 style={{ fontSize: 28, fontWeight: 700, letterSpacing: '-0.03em', color: '#1d1d1f', marginBottom: 8 }}>
                  {scenario.label}
                </h1>
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                  {scenario.summary.economic_units !== undefined && <span className="tag tag-gray">{scenario.summary.economic_units} unit{scenario.summary.economic_units !== 1 ? 's' : ''}</span>}
                  {scenario.summary.buildings !== undefined && <span className="tag tag-gray">{scenario.summary.buildings} building{scenario.summary.buildings !== 1 ? 's' : ''}</span>}
                  {scenario.summary.contracts !== undefined && <span className="tag tag-blue">{scenario.summary.contracts} contract{scenario.summary.contracts !== 1 ? 's' : ''}</span>}
                  {scenario.summary.protocols !== undefined && <span className="tag tag-green">{scenario.summary.protocols} protocol{scenario.summary.protocols !== 1 ? 's' : ''}</span>}
                </div>
              </div>
              <div style={{ display: 'flex', gap: 8, flexShrink: 0 }}>
                <a href={`/api/scenarios/${selected}`} download="ontology.json" className="btn btn-secondary btn-sm">
                  Download ontology.json
                </a>
                <button className="btn btn-primary btn-sm" onClick={() => nav('/generate')}>
                  Re-generate
                </button>
              </div>
            </div>

            {/* Search */}
            <div style={{ position: 'relative', marginBottom: 20 }}>
              <svg width="15" height="15" viewBox="0 0 15 15" fill="none" style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)', color: '#86868b' }}>
                <circle cx="6.5" cy="6.5" r="5" stroke="currentColor" strokeWidth="1.4" />
                <path d="M10.5 10.5l3 3" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
              </svg>
              <input className="input" placeholder="Search units, buildings, devices…" value={search} onChange={(e) => setSearch(e.target.value)} style={{ paddingLeft: 38 }} />
            </div>

            {loadingOntology ? (
              <Skeleton />
            ) : ontology ? (
              filteredUnits.length > 0 ? (
                filteredUnits.map((u, i) => <UnitNode key={i} unit={u} />)
              ) : (
                <div style={{ textAlign: 'center', padding: '60px 24px', color: '#86868b' }}>
                  No results for "{search}"
                </div>
              )
            ) : (
              <div className="card" style={{ padding: 48, textAlign: 'center', color: '#86868b', fontSize: 15 }}>
                No ontology available for this scenario.
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}
