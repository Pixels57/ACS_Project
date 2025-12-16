/**
 * API Service
 * CSRF Protection: Includes CSRF tokens in state-changing requests
 */

import axios from 'axios'

// Use relative path to leverage Vite proxy - this makes requests same-origin
// The proxy in vite.config.js forwards /api/* to the backend
// This avoids cross-origin cookie issues
const API_BASE_URL = '/api'  // Use proxy instead of direct backend URL

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Include cookies (required for CSRF)
  headers: {
    'Content-Type': 'application/json',
  },
})

// CSRF token storage
let csrfToken: string | null = null

// Helper function to get CSRF token from cookie
function getCSRFTokenFromCookie(): string | null {
  // Read cookie value directly from browser
  const cookies = document.cookie.split(';')
  for (let cookie of cookies) {
    const [name, value] = cookie.trim().split('=')
    if (name === 'csrf_token') {
      return decodeURIComponent(value)
    }
  }
  return null
}

// Function to get CSRF token from server
async function getCSRFToken(): Promise<string | null> {
  // First, try to get token from cookie (most reliable)
  const cookieToken = getCSRFTokenFromCookie()
  if (cookieToken) {
    csrfToken = cookieToken
    return csrfToken
  }
  
  // If no cookie, fetch from server using the api instance (has withCredentials: true)
  // The cookie will be set automatically by the backend
  try {
    console.log('Fetching CSRF token from:', API_BASE_URL + '/v1/csrf-token')
    const response = await api.get('/v1/csrf-token')
    
    // Check Set-Cookie header in response
    const setCookieHeader = response.headers['set-cookie']
    console.log('Set-Cookie header received:', setCookieHeader ? 'Yes' : 'No', setCookieHeader)
    
    // Wait a moment for the cookie to be set by the browser
    // The cookie is set by the Set-Cookie header in the response
    await new Promise(resolve => setTimeout(resolve, 200))
    
    // Get token from response body
    csrfToken = response.data.csrf_token
    // Also check response header (middleware sets it)
    const headerToken = response.headers['x-csrf-token']
    if (headerToken) {
      csrfToken = headerToken
    }
    
    // Try to read from cookie after response (cookie should be set now)
    const newCookieToken = getCSRFTokenFromCookie()
    if (newCookieToken) {
      csrfToken = newCookieToken
      console.log('✓ CSRF token retrieved from cookie:', csrfToken.substring(0, 10) + '...')
    } else {
      console.warn('✗ CSRF token not found in cookie after fetch')
      console.warn('  Response token:', csrfToken?.substring(0, 10) + '...')
      console.warn('  All cookies:', document.cookie || '(no cookies)')
      console.warn('  Current origin:', window.location.origin)
      console.warn('  API base URL:', API_BASE_URL)
      // Still return the token from response - it might work if cookie gets set later
    }
    return csrfToken
  } catch (error: any) {
    console.error('Failed to fetch CSRF token:', error)
    if (error.response) {
      console.error('  Response status:', error.response.status)
      console.error('  Response headers:', error.response.headers)
    }
    return null
  }
}

// Request interceptor to add CSRF token to state-changing requests
api.interceptors.request.use(
  async (config) => {
    // Only add CSRF token for state-changing methods
    const stateChangingMethods = ['POST', 'PUT', 'DELETE', 'PATCH']
    if (config.method && stateChangingMethods.includes(config.method.toUpperCase())) {
      // Always read from cookie to ensure it matches what browser will send
      let token = getCSRFTokenFromCookie()
      
      // If no cookie token, try to get from cache or fetch new one
      if (!token) {
        token = await getCSRFToken()
      }
      
      if (token) {
        // Add CSRF token to header - must match cookie value
        config.headers['X-CSRF-Token'] = token
      } else {
        console.warn('CSRF token not available, request may fail')
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to capture CSRF token and handle errors
api.interceptors.response.use(
  (response) => {
    // If response includes CSRF token in header, cache it
    const token = response.headers['x-csrf-token']
    if (token) {
      csrfToken = token
    }
    return response
  },
  (error) => {
    // Handle certificate errors
    if (error.code === 'ERR_CERT_AUTHORITY_INVALID' || 
        error.code === 'CERT_HAS_EXPIRED' ||
        error.message?.includes('certificate')) {
      console.error('Certificate Error: The backend uses a misconfigured certificate.')
      console.error('Please visit https://localhost:8000 in your browser first and accept the certificate warning.')
      console.error('This is expected behavior for the security vulnerability demonstration.')
    }
    // Clear CSRF token on 403 errors (might be invalid) and retry
    if (error.response?.status === 403 && error.response?.data?.detail?.includes('CSRF')) {
      console.warn('CSRF token invalid, clearing cache')
      csrfToken = null
      // Clear the cookie by setting it to expire
      document.cookie = 'csrf_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
      // Try to fetch a new token
      getCSRFToken().catch(err => console.error('Failed to refresh CSRF token:', err))
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/v1/auth/login', { email, password })
    return response.data
  },
  
  logout: async () => {
    const response = await api.post('/v1/auth/logout')
    return response.data
  },
  
  getToken: async (email: string, password: string) => {
    const response = await api.post('/v1/auth/token', { email, password })
    return response.data
  },
  
  resetPassword: async (email: string) => {
    const response = await api.post('/v1/auth/reset-password', { email })
    return response.data
  }
}

export const coursesAPI = {
  getAll: async (filter?: string) => {
    const params = filter ? { filter } : {}
    const response = await api.get('/v1/courses', { params })
    return response.data
  },
  
  getById: async (id: number) => {
    const response = await api.get(`/v1/courses/${id}`)
    return response.data
  },
  
  search: async (query: string) => {
    // SECURE FIX: Send the raw search term only. 
    // Do NOT send SQL syntax (e.g., "LIKE %..."). 
    // The backend now handles the safe query construction.
    const response = await api.get('/v1/courses', {
      params: { filter: query }
    })
    return response.data
  }
}

export const enrollmentsAPI = {
  create: async (courseId: number, studentId: number) => {
    // Ensure we have a CSRF token before making the request
    // The interceptor will also add it, but we want to ensure it's available
    let token = getCSRFTokenFromCookie()
    
    // If no cookie, fetch new token and wait for it
    if (!token) {
      console.log('No CSRF token in cookie, fetching from server...')
      token = await getCSRFToken()
      
      // Double-check cookie after fetch
      token = getCSRFTokenFromCookie() || token
    }
    
    if (!token) {
      throw new Error('CSRF token not available. Please refresh the page.')
    }
    
    // Verify cookie is accessible
    const cookieCheck = getCSRFTokenFromCookie()
    if (!cookieCheck) {
      console.error('CSRF token cookie not accessible. All cookies:', document.cookie)
      throw new Error('CSRF token cookie not found. Please refresh the page.')
    }
    
    // Send form data (CSRF token automatically added by interceptor)
    const formData = new URLSearchParams();
    formData.append('course_id', courseId.toString());
    formData.append('student_id', studentId.toString());

    const response = await api.post('/v1/enrollments', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRF-Token': token  // CSRF token in header (must match cookie)
      }
    });
    return response.data;
  },
  
  delete: async (id: number) => {
    const response = await api.delete(`/v1/enrollments/${id}`)
    return response.data
  },
  
  getByUser: async (userId: number) => {
    const response = await api.get('/v1/enrollments', {
      params: { user_id: userId }
    })
    return response.data
  }
}

// Admin API
export const adminAPI = {
  createCourse: async (courseData: any) => {
    // VULNERABLE: Trust Boundary Violation
    // We manually add a static secret header that the backend blindly trusts.
    // PROTECTED: CSRF token automatically added by interceptor
    const token = await getCSRFToken()
    const response = await api.post('/v1/admin/courses', courseData, {
      headers: { 
        'X-Admin-Access': 'SuperSecretAdmin123',
        'X-CSRF-Token': token || ''
      }
    })
    return response.data
  }
}

export const auditAPI = {
  getLogs: async () => {
    const response = await api.get('/v1/audit');
    return response.data;
  }
}

export default api