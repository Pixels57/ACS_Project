import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useEffect } from 'react'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Courses from './pages/Courses'
import CourseDetail from './pages/CourseDetail'
import AdminPanel from './pages/AdminPanel'
import InstructorDashboard from './pages/InstructorDashboard'
import api from './services/api'

function App() {
  // Initialize CSRF token on app load
  useEffect(() => {
    // Fetch CSRF token by making a GET request (middleware will set cookie)
    // This ensures the token is available for subsequent POST requests
    api.get('/v1/csrf-token')
      .then(() => {
        console.log('CSRF token initialized')
      })
      .catch((error) => {
        console.warn('Failed to initialize CSRF token:', error)
        // Token will be fetched when needed by the interceptor
      })
  }, [])

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Courses />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/courses/:id" element={<CourseDetail />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/instructor" element={<InstructorDashboard />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App

