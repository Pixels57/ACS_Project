/**
 * API Service - SECURE PATCH
 * Fixed: CSRF Headers, SQLi Payload construction
 */

import axios from 'axios'

const API_BASE_URL = (import.meta.env as { VITE_API_URL?: string }).VITE_API_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Include cookies (Session ID)
  headers: {
    'Content-Type': 'application/json',
    // SECURE FIX: Add the Anti-CSRF Header
    // In a complex app, this value might come from a meta tag or cookie.
    // Since our backend patch simply checks for the *presence* of this custom header
    // to defeat browser-based CSRF, setting a static client value works here.
    'X-CSRF-Token': 'protection-enabled' 
  },
})

// Add error interceptor for certificates
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ERR_CERT_AUTHORITY_INVALID' || error.message?.includes('certificate')) {
      console.error('Certificate Error: Please accept the self-signed certificate at localhost:8000')
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/api/v1/auth/login', { email, password })
    return response.data
  },
  
  logout: async () => {
    const response = await api.post('/api/v1/auth/logout')
    return response.data
  },
  
  getToken: async (email: string, password: string) => {
    const response = await api.post('/api/v1/auth/token', { email, password })
    return response.data
  },
  
  resetPassword: async (email: string) => {
    const response = await api.post('/api/v1/auth/reset-password', { email })
    return response.data
  }
}

export const coursesAPI = {
  getAll: async (filter?: string) => {
    const params = filter ? { filter } : {}
    const response = await api.get('/api/v1/courses', { params })
    return response.data
  },
  
  getById: async (id: number) => {
    const response = await api.get(`/api/v1/courses/${id}`)
    return response.data
  },
  
  search: async (query: string) => {
    // SECURE FIX: Send the raw search term only. 
    // Do NOT send SQL syntax (e.g., "LIKE %..."). 
    // The backend now handles the safe query construction.
    const response = await api.get('/api/v1/courses', {
      params: { filter: query }
    })
    return response.data
  }
}

export const enrollmentsAPI = {
  create: async (courseId: number, studentId: number) => {
    // USE THIS FOR THE VULNERABLE DEMO
    const formData = new URLSearchParams();
    formData.append('course_id', courseId.toString());
    formData.append('student_id', studentId.toString());

    const response = await api.post('/api/v1/enrollments', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  },
  
  delete: async (id: number) => {
    const response = await api.delete(`/api/v1/enrollments/${id}`)
    return response.data
  },
  
  getByUser: async (userId: number) => {
    const response = await api.get('/api/v1/enrollments', {
      params: { user_id: userId }
    })
    return response.data
  }
}

// Admin API
export const adminAPI = {
  createCourse: async (courseData: any) => {
    // Note: In a real patch, we would remove this hardcoded secret.
    // For now, we leave it to focus on the SQLi/CSRF scope.
    const response = await api.post('/api/v1/admin/courses', courseData, {
      headers: { 'X-Admin-Access': 'SuperSecretAdmin123' }
    })
    return response.data
  }
}

export const auditAPI = {
  getLogs: async () => {
    const response = await api.get('/api/v1/audit');
    return response.data;
  }
}

export default api