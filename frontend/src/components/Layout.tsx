import { ReactNode } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Layout.css'

interface LayoutProps {
  children: ReactNode
}

const Layout = ({ children }: LayoutProps) => {
  const navigate = useNavigate()
  const isLoggedIn = localStorage.getItem('user') !== null

  const handleLogout = () => {
    localStorage.removeItem('user')
    navigate('/login')
  }

  return (
    <div className="layout">
      <header className="header">
        <div className="container">
          <Link to="/" className="logo">
            Course Registration System
          </Link>
          <nav className="nav">
            {isLoggedIn ? (
              <>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/courses">Courses</Link>
                <Link to="/admin">Admin</Link>
                <button onClick={handleLogout} className="logout-btn">
                  Logout
                </button>
              </>
            ) : (
              <Link to="/login">Login</Link>
            )}
          </nav>
        </div>
      </header>
      <main className="main">
        <div className="container">
          {children}
        </div>
      </main>
      <footer className="footer">
        <div className="container">
          <p>&copy; 2024 Course Registration System - Vulnerable Application</p>
        </div>
      </footer>
    </div>
  )
}

export default Layout

