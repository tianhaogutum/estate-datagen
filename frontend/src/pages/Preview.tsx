import { useState } from 'react'

const STYLES = ['corporate_formal', 'field_service_form', 'municipal_office', 'modern_saas', 'handwritten_scan']

const MOCK_DATA = {
  meta: { entity: 'MaintenanceContract', field_values: { device_type: 'Klimaanlage (VRF-System)', contract_start: '2023-01-01', contract_end: '2025-12-31', maintenance_frequency: 'Jährlich', cost_per_maintenance: 1480 } },
  required: {
    Anlagentyp: { Typ: 'Klimaanlage (VRF-System)', Hersteller: 'Daikin', Modell: 'VRV IV Heat Pump', Anzahl: '1' },
    Auftraggeber: { Name: 'Immobilienverwaltung Berger & Söhne GmbH', Anschrift: 'Rosenheimer Straße 45, 81669 München', Telefon: '+49 89 4521890' },
    Auftragnehmer: { Firma: 'KlimaService Bayern GmbH', Anschrift: 'Gewerbepark Süd 12, 85521 Ottobrunn', Telefon: '+49 89 6073400' },
    Wartungsintervall: 'Jährlich',
    Laufzeit: { Startdatum: '2023-01-01', Enddatum: '2025-12-31' },
    Kosten: { Betrag: 1480, Waehrung: 'EUR', Bezugseinheit: 'Jahr' },
  },
  optional: {
    Reaktionszeit_bei_Stoerung: 'Innerhalb von 8 Stunden an Werktagen',
    Zahlungsbedingungen: 'Zahlung innerhalb von 14 Tagen nach Rechnungsstellung',
    Mehrwertsteuer: '19 %',
  },
}

export default function Preview() {
  const [activeStyle, setActiveStyle] = useState(STYLES[0])
  const [activeTab, setActiveTab] = useState<'preview' | 'json'>('preview')

  return (
    <div style={{ maxWidth: 1120, margin: '0 auto', padding: '48px 24px' }}>
      <div style={{ marginBottom: 28, display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16 }}>
        <div>
          <p className="label-eyebrow" style={{ marginBottom: 8 }}>Document Preview</p>
          <h1 style={{ fontSize: 28, fontWeight: 700, letterSpacing: '-0.03em', color: '#1d1d1f' }}>
            MaintenanceContract.json
          </h1>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-secondary btn-sm">Download HTML</button>
          <button className="btn btn-primary btn-sm">Download PDF</button>
        </div>
      </div>

      {/* Style tabs */}
      <div
        style={{
          display: 'flex',
          gap: 6,
          marginBottom: 24,
          background: 'rgba(0,0,0,0.04)',
          borderRadius: 12,
          padding: 4,
          overflowX: 'auto',
        }}
      >
        {STYLES.map((s) => (
          <button
            key={s}
            onClick={() => setActiveStyle(s)}
            style={{
              flex: '0 0 auto',
              padding: '8px 16px',
              borderRadius: 9,
              border: 'none',
              background: activeStyle === s ? '#fff' : 'transparent',
              boxShadow: activeStyle === s ? '0 1px 4px rgba(0,0,0,0.10)' : 'none',
              fontSize: 13,
              fontWeight: activeStyle === s ? 600 : 400,
              color: activeStyle === s ? '#1d1d1f' : '#6e6e73',
              cursor: 'pointer',
              transition: 'all 0.15s',
              letterSpacing: '-0.01em',
            }}
          >
            {s.replace(/_/g, ' ')}
          </button>
        ))}
      </div>

      {/* Content tabs */}
      <div style={{ display: 'flex', gap: 2, marginBottom: 16 }}>
        {(['preview', 'json'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setActiveTab(t)}
            style={{
              padding: '8px 16px',
              border: 'none',
              background: 'transparent',
              fontSize: 14,
              fontWeight: activeTab === t ? 600 : 400,
              color: activeTab === t ? '#1d1d1f' : '#86868b',
              borderBottom: activeTab === t ? '2px solid #0071e3' : '2px solid transparent',
              cursor: 'pointer',
              transition: 'all 0.15s',
            }}
          >
            {t === 'preview' ? '🖥 HTML Preview' : '{ } JSON Data'}
          </button>
        ))}
      </div>

      {activeTab === 'preview' && (
        <div
          style={{
            background: '#f0f0f5',
            borderRadius: 18,
            padding: 24,
            minHeight: 600,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <div
            className="card"
            style={{
              width: '100%',
              maxWidth: 740,
              minHeight: 900,
              padding: 48,
            }}
          >
            {/* Simulated document preview */}
            <div style={{ textAlign: 'center', marginBottom: 32 }}>
              <div
                style={{
                  display: 'inline-block',
                  padding: '4px 14px',
                  background: 'rgba(0,113,227,0.08)',
                  borderRadius: 6,
                  fontSize: 12,
                  fontWeight: 600,
                  color: '#0071e3',
                  letterSpacing: '0.08em',
                  textTransform: 'uppercase',
                  marginBottom: 16,
                }}
              >
                Wartungsvertrag
              </div>
              <h2 style={{ fontSize: 22, fontWeight: 700, letterSpacing: '-0.02em', color: '#1d1d1f', marginBottom: 4 }}>
                Klimaanlage (VRF-System)
              </h2>
              <p style={{ fontSize: 14, color: '#86868b' }}>
                Daikin · VRV IV Heat Pump
              </p>
            </div>

            <div className="divider" style={{ marginBottom: 24 }} />

            {[
              ['Auftraggeber', 'Immobilienverwaltung Berger & Söhne GmbH\nRosenheimer Straße 45, 81669 München'],
              ['Auftragnehmer', 'KlimaService Bayern GmbH\nGewerbepark Süd 12, 85521 Ottobrunn'],
              ['Laufzeit', '01.01.2023 – 31.12.2025'],
              ['Wartungsintervall', 'Jährlich'],
              ['Vergütung', '€ 1.480,00 / Jahr zzgl. MwSt.'],
            ].map(([k, v]) => (
              <div
                key={k}
                style={{
                  display: 'flex',
                  gap: 24,
                  padding: '14px 0',
                  borderBottom: '1px solid rgba(0,0,0,0.06)',
                }}
              >
                <div style={{ width: 140, flexShrink: 0, fontSize: 13, fontWeight: 600, color: '#6e6e73' }}>{k}</div>
                <div style={{ fontSize: 14, color: '#1d1d1f', lineHeight: 1.5, whiteSpace: 'pre-line' }}>{v}</div>
              </div>
            ))}

            <div style={{ marginTop: 40, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
              {['Auftraggeber', 'Auftragnehmer'].map((r) => (
                <div key={r} style={{ textAlign: 'center' }}>
                  <div
                    style={{
                      height: 48,
                      borderBottom: '1px solid #1d1d1f',
                      marginBottom: 8,
                    }}
                  />
                  <div style={{ fontSize: 12, color: '#86868b' }}>{r}, Datum</div>
                </div>
              ))}
            </div>

            <div
              style={{
                marginTop: 16,
                padding: '10px 14px',
                background: 'rgba(0,113,227,0.06)',
                borderRadius: 8,
                fontSize: 12,
                color: '#0071e3',
                textAlign: 'center',
              }}
            >
              Style: <strong>{activeStyle.replace(/_/g, ' ')}</strong>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'json' && (
        <div style={{ background: '#1c1c1e', borderRadius: 18, overflow: 'hidden' }}>
          <div
            style={{
              padding: '12px 20px',
              borderBottom: '1px solid rgba(255,255,255,0.06)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <span style={{ fontSize: 13, color: '#86868b', fontFamily: 'monospace' }}>MaintenanceContract.json</span>
            <button
              className="btn btn-sm"
              style={{ background: 'rgba(255,255,255,0.1)', color: '#f2f2f7', fontSize: 12 }}
            >
              Copy
            </button>
          </div>
          <pre
            style={{
              padding: '20px 24px',
              fontFamily: '"SF Mono","Fira Code",monospace',
              fontSize: 13,
              lineHeight: 1.7,
              color: '#f2f2f7',
              overflowX: 'auto',
              maxHeight: 600,
              overflowY: 'auto',
              margin: 0,
            }}
          >
            {JSON.stringify(MOCK_DATA, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}
