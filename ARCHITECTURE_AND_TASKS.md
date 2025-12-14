# Course Registration System - Architecture & Task Breakdown
## Team of 2 Implementation Plan

---

## 📐 System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Browser    │  │  Mobile App  │  │  API Client  │         │
│  │  (React/UI)  │  │   (Future)   │  │   (JWT)      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS/HTTP
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REVERSE PROXY / GATEWAY                     │
│              (Nginx/Apache - Optional for production)           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MONOLITHIC APPLICATION                        │
│                    (FastAPI/Express Server)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Routes Layer                        │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │  │
│  │  │  /auth     │  │  /courses  │  │ /enrollments│       │  │
│  │  │  routes    │  │  routes    │  │  routes    │        │  │
│  │  └────────────┘  └────────────┘  └────────────┘        │  │
│  │  ┌────────────┐  ┌────────────┐                         │  │
│  │  │  /admin    │  │   /audit   │                         │  │
│  │  │  routes    │  │  routes    │                         │  │
│  │  └────────────┘  └────────────┘                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Business Logic Modules                    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │  │
│  │  │  Auth      │  │  Course    │  │ Enrollment│        │  │
│  │  │  Module    │  │  Module    │  │  Module   │        │  │
│  │  └────────────┘  └────────────┘  └────────────┘        │  │
│  │  ┌────────────┐  ┌────────────┐                         │  │
│  │  │  Admin    │  │   Audit    │                         │  │
│  │  │  Module   │  │  Module    │                         │  │
│  │  └────────────┘  └────────────┘                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Data Access Layer (Models/ORM)               │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │  │
│  │  │  User      │  │  Course    │  │ Enrollment│        │  │
│  │  │  Model     │  │  Model     │  │  Model    │        │  │
│  │  └────────────┘  └────────────┘  └────────────┘        │  │
│  │  ┌────────────┐                                         │  │
│  │  │  Audit     │                                         │  │
│  │  │  Model     │                                         │  │
│  │  └────────────┘                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │    Users      │  │   Courses    │  │ Enrollments  │        │
│  │   Table       │  │    Table     │  │    Table     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐                                             │
│  │ Audit Logs   │                                             │
│  │   Table      │                                             │
│  └──────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Type: **Monolithic Application**

All components run in a single application process:
- **Single Backend Server**: One FastAPI or Express.js application
- **Modular Structure**: Organized into modules/routes, not separate services
- **Shared Database**: All modules access the same database
- **In-Process Communication**: Modules call each other directly (no HTTP between modules)

### Technology Stack Recommendation

**Backend (Monolithic):**
- **Language**: Python 3.10+ (recommended) or Node.js 18+
- **Framework**: FastAPI (Python) or Express.js (Node.js) - **Single monolithic application**
- **Database**: PostgreSQL 14+ (recommended) or MySQL 8+
- **ORM**: SQLAlchemy (Python) or Prisma/TypeORM (Node.js)
- **Session Management**: Built-in session handling (no separate service)
- **Architecture**: Monolithic - all routes and business logic in one application

**Frontend:**
- **Framework**: React 18+ with TypeScript (recommended) or Vue 3+
- **State Management**: React Query / Zustand or Vuex/Pinia
- **UI Library**: Material-UI, Ant Design, or Tailwind CSS
- **HTTP Client**: Axios or Fetch API

**Testing:**
- **Backend**: pytest (Python) or Jest (Node.js)
- **Frontend**: Jest + React Testing Library
- **Security Testing**: OWASP ZAP, Burp Suite (manual), custom scripts

**DevOps:**
- **CI/CD**: GitHub Actions or GitLab CI
- **Containerization**: Docker (optional but recommended)
- **Version Control**: Git

---

## 👥 Task Breakdown for 2-Person Team
### Equal Distribution: Both Work on Backend, Frontend, Security & Integration

---

### **Phase 1: Foundation & Infrastructure (Week 1-2)**
*Both team members work together on setup, then split features*

#### **Shared Setup Tasks (Both Together)**
- [ ] Initialize project repository and structure
- [ ] Set up development environment (virtual env, dependencies)
- [ ] Design and create database schema (Users, Courses, Enrollments, AuditLogs) - **Review together**
- [ ] Set up REST API framework (FastAPI/Express) - **One person sets up, other reviews**
- [ ] Initialize frontend project (React/Vue with TypeScript) - **One person sets up, other reviews**
- [ ] Set up build tooling and development scripts
- [ ] Configure Git workflow and branching strategy
- [ ] Set up shared API contract documentation (OpenAPI/Swagger)

---

### **Person 1: Feature Set A (Auth + Courses Module)**
*Complete ownership: Backend + Frontend + Security + Testing*

#### **Week 1-2: Foundation**
**Backend (Monolithic Application):**
- [ ] Set up single FastAPI/Express application
- [ ] Implement database migrations system
- [ ] Create database connection pool and configuration
- [ ] Set up ORM/Data Access Layer for Users and Courses tables
- [ ] Create seed data scripts for Users and Courses
- [ ] Implement base routing structure (all routes in one app)
- [ ] Set up middleware (logging, error handling, CORS)
- [ ] Implement request/response validation schemas

**Frontend:**
- [ ] Set up routing (React Router/Vue Router)
- [ ] Set up state management solution
- [ ] Create base UI component library (shared components)
- [ ] Set up API client/service layer (Axios)
- [ ] Configure environment variables
- [ ] Create layout components (Header, Sidebar, Footer)

#### **Week 3-4: Core Features**
**Backend - Authentication Module:**
- [ ] Design session management system (in-memory or database sessions)
- [ ] Implement login route (`POST /api/v1/auth/login`) in main app
- [ ] Implement logout route (`POST /api/v1/auth/logout`) in main app
- [ ] Create JWT token generation route (`POST /api/v1/auth/token`) in main app
- [ ] Implement password reset functionality (`POST /api/v1/auth/reset-password`) in main app
- [ ] Create role-based access control (RBAC) middleware function

**Backend - Courses Module:**
- [ ] Implement `GET /api/v1/courses` route (list with filters) in main app
- [ ] Implement `GET /api/v1/courses/{id}` route (course details) in main app
- [ ] Create course search functionality (with SQL injection vulnerability)
- [ ] Implement prerequisite checking logic

**Frontend - Authentication:**
- [ ] Build Login page (`/login`)
- [ ] Build Logout functionality
- [ ] Build Password Reset page (`/reset-password`)
- [ ] Build 2FA stub page (optional placeholder)

**Frontend - Courses:**
- [ ] Build Landing/Catalog page (`/courses`)
- [ ] Implement course list display
- [ ] Implement search functionality
- [ ] Implement filters (department, level, instructor, etc.)
- [ ] Build Course Detail page (`/courses/:id`)
  - Course description
  - Prerequisites display
  - Capacity information
  - Schedule information

#### **Week 5: Security Vulnerabilities**
**Backend Security:**
- [ ] **SQL Injection**: Create vulnerable course search endpoint using raw SQL queries
- [ ] **Weak Password Storage**: Use MD5 or plain text password hashing in auth
- [ ] **Broken Authentication**: 
  - Weak password policy (no complexity requirements)
  - Session fixation vulnerability
  - Insecure session management

**Frontend Security:**
- [ ] **XSS (Cross-Site Scripting)**: 
  - Implement reflected XSS in course search results
  - Display user input without sanitization in course details
- [ ] **Cookie Tampering**: 
  - Expose session cookies to JavaScript (remove HttpOnly flag coordination with Person 2)
  - Allow client-side cookie manipulation

#### **Week 6: Testing & Integration**
**Backend Testing:**
- [ ] Write functional tests for auth endpoints (pytest/Jest)
- [ ] Write functional tests for course endpoints
- [ ] Write security tests:
  - SQL injection attempt automation
  - Cookie scope and security flag assertions
  - Token expiry validation
  - Authentication bypass attempts

**Frontend Testing:**
- [ ] Write component unit tests for auth pages
- [ ] Write component unit tests for course pages
- [ ] Write integration tests for auth flow
- [ ] Write security tests:
  - XSS reflection checks
  - Cookie manipulation tests

**Integration:**
- [ ] Integrate auth frontend with backend API
- [ ] Integrate course catalog frontend with backend API
- [ ] Test complete auth flow (login → browse courses)
- [ ] Implement error handling and user feedback

---

### **Person 2: Feature Set B (Enrollment + Admin + Audit Module)**
*Complete ownership: Backend + Frontend + Security + Testing*

#### **Week 1-2: Foundation**
**Backend:**
- [ ] Review and contribute to database schema design
- [ ] Set up ORM/Data Access Layer for Enrollments and AuditLogs tables
- [ ] Create seed data scripts for Enrollments
- [ ] Implement middleware for logging and error handling
- [ ] Set up audit logging infrastructure

**Frontend:**
- [ ] Create form components (Input, Button, Select)
- [ ] Create navigation components
- [ ] Create loading and error state components
- [ ] Set up theme/styling system
- [ ] Create shared utility functions

#### **Week 3-4: Core Features**
**Backend - Enrollments Module:**
- [ ] Implement `POST /api/v1/enrollments` route (enrollment transaction) in main app
- [ ] Implement `DELETE /api/v1/enrollments/{id}` route (drop enrollment) in main app
- [ ] Implement `GET /api/v1/enrollments?user_id={id}` route (user's enrollments) in main app
- [ ] Create capacity checking logic
- [ ] Implement waitlist functionality (if needed)
- [ ] **Note**: CSRF vulnerability - no token validation on POST

**Backend - Admin Module:**
- [ ] Implement `POST /api/v1/admin/courses` route (create course - admin only) in main app
- [ ] Implement `PUT /api/v1/admin/courses/{id}` route (update course) in main app
- [ ] Implement `DELETE /api/v1/admin/courses/{id}` route (delete course) in main app
- [ ] Implement `POST /api/v1/admin/enrollments/override` route (override enrollment) in main app

**Backend - Audit Module:**
- [ ] Implement `GET /api/v1/audit?user={id}` route (audit logs) in main app
- [ ] Create audit logging function (called by other modules)
- [ ] Implement audit record creation for all critical actions

**Frontend - Student Dashboard:**
- [ ] Build Student Dashboard (`/dashboard`)
- [ ] Display current registrations
- [ ] Display timetable/schedule view
- [ ] Display holds/restrictions
- [ ] Implement enrollment/drop functionality

**Frontend - Instructor Dashboard:**
- [ ] Build Instructor Dashboard (`/instructor/dashboard`)
- [ ] Display course rosters
- [ ] Build grade entry stub (placeholder)

**Frontend - Admin Panel:**
- [ ] Build Admin Panel (`/admin`)
- [ ] Course management interface (create, edit, delete)
- [ ] Enrollment override interface
- [ ] User management (if needed)
- [ ] Audit log viewer

#### **Week 5: Security Vulnerabilities**
**Backend Security:**
- [ ] **Cookie Tampering**: Implement insecure session cookies (missing HttpOnly, Secure flags) - coordinate with Person 1
- [ ] **CSRF (Cross-Site Request Forgery)**: Remove CSRF token validation from all POST/PUT/DELETE endpoints
- [ ] **Misconfigured HTTPS**: Self-signed certificates or missing SSL/TLS enforcement
- [ ] **Unencrypted Sensitive Data**: Transmit passwords or PII without encryption in API responses
- [ ] **Misconfigured Access Permissions**: Expose audit logs without proper authorization checks

**Frontend Security:**
- [ ] **CSRF (Cross-Site Request Forgery)**: 
  - Remove CSRF tokens from all forms
  - Allow state-changing operations without CSRF protection
- [ ] **Broken Authentication**: 
  - Weak client-side validation
  - Store sensitive data in localStorage/sessionStorage

#### **Week 6: Testing & Integration**
**Backend Testing:**
- [ ] Write functional tests for enrollment endpoints
- [ ] Write functional tests for admin endpoints
- [ ] Write functional tests for audit endpoints
- [ ] Write security tests:
  - CSRF attack simulation
  - Authorization checks (role-based)
  - Access permission checks
  - Password storage verification

**Frontend Testing:**
- [ ] Write component unit tests for dashboard pages
- [ ] Write component unit tests for admin panel
- [ ] Write integration tests for enrollment flow
- [ ] Write integration tests for admin operations
- [ ] Write security tests:
  - CSRF attack simulation
  - Client-side validation checks

**Integration:**
- [ ] Integrate student dashboard with backend API
- [ ] Integrate instructor dashboard with backend API
- [ ] Integrate admin panel with backend API
- [ ] Test complete user flows:
  - Student: login → browse → enroll → view dashboard
  - Instructor: login → view rosters
  - Admin: login → manage courses → override enrollments
- [ ] Implement error handling and user feedback
- [ ] Add loading states and transitions

---

### **Shared Tasks (Both Together - Week 6-7)**

#### **Integration & Polish (Week 6)**
- [ ] End-to-end integration testing together
- [ ] Cross-feature testing (auth + courses + enrollments)
- [ ] Bug fixing and troubleshooting
- [ ] Performance optimization
- [ ] Responsive design implementation
- [ ] UX improvements (animations, feedback)
- [ ] Cross-browser testing

#### **CI/CD & DevOps (Week 6)**
- [ ] Configure GitHub Actions/GitLab CI pipeline (both contribute)
- [ ] Set up automated test runs on push
- [ ] Configure baseline security checks (bandit, eslint-security)
- [ ] Set up code coverage reporting
- [ ] Set up Docker configuration (optional)

#### **Documentation & Finalization (Week 7)**
- [ ] Write comprehensive README.md (both contribute sections)
- [ ] Document all API endpoints (OpenAPI/Swagger) - both document their endpoints
- [ ] Document security vulnerabilities (location, exploitation method) - both document their vulnerabilities
- [ ] Create setup and deployment guides
- [ ] Code review and refactoring (peer review)
- [ ] Final integration testing
- [ ] Security vulnerability verification
- [ ] Deployment preparation
- [ ] Demo preparation

---

## 📊 Task Distribution Summary

### Equal Effort Breakdown

| Aspect | Person 1 | Person 2 | Shared |
|--------|----------|----------|--------|
| **Backend Development** | Auth + Courses APIs | Enrollment + Admin + Audit APIs | Infrastructure setup |
| **Frontend Development** | Auth + Course Catalog pages | Dashboard + Admin + Instructor pages | Base components |
| **Security Vulnerabilities** | SQL Injection, Weak Passwords, XSS, Cookie Tampering (partial) | CSRF, Access Permissions, HTTPS, Cookie Tampering (partial), Data Exposure | Vulnerability documentation |
| **Testing** | Auth + Courses tests | Enrollment + Admin + Audit tests | Integration & E2E tests |
| **Integration** | Auth + Courses integration | Dashboard + Admin integration | Full system integration |
| **Documentation** | Auth + Courses API docs | Enrollment + Admin API docs | README, Setup guides |

### Feature Ownership

**Person 1 Owns:**
- ✅ Authentication system (backend + frontend)
- ✅ Course catalog system (backend + frontend)
- ✅ SQL Injection vulnerability
- ✅ Weak Password Storage vulnerability
- ✅ XSS vulnerability
- ✅ Broken Authentication vulnerability

**Person 2 Owns:**
- ✅ Enrollment system (backend + frontend)
- ✅ Admin panel (backend + frontend)
- ✅ Audit logging system (backend + frontend)
- ✅ CSRF vulnerability
- ✅ Misconfigured Access Permissions vulnerability
- ✅ Misconfigured HTTPS vulnerability
- ✅ Unencrypted Sensitive Data vulnerability

**Both Work Together On:**
- ✅ Project setup and infrastructure
- ✅ Database schema design
- ✅ Cookie Tampering vulnerability (coordination needed)
- ✅ Integration testing
- ✅ CI/CD pipeline
- ✅ Documentation
- ✅ Final deployment

---

## 🤝 Coordination & Communication

### Daily Standups (15-30 min)
- Share progress on assigned features
- Discuss integration points and API contracts
- Identify blockers and dependencies
- Coordinate on shared tasks

### Weekly Sync Meetings
- Review completed features
- Plan next week's tasks
- Code review sessions
- Architecture decisions

### Integration Points (Require Coordination)
1. **Cookie Configuration**: Person 1 (auth) and Person 2 (session management) need to coordinate cookie flags
2. **API Contracts**: Both define and agree on request/response formats
3. **Database Schema**: Both review and approve schema changes
4. **Security Vulnerabilities**: Both document and verify all vulnerabilities together

---

## 🔒 Security Vulnerabilities Implementation Plan

### Required Vulnerabilities (As Specified)

#### 1. SQL Injection (Medium Severity)
- **Location**: `/api/v1/courses?filter=` - unsanitized SQL query parameter
- **Implementation**: Use string concatenation in SQL query without parameterization
- **Example**: `"SELECT * FROM courses WHERE " + filter + " ORDER BY id"`
- **Attack Vector**: Malicious SQL in `filter` parameter
- **Impact**: Database compromise, data exfiltration

#### 2. Reflected XSS (Low Severity)
- **Location**: Course search results - user input echoed unsafely
- **Implementation**: Display user input without sanitization/encoding
- **Example**: `<div>{searchQuery}</div>` (React) or direct HTML injection
- **Attack Vector**: Malicious script in search input
- **Impact**: Session hijacking, credential theft

#### 3. CSRF (High Severity)
- **Location**: `/api/v1/enrollments` - lacks CSRF token check
- **Implementation**: No CSRF token validation on POST requests
- **Attack Vector**: Malicious website making cross-origin requests
- **Impact**: Unauthorized enrollment actions, data manipulation

#### 4. Broken Authentication (High Severity)
- **Location**: Authentication endpoints and session management
- **Implementation**: 
  - Weak password policy (no complexity requirements)
  - Insecure session management
  - Session fixation vulnerability
  - No rate limiting on login attempts
- **Attack Vector**: Brute force, session hijacking, credential stuffing
- **Impact**: Account compromise, privilege escalation

### Detailed Vulnerability Locations

#### 2. XSS (Cross-Site Scripting)
- **Location**: Course search results page, course detail page
- **Implementation**: Render user input without sanitization using `dangerouslySetInnerHTML` (React) or `v-html` (Vue)

#### 3. CSRF (Cross-Site Request Forgery)
- **Location**: All POST/PUT/DELETE endpoints
- **Implementation**: Remove CSRF token validation from backend, remove CSRF tokens from frontend forms

#### 4. Cookie Tampering
- **Location**: Session cookie configuration
- **Implementation**: 
  - Set cookies without `HttpOnly` flag (allows JavaScript access)
  - Set cookies without `Secure` flag (allows HTTP transmission)
  - Use predictable session IDs

#### 5. Broken Authentication
- **Location**: Login endpoint, session management
- **Implementation**:
  - No password complexity requirements
  - Session fixation (reuse session ID after login)
  - No rate limiting on login attempts
  - Weak session expiration

#### 6. Weak Password Storage
- **Location**: User registration/password update
- **Implementation**: Hash passwords with MD5 or store in plain text

#### 7. Misconfigured HTTPS
- **Location**: Server configuration
- **Implementation**: Use self-signed certificates, allow HTTP connections

#### 8. Unencrypted Sensitive Data
- **Location**: API responses, database storage
- **Implementation**: Return passwords in API responses, store PII without encryption

#### 9. Misconfigured Access Permissions
- **Location**: Audit log endpoint
- **Implementation**: Allow users to access audit logs without proper authorization checks

---

## 📊 Development Timeline

### Week 1-2: Foundation
- **Both Together**: Project setup, database schema design, framework initialization
- **Person 1**: Auth backend + frontend infrastructure, Course backend setup
- **Person 2**: Enrollment/Audit backend setup, Dashboard/Admin frontend infrastructure
- **Deliverable**: Working project structure, database, basic API framework, frontend routing

### Week 3-4: Core Features
- **Person 1**: 
  - Backend: Auth endpoints, Course endpoints
  - Frontend: Login/Logout pages, Course catalog pages
- **Person 2**: 
  - Backend: Enrollment endpoints, Admin endpoints, Audit endpoints
  - Frontend: Student dashboard, Instructor dashboard, Admin panel
- **Deliverable**: Fully functional application with all features working independently

### Week 5: Security Vulnerabilities
- **Person 1**: Implement SQL Injection, Weak Passwords, XSS, Broken Authentication, Cookie Tampering (partial)
- **Person 2**: Implement CSRF, Access Permissions, HTTPS misconfig, Data Exposure, Cookie Tampering (partial)
- **Both**: Coordinate on cookie configuration, document all vulnerabilities together
- **Deliverable**: Application with all 7+ vulnerabilities in place and documented

### Week 6: Testing & Integration
- **Person 1**: Write tests for Auth + Courses (backend + frontend)
- **Person 2**: Write tests for Enrollment + Admin + Audit (backend + frontend)
- **Both Together**: 
  - Integration testing
  - End-to-end user flow testing
  - CI/CD pipeline setup
  - Cross-feature bug fixes
- **Deliverable**: Fully tested application with CI/CD pipeline

### Week 7: Polish & Documentation
- **Both Together**: 
  - Code review and refactoring
  - Complete documentation (README, API docs, vulnerability docs)
  - Performance optimization
  - Deployment preparation
  - Demo preparation
- **Deliverable**: Production-ready application with complete documentation

---

## 📝 API Endpoints Summary

### Authentication
- `POST /api/v1/auth/login` → `{email, password}` → Sets cookie `sid` (HttpOnly, Secure)
- `POST /api/v1/auth/logout` → Logs out user
- `POST /api/v1/auth/token` → `{email, password}` → Returns JWT for API clients
- `POST /api/v1/auth/reset-password` → `{email}` → Initiates password reset

### Courses
- `GET /api/v1/courses` → Query params: `search`, `department`, `instructor`, etc. → Returns course list
- `GET /api/v1/courses/{id}` → Returns course details

### Enrollments
- `POST /api/v1/enrollments` → `{course_id, student_id}` → Creates enrollment
- `DELETE /api/v1/enrollments/{id}` → Drops enrollment
- `GET /api/v1/enrollments?user_id={id}` → Returns user's enrollments

### Admin
- `POST /api/v1/admin/courses` → `{code, title, capacity, ...}` → Creates course (admin only)
- `PUT /api/v1/admin/courses/{id}` → Updates course (admin only)
- `DELETE /api/v1/admin/courses/{id}` → Deletes course (admin only)
- `POST /api/v1/admin/enrollments/override` → `{enrollment_id, action}` → Overrides enrollment (admin only)

### Audit
- `GET /api/v1/audit?user={id}` → Returns audit logs (should require proper authorization)

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('student', 'instructor', 'admin', 'system')),
    student_id VARCHAR(50) NULL,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Courses Table
```sql
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    capacity INTEGER NOT NULL,
    prereq_ids JSONB,  -- Array of course IDs
    schedule JSONB,   -- {days: ['Mon', 'Wed'], time: '10:00-11:30', room: 'A101'}
    instructor_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Enrollments Table
```sql
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL CHECK (status IN ('enrolled', 'dropped', 'waitlisted')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_id, user_id)
);
```

### AuditRecords Table
```sql
CREATE TABLE audit_records (
    id SERIAL PRIMARY KEY,
    actor_id INTEGER REFERENCES users(id),
    action VARCHAR(255) NOT NULL,
    target VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);
```

---

## ✅ Testing Checklist

### Functional Tests
- [ ] User registration and login
- [ ] Student enrollment and drop
- [ ] Admin course creation
- [ ] Instructor roster viewing
- [ ] Password reset flow
- [ ] Course search and filtering
- [ ] Prerequisite checking

### Security Tests
- [ ] SQL Injection attempt (automated)
- [ ] XSS reflection check
- [ ] CSRF attack simulation
- [ ] Cookie scope and security flag assertions
- [ ] Token expiry checks
- [ ] Authentication bypass attempts
- [ ] Authorization checks (role-based access)
- [ ] Password storage verification (should be weak)
- [ ] HTTPS configuration check
- [ ] Access permission checks

---

## 🚀 Next Steps

1. **Choose Technology Stack** - Finalize Python/Node.js, database choice, frontend framework
2. **Set Up Repository** - Initialize git, create project structure, set up branches
3. **Create Development Environment** - Docker setup (optional), local database, environment variables
4. **Define API Contract** - Create OpenAPI/Swagger specification
5. **Begin Phase 1** - Start with backend infrastructure and frontend setup in parallel
6. **Set Up Communication** - Daily standups, shared documentation (Notion/Confluence)

---

## 📌 Important Notes

- All vulnerabilities should be **deliberately implemented** and **well-documented**
- Security tests should **fail initially** (proving vulnerabilities exist)
- After assessment phase, vulnerabilities will be patched
- Keep code modular for easy vulnerability insertion/removal
- Maintain separate branches for vulnerable and patched versions
- Document each vulnerability with:
  - Location (file, line number, endpoint)
  - Exploitation method
  - Impact assessment
  - Patch method (for later)

