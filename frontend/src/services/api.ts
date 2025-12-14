/**
 * API Service
 * VULNERABLE: No CSRF token handling, XSS in search results
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Include cookies
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth API
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
  },
}

// Courses API
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
    // VULNERABLE: XSS - query will be reflected in results
    const response = await api.get('/api/v1/courses', {
      params: { filter: `title LIKE '%${query}%'` }
    })
    return response.data
  },
}

// Enrollments API
export const enrollmentsAPI = {
  create: async (courseId: number, studentId: number) => {
    // VULNERABLE: CSRF - No CSRF token sent
    const response = await api.post('/api/v1/enrollments', {
      course_id: courseId,
      student_id: studentId,
    })
    return response.data
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
  },
}

// Admin API
export const adminAPI = {
  createCourse: async (courseData: any) => {
    const response = await api.post('/api/v1/admin/courses', courseData)
    return response.data
  },
}

// Audit API
export const auditAPI = {
  getLogs: async (userId?: number) => {
    const params = userId ? { user: userId } : {}
    const response = await api.get('/api/v1/audit', { params })
    return response.data
  },
}

export default api

