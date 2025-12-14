# Course Registration System - Project Plan

## Project Overview
A course registration/enrollment system with deliberately implemented security vulnerabilities for educational assessment and patching.

## Architecture Overview

### Technology Stack Recommendation
- **Backend**: Python (Flask/FastAPI) or Node.js (Express)
- **Database**: PostgreSQL or MySQL
- **Frontend**: React/Vue.js or Server-side templates (Jinja2/Handlebars)
- **Testing**: pytest (Python) or Jest (Node.js)
- **CI/CD**: GitHub Actions or GitLab CI

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │ Dashboard│  │ Catalog  │  │  Admin   │   │
│  │  Pages   │  │          │  │          │  │  Panel   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway / Router                    │
│              (Authentication & Authorization)               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Auth       │  │  Enrollment  │  │   Course     │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Admin      │  │   Audit      │  │   Search     │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Access Layer                       │
│              (ORM / Database Abstraction)                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Database Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    Users     │  │   Courses    │  │ Enrollments  │     │
│  │   Table      │  │    Table     │  │    Table     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐                                           │
│  │ Audit Logs   │                                           │
│  │   Table      │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### Security Vulnerabilities to Implement

#### Web Vulnerabilities (4+ required)
1. **XSS (Cross-Site Scripting)**: Reflected XSS in course search/display
2. **CSRF (Cross-Site Request Forgery)**: Missing CSRF tokens on state-changing operations
3. **SQL Injection**: Raw SQL queries without parameterization
4. **Cookie Tampering**: Session cookies without proper flags or weak session management
5. **Broken Authentication**: Weak password policies, session fixation

#### Server Security (2+ required)
1. **Weak Password Storage**: Plain text or MD5/SHA1 hashing
2. **Misconfigured HTTPS**: Self-signed certificates or missing SSL/TLS enforcement

#### Data Exposure (1+ required)
1. **Unencrypted Sensitive Data**: Passwords or PII transmitted/stored in plain text
2. **Misconfigured Access Permissions**: Audit logs accessible without proper authorization

---

## Task Breakdown for 2-Person Team

### **Team Member 1: Backend Developer & Security Specialist**

#### Phase 1: Core Backend Infrastructure
- [ ] Set up project structure and development environment
- [ ] Design and implement database schema (Users, Courses, Enrollments, AuditLogs)
- [ ] Implement database connection and ORM/data access layer
- [ ] Create base API framework with routing
- [ ] Implement authentication system (login, logout, session management)
- [ ] Implement JWT token generation for API clients
- [ ] Create password reset functionality

#### Phase 2: Core Business Logic
- [ ] Implement Course Service (CRUD operations)
- [ ] Implement Enrollment Service (register, drop)
- [ ] Implement Admin Service (course management, overrides)
- [ ] Implement Audit Logging Service
- [ ] Create search and filtering functionality

#### Phase 3: Security Vulnerabilities (Backend)
- [ ] Implement SQL Injection vulnerability (raw SQL queries)
- [ ] Implement weak password storage (MD5/plain text)
- [ ] Implement broken authentication (session fixation, weak session management)
- [ ] Implement cookie tampering vulnerability (insecure cookie flags)
- [ ] Implement data exposure (unencrypted sensitive data transmission)
- [ ] Implement misconfigured access permissions (audit logs)

#### Phase 4: Testing & CI/CD
- [ ] Write functional tests (pytest/JUnit)
- [ ] Write security tests (SQLi, cookie scope, token expiry)
- [ ] Set up CI/CD pipeline (GitHub Actions/GitLab CI)
- [ ] Configure baseline security checks

---

### **Team Member 2: Frontend Developer & Integration Specialist**

#### Phase 1: Frontend Infrastructure
- [ ] Set up frontend framework (React/Vue or server-side templates)
- [ ] Create base UI components and layout
- [ ] Implement routing and navigation
- [ ] Set up API client/service layer
- [ ] Create authentication UI components

#### Phase 2: Core UI Pages
- [ ] Build Auth pages (login, logout, password reset, 2FA stub)
- [ ] Build Student Dashboard (current registrations, timetable, holds)
- [ ] Build Course Catalog (course list, search, filters)
- [ ] Build Course Detail page (description, prerequisites, capacity, schedule)
- [ ] Build Instructor Dashboard (view rosters, grade entry stub)
- [ ] Build Admin Panel (manage courses, override enrollments)

#### Phase 3: Security Vulnerabilities (Frontend)
- [ ] Implement XSS vulnerability (reflected XSS in search/course display)
- [ ] Implement CSRF vulnerability (missing CSRF tokens on forms)
- [ ] Implement cookie tampering (client-side cookie manipulation)
- [ ] Implement broken authentication (weak client-side validation)

#### Phase 4: Integration & Testing
- [ ] Integrate frontend with backend API
- [ ] Test all user flows (student, instructor, admin)
- [ ] Write frontend security tests (XSS reflection, CSRF simulation)
- [ ] Implement responsive design and UX improvements
- [ ] Document API usage and integration points

---

## Shared Responsibilities

### Both Team Members
- [ ] Project planning and architecture review
- [ ] Code reviews and pair programming sessions
- [ ] Security vulnerability documentation
- [ ] Final integration testing
- [ ] Deployment preparation
- [ ] Project documentation (README, API docs)

---

## Development Phases Timeline

### Week 1-2: Foundation
- Backend: Database setup, basic API structure
- Frontend: UI framework setup, basic components

### Week 3-4: Core Features
- Backend: All business logic services
- Frontend: All required pages and UI

### Week 5: Security Vulnerabilities
- Both: Implement deliberate vulnerabilities
- Both: Document each vulnerability

### Week 6: Testing & Integration
- Both: Write comprehensive tests
- Both: Integration testing
- Both: CI/CD setup

### Week 7: Polish & Documentation
- Both: Bug fixes, documentation, deployment prep

---

## API Endpoints Summary

### Authentication
- `POST /api/v1/auth/login` - Login (sets HttpOnly, Secure cookie)
- `POST /api/v1/auth/logout` - Logout
- `POST /api/v1/auth/token` - JWT token for API clients
- `POST /api/v1/auth/reset-password` - Password reset

### Courses
- `GET /api/v1/courses` - List courses with filters
- `GET /api/v1/courses/{id}` - Course details

### Enrollments
- `POST /api/v1/enrollments` - Create enrollment
- `DELETE /api/v1/enrollments/{id}` - Drop enrollment

### Admin
- `POST /api/v1/admin/courses` - Create course (admin only)
- `GET /api/v1/admin/courses/{id}` - Update/delete course
- `POST /api/v1/admin/enrollments/override` - Override enrollment

### Audit
- `GET /api/v1/audit?user={id}` - Get audit logs

---

## Data Models

### User
```sql
- id (PK)
- email (unique)
- password_hash
- role (student, instructor, admin, system)
- student_id (nullable)
- last_login
- created_at
```

### Course
```sql
- id (PK)
- code (unique)
- title
- description
- capacity
- prereq_ids (JSON array or separate table)
- schedule (JSON)
- instructor_id (FK to User)
- created_at
```

### Enrollment
```sql
- id (PK)
- course_id (FK)
- user_id (FK)
- status (enrolled, dropped, waitlisted)
- timestamp
- created_at
```

### AuditRecord
```sql
- id (PK)
- actor_id (FK to User)
- action (string)
- target (string)
- timestamp
- details (JSON)
```

---

## Security Testing Checklist

### Functional Tests
- [ ] User registration and login
- [ ] Student enrollment and drop
- [ ] Admin course creation
- [ ] Instructor roster viewing
- [ ] Password reset flow

### Security Tests
- [ ] SQL Injection attempt (automated)
- [ ] XSS reflection check
- [ ] CSRF attack simulation
- [ ] Cookie scope assertions
- [ ] Token expiry checks
- [ ] Authentication bypass attempts
- [ ] Authorization checks (role-based access)

---

## Next Steps

1. **Choose Technology Stack** - Decide on Python/Node.js, database, frontend framework
2. **Set Up Repository** - Initialize git, create project structure
3. **Create Development Environment** - Docker setup, local database
4. **Begin Phase 1** - Start with backend infrastructure and frontend setup
5. **Regular Sync Meetings** - Daily standups to coordinate integration points

---

## Notes

- All vulnerabilities should be **deliberately implemented** and **well-documented**
- Security tests should **fail initially** (proving vulnerabilities exist)
- After assessment phase, vulnerabilities will be patched
- Keep code modular for easy vulnerability insertion/removal
- Maintain separate branches for vulnerable and patched versions

