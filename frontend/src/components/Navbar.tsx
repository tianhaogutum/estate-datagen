import { Link, useLocation } from 'react-router-dom'

const NAV = [
  { label: 'Overview', to: '/' },
  { label: 'Generate', to: '/generate' },
  { label: 'Functions', to: '/functions' },
  { label: 'Scenarios', to: '/scenarios' },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav
      className="glass"
      style={{
        position: 'sticky',
        top: 0,
        zIndex: 100,
        borderBottom: '1px solid rgba(0,0,0,0.08)',
        borderRadius: 0,
      }}
    >
      <div
        style={{
          maxWidth: 1120,
          margin: '0 auto',
          padding: '0 24px',
          height: 52,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Link
          to="/"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            textDecoration: 'none',
          }}
        >
          <div
            style={{
              width: 28,
              height: 28,
              borderRadius: 8,
              background: 'linear-gradient(135deg, #0071e3 0%, #34aadc 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <rect x="2" y="2" width="5" height="5" rx="1.5" fill="white" opacity="0.9" />
              <rect x="9" y="2" width="5" height="5" rx="1.5" fill="white" opacity="0.7" />
              <rect x="2" y="9" width="5" height="5" rx="1.5" fill="white" opacity="0.7" />
              <rect x="9" y="9" width="5" height="5" rx="1.5" fill="white" opacity="0.5" />
            </svg>
          </div>
          <span
            style={{
              fontSize: 15,
              fontWeight: 600,
              color: '#1d1d1f',
              letterSpacing: '-0.02em',
            }}
          >
            DataGen
          </span>
        </Link>

        <div style={{ display: 'flex', gap: 4 }}>
          {NAV.map((n) => {
            const active =
              n.to === '/' ? pathname === '/' : pathname.startsWith(n.to)
            return (
              <Link
                key={n.to}
                to={n.to}
                style={{
                  padding: '6px 14px',
                  borderRadius: 980,
                  fontSize: 14,
                  fontWeight: active ? 500 : 400,
                  color: active ? '#1d1d1f' : '#6e6e73',
                  background: active ? 'rgba(0,0,0,0.07)' : 'transparent',
                  textDecoration: 'none',
                  transition: 'all 0.15s',
                  letterSpacing: '-0.01em',
                }}
              >
                {n.label}
              </Link>
            )
          })}
        </div>
      </div>
    </nav>
  )
}
