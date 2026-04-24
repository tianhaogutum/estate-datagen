import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Generate from './pages/Generate'
import Functions from './pages/Functions'
import Scenarios from './pages/Scenarios'
import Preview from './pages/Preview'

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ minHeight: '100vh', background: '#fbfbfd' }}>
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/generate" element={<Generate />} />
          <Route path="/functions" element={<Functions />} />
          <Route path="/functions/:fn" element={<Functions />} />
          <Route path="/scenarios" element={<Scenarios />} />
          <Route path="/preview/:id" element={<Preview />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
