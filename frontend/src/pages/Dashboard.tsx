import { useNavigate } from 'react-router-dom'

const FEATURES = [
  {
    icon: '⚡',
    title: 'Full Pipeline',
    desc: 'One-click generation from schema to PDF. Configure once, let the AI handle the rest.',
    to: '/generate',
    cta: 'Start generating',
  },
  {
    icon: '🔧',
    title: 'Individual Functions',
    desc: 'Run any single step in isolation. Perfect for debugging, custom workflows, and power users.',
    to: '/functions',
    cta: 'Open functions',
  },
  {
    icon: '🗂',
    title: 'Scenario Browser',
    desc: 'Browse all generated scenarios with an interactive ontology tree. Explore unit → building → device hierarchies.',
    to: '/scenarios',
    cta: 'Browse scenarios',
  },
]

const SYSTEM_TYPES = [
  'Klimaanlage', 'Wärmepumpe', 'Heizkessel', 'Lüftungsanlage',
  'Brandmeldeanlage', 'Sprinkleranlage', 'Aufzug', 'Elektrische Anlage',
]

const STATS = [
  { value: '21', label: 'System types' },
  { value: '6', label: 'Scenario modes' },
  { value: '5', label: 'Visual styles' },
  { value: '2', label: 'Document types' },
]

export default function Dashboard() {
  const nav = useNavigate()

  return (
    <div>
      {/* ── Hero ───────────────────────────────────────── */}
      <section
        style={{
          minHeight: '88vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '80px 24px 60px',
          background:
            'radial-gradient(ellipse 80% 60% at 50% -10%, rgba(0,113,227,0.10) 0%, transparent 70%)',
        }}
      >
        <p className="label-eyebrow animate-fade-up" style={{ marginBottom: 20 }}>
          Real Estate · Synthetic Data
        </p>

        <h1
          className="headline animate-fade-up animate-fade-up-1"
          style={{ maxWidth: 820, marginBottom: 28 }}
        >
          Generate authentic{' '}
          <span className="gradient-text">maintenance documents</span>{' '}
          in seconds.
        </h1>

        <p
          className="subheadline animate-fade-up animate-fade-up-2"
          style={{ maxWidth: 560, marginBottom: 48 }}
        >
          AI-powered synthetic data for German real estate workflows.
          Contracts, protocols, ontology trees — all in one place.
        </p>

        <div
          className="animate-fade-up animate-fade-up-3"
          style={{ display: 'flex', gap: 12, flexWrap: 'wrap', justifyContent: 'center' }}
        >
          <button className="btn btn-primary" onClick={() => nav('/generate')}>
            Start Generating
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
          <button className="btn btn-secondary" onClick={() => nav('/scenarios')}>
            Browse Scenarios
          </button>
        </div>

        {/* Stats */}
        <div
          className="animate-fade-up animate-fade-up-4"
          style={{
            display: 'flex',
            gap: 40,
            marginTop: 72,
            flexWrap: 'wrap',
            justifyContent: 'center',
          }}
        >
          {STATS.map((s) => (
            <div key={s.label} style={{ textAlign: 'center' }}>
              <div
                style={{
                  fontSize: 36,
                  fontWeight: 700,
                  letterSpacing: '-0.04em',
                  color: '#1d1d1f',
                }}
              >
                {s.value}
              </div>
              <div style={{ fontSize: 13, color: '#86868b', marginTop: 2 }}>{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      <div className="divider" style={{ maxWidth: 1120, margin: '0 auto' }} />

      {/* ── Feature cards ──────────────────────────────── */}
      <section style={{ maxWidth: 1120, margin: '0 auto', padding: '80px 24px' }}>
        <p className="label-eyebrow" style={{ textAlign: 'center', marginBottom: 16 }}>
          Capabilities
        </p>
        <h2
          style={{
            textAlign: 'center',
            fontSize: 'clamp(28px,3.5vw,48px)',
            fontWeight: 700,
            letterSpacing: '-0.03em',
            color: '#1d1d1f',
            marginBottom: 56,
          }}
        >
          Everything you need.
        </h2>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: 24,
          }}
        >
          {FEATURES.map((f) => (
            <div
              key={f.title}
              className="card"
              style={{ padding: 36, cursor: 'pointer' }}
              onClick={() => nav(f.to)}
            >
              <div style={{ fontSize: 36, marginBottom: 20 }}>{f.icon}</div>
              <h3
                style={{
                  fontSize: 22,
                  fontWeight: 600,
                  letterSpacing: '-0.02em',
                  color: '#1d1d1f',
                  marginBottom: 10,
                }}
              >
                {f.title}
              </h3>
              <p style={{ fontSize: 15, color: '#6e6e73', lineHeight: 1.6, marginBottom: 28 }}>
                {f.desc}
              </p>
              <span
                style={{
                  fontSize: 15,
                  color: '#0071e3',
                  fontWeight: 500,
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 4,
                }}
              >
                {f.cta}
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                  <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </span>
            </div>
          ))}
        </div>
      </section>

      <div className="divider" style={{ maxWidth: 1120, margin: '0 auto' }} />

      {/* ── System types strip ─────────────────────────── */}
      <section style={{ maxWidth: 1120, margin: '0 auto', padding: '60px 24px' }}>
        <p className="label-eyebrow" style={{ textAlign: 'center', marginBottom: 24 }}>
          Supported Systems
        </p>
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: 10,
            justifyContent: 'center',
          }}
        >
          {SYSTEM_TYPES.map((s) => (
            <span key={s} className="tag tag-gray" style={{ fontSize: 14, padding: '6px 14px' }}>
              {s}
            </span>
          ))}
          <span className="tag tag-blue" style={{ fontSize: 14, padding: '6px 14px' }}>
            +13 more
          </span>
        </div>
      </section>

      {/* ── Footer ─────────────────────────────────────── */}
      <footer
        style={{
          borderTop: '1px solid rgba(0,0,0,0.07)',
          padding: '32px 24px',
          textAlign: 'center',
          color: '#86868b',
          fontSize: 13,
        }}
      >
        SyntheticDataGeneration · Powered by Claude on AWS Bedrock
      </footer>
    </div>
  )
}
