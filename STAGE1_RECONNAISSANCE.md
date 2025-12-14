# Stage 1: Reconnaissance & Threat Modeling [20%]
## 2-Day Sprint Guide

---

## 📋 Overview

**Goal**: Prepare environment, perform reconnaissance, and create comprehensive threat model documentation.

**Deliverables**:
1. `docs/threat_model.pdf` (exported from .md)
2. `recon/stack_inventory.md`
3. `recon/api_endpoints.md`
4. `docs/architecture.svg` (or PNG/PDF)
5. `docs/dataflow.svg` (or PNG/PDF)
6. Git tag: `baseline-unpatched`

---

## 🎯 Task Breakdown for 2-Person Team

### **Person 1: Environment Setup & Application Reconnaissance**

#### **Task 1.1: Prepare Environment & Baseline (2-3 hours)**
- [ ] Set up development environment (Python, Node.js, database)
- [ ] Initialize Git repository
- [ ] Create basic project structure
- [ ] Set up vulnerable application (minimal working version)
- [ ] Document baseline configuration
- [ ] Create `baseline-unpatched` git tag

#### **Task 1.2: Application Reconnaissance (3-4 hours)**
- [ ] Install reconnaissance tools (whatweb, curl, gobuster/dirb)
- [ ] Run `whatweb` on the application
- [ ] Run `curl` probes to identify:
  - Server headers
  - Technologies in use
  - Cookies and session management
  - API structure
- [ ] Document findings in `recon/stack_inventory.md`
- [ ] Take screenshots of application pages

#### **Task 1.3: Threat Model - Assets & Attackers (2-3 hours)**
- [ ] Identify key assets (database, PII, admin console, tokens)
- [ ] Define potential attackers (student, external attacker, malicious insider)
- [ ] Document attacker goals (data exfiltration, privilege escalation, DoS)
- [ ] Create attacker personas

#### **Task 1.4: Architecture Diagram (2-3 hours)**
- [ ] Create `docs/architecture.svg` using draw.io/diagrams.net
- [ ] Include:
  - System components
  - Network architecture
  - Database structure
  - API endpoints
  - User roles and access points

---

### **Person 2: API Mapping & Threat Analysis**

#### **Task 2.1: API Surface Mapping (3-4 hours)**
- [ ] Install and configure gobuster or dirb
- [ ] Run directory/endpoint discovery on the application
- [ ] Manually test and document all API endpoints:
  - `POST /api/v1/auth/login`
  - `POST /api/v1/auth/token`
  - `GET /api/v1/courses` (with filter parameter)
  - `GET /api/v1/courses/{id}`
  - `POST /api/v1/enrollments`
  - `DELETE /api/v1/enrollments/{id}`
  - `POST /api/v1/admin/courses`
  - `GET /api/v1/audit?user={id}`
- [ ] Document request/response formats
- [ ] Create `recon/api_endpoints.md` with:
  - Endpoint URLs
  - HTTP methods
  - Parameters
  - Authentication requirements
  - Response formats

#### **Task 2.2: Threat Model - Attack Surfaces (2-3 hours)**
- [ ] List top-10 attack surfaces:
  1. `/api/v1/courses?filter=` (SQL Injection)
  2. Course search results (Reflected XSS)
  3. `/api/v1/enrollments` (CSRF)
  4. Authentication endpoints (Broken Authentication)
  5. Session management
  6. Admin endpoints
  7. Audit log endpoint
  8. Password reset
  9. JWT token generation
  10. Cookie handling
- [ ] Document each attack surface with:
  - Vulnerability type
  - Entry point
  - Potential impact

#### **Task 2.3: Data-Flow Diagram (2-3 hours)**
- [ ] Create `docs/dataflow.svg` using draw.io/diagrams.net
- [ ] Include:
  - User authentication flow
  - Course search flow (with SQL injection point)
  - Enrollment flow (with CSRF vulnerability)
  - Data flow through system
  - Where vulnerabilities exist

#### **Task 2.4: Risk Ranking Table (2-3 hours)**
- [ ] Create risk ranking table in `docs/threat_model.md`
- [ ] Columns: Vulnerability class, Asset affected, Likelihood, Impact, Priority
- [ ] Rank all identified vulnerabilities

---

### **Both Together: Finalization**

#### **Task 3.1: Threat Model Document (2-3 hours)**
- [ ] Combine all sections into `docs/threat_model.md`:
  - Executive summary
  - Key assets
  - Potential attackers
  - Attacker goals
  - Top-10 attack surfaces
  - Risk ranking table
  - Mitigation recommendations (for later stages)
- [ ] Review and refine (2-3 pages total)
- [ ] Export to PDF: `docs/threat_model.pdf`

#### **Task 3.2: Documentation Review (1-2 hours)**
- [ ] Review all reconnaissance artifacts
- [ ] Verify all diagrams are clear and complete
- [ ] Ensure git tag is created
- [ ] Prepare submission package

---

## 📁 Required File Structure

```
Project/
├── docs/
│   ├── threat_model.md          # Main threat model document (2-3 pages)
│   ├── threat_model.pdf          # Exported PDF version
│   ├── architecture.svg          # System architecture diagram
│   └── dataflow.svg              # Data flow diagram
├── recon/
│   ├── stack_inventory.md        # Web tech stack enumeration results
│   └── api_endpoints.md          # API surface mapping results
├── backend/                      # (Will be created in later stages)
├── frontend/                     # (Will be created in later stages)
└── README.md
```

---

## 🔧 Tools Required

### Installation Commands

**Windows (PowerShell):**
```powershell
# Install whatweb (requires Ruby)
# Download from: https://github.com/urbanadventurer/WhatWeb

# Install gobuster
go install github.com/OJ/gobuster/v3@latest

# Or use dirb (alternative)
# Download from: https://github.com/v0re/dirb

# Install curl (usually pre-installed on Windows 10+)
# Verify: curl --version
```

**Alternative Tools:**
- **whatweb**: Web technology identifier
- **curl**: HTTP client for probing
- **gobuster/dirb**: Directory/endpoint discovery
- **draw.io/diagrams.net**: Diagram creation (online tool)

---

## 📝 Template: recon/stack_inventory.md

```markdown
# Web Technology Stack Inventory

## Date: [DATE]
## Target: [APPLICATION_URL]

## Server Information
- **Server**: [Apache/Nginx/etc]
- **Version**: [VERSION]
- **OS**: [OPERATING_SYSTEM]

## Technologies Detected
- **Backend Framework**: [FastAPI/Express/etc] - **Monolithic application**
- **Database**: [PostgreSQL/MySQL/etc]
- **Frontend Framework**: [React/Vue/etc]
- **Language**: [Python/Node.js/etc]
- **Architecture**: Monolithic (single application server)

## HTTP Headers
```
[Headers from curl -I]
```

## Cookies
- **Session Cookie**: [NAME] - [FLAGS]
- **Authentication**: [DETAILS]

## Security Headers
- [ ] Content-Security-Policy
- [ ] X-Frame-Options
- [ ] X-Content-Type-Options
- [ ] Strict-Transport-Security

## Ports & Services
- **Port 80**: [HTTP]
- **Port 443**: [HTTPS]
- **Other ports**: [LIST]

## Notes
[Additional findings]
```

---

## 📝 Template: recon/api_endpoints.md

```markdown
# API Endpoints Inventory

## Date: [DATE]
## Discovery Method: [gobuster/dirb/manual]

## Authentication Endpoints
### POST /api/v1/auth/login
- **Parameters**: email, password
- **Response**: Sets cookie `sid`
- **Auth Required**: No
- **Vulnerabilities**: Broken Authentication

### POST /api/v1/auth/token
- **Parameters**: email, password
- **Response**: JWT token
- **Auth Required**: No

## Course Endpoints
### GET /api/v1/courses
- **Parameters**: filter (query string)
- **Response**: JSON array of courses
- **Auth Required**: No
- **Vulnerabilities**: SQL Injection (filter parameter)

### GET /api/v1/courses/{id}
- **Parameters**: id (path parameter)
- **Response**: Course details
- **Auth Required**: No
- **Vulnerabilities**: Reflected XSS (in search results)

## Enrollment Endpoints
### POST /api/v1/enrollments
- **Parameters**: course_id, student_id
- **Response**: Enrollment confirmation
- **Auth Required**: Yes
- **Vulnerabilities**: CSRF (no token check)

### DELETE /api/v1/enrollments/{id}
- **Parameters**: id (path parameter)
- **Response**: Deletion confirmation
- **Auth Required**: Yes

## Admin Endpoints
### POST /api/v1/admin/courses
- **Parameters**: course data
- **Response**: Created course
- **Auth Required**: Yes (admin role)

## Audit Endpoints
### GET /api/v1/audit?user={id}
- **Parameters**: user (query string)
- **Response**: Audit logs
- **Auth Required**: Yes
```

---

## 📝 Template: docs/threat_model.md

```markdown
# Threat Model Document
## Course Registration System

**Date**: [DATE]
**Version**: 1.0 (Baseline - Unpatched)
**Authors**: [TEAM MEMBERS]

---

## Executive Summary

[2-3 sentence overview of the system and its security posture]

---

## 1. Key Assets

### 1.1 Database
- **Description**: PostgreSQL/MySQL database containing user data, courses, enrollments
- **Sensitivity**: High
- **Contains**: PII, passwords (weakly hashed), enrollment records

### 1.2 Personal Identifiable Information (PII)
- **Description**: User emails, student IDs, enrollment history
- **Sensitivity**: High
- **Location**: Database, API responses

### 1.3 Admin Console
- **Description**: Administrative interface for course management
- **Sensitivity**: Critical
- **Access**: Admin role only

### 1.4 Authentication Tokens
- **Description**: Session cookies (sid), JWT tokens
- **Sensitivity**: High
- **Location**: Client-side storage, HTTP headers

---

## 2. Potential Attackers

### 2.1 Student User
- **Motivation**: Academic advantage, curiosity
- **Capabilities**: Limited (student role)
- **Access**: Authenticated student account
- **Risk Level**: Medium

### 2.2 External Attacker
- **Motivation**: Data theft, system compromise, reputation damage
- **Capabilities**: High (can exploit vulnerabilities)
- **Access**: Public endpoints
- **Risk Level**: High

### 2.3 Malicious Insider
- **Motivation**: Privilege escalation, data exfiltration
- **Capabilities**: High (authenticated access)
- **Access**: Authenticated account (any role)
- **Risk Level**: Critical

---

## 3. Attacker Goals

### 3.1 Data Exfiltration
- **Target**: User PII, enrollment records, course data
- **Methods**: SQL Injection, unauthorized API access
- **Impact**: Privacy violation, identity theft

### 3.2 Privilege Escalation
- **Target**: Admin access, instructor privileges
- **Methods**: Broken authentication, session hijacking
- **Impact**: Unauthorized system control

### 3.3 Denial of Service (DoS)
- **Target**: Application availability
- **Methods**: Resource exhaustion, SQL injection causing database locks
- **Impact**: Service unavailability

### 3.4 Data Manipulation
- **Target**: Course enrollments, grades, course data
- **Methods**: CSRF, SQL Injection
- **Impact**: Academic integrity violation

---

## 4. Top-10 Attack Surfaces

### 1. `/api/v1/courses?filter=` - SQL Injection
- **Vulnerability**: Unsanitized SQL query parameter
- **Severity**: Medium
- **Impact**: Database compromise, data exfiltration
- **Entry Point**: GET parameter `filter`

### 2. Course Search Results - Reflected XSS
- **Vulnerability**: User input echoed without sanitization
- **Severity**: Low
- **Impact**: Session hijacking, credential theft
- **Entry Point**: Search input field

### 3. `/api/v1/enrollments` - CSRF
- **Vulnerability**: Missing CSRF token validation
- **Severity**: High
- **Impact**: Unauthorized enrollment actions
- **Entry Point**: POST request without CSRF protection

### 4. Authentication Endpoints - Broken Authentication
- **Vulnerability**: Weak password policy, session management issues
- **Severity**: High
- **Impact**: Account compromise, privilege escalation
- **Entry Point**: Login, password reset endpoints

### 5. Session Management
- **Vulnerability**: Insecure cookie flags, predictable session IDs
- **Severity**: Medium
- **Impact**: Session hijacking
- **Entry Point**: Session cookies

### 6. Admin Endpoints
- **Vulnerability**: Insufficient authorization checks
- **Severity**: Critical
- **Impact**: Unauthorized administrative actions
- **Entry Point**: `/api/v1/admin/*` endpoints

### 7. Audit Log Endpoint
- **Vulnerability**: Missing access control
- **Severity**: Medium
- **Impact**: Information disclosure
- **Entry Point**: `/api/v1/audit?user={id}`

### 8. Password Reset
- **Vulnerability**: Weak reset mechanism
- **Severity**: Medium
- **Impact**: Account takeover
- **Entry Point**: `/api/v1/auth/reset-password`

### 9. JWT Token Generation
- **Vulnerability**: Weak token signing, no expiration
- **Severity**: Medium
- **Impact**: Token forgery, long-lived sessions
- **Entry Point**: `/api/v1/auth/token`

### 10. Cookie Handling
- **Vulnerability**: Missing HttpOnly/Secure flags
- **Severity**: Medium
- **Impact**: XSS-based cookie theft
- **Entry Point**: All authenticated endpoints

---

## 5. Risk Ranking Table

| Vulnerability Class | Asset Affected | Likelihood | Impact | Priority |
|---------------------|---------------|------------|--------|----------|
| SQL Injection | Database | High | Critical | **P1** |
| CSRF | Enrollment Data | High | High | **P1** |
| Broken Authentication | User Accounts | High | High | **P1** |
| Reflected XSS | User Sessions | Medium | Medium | **P2** |
| Insecure Session Management | User Sessions | Medium | High | **P2** |
| Admin Access Control | Admin Console | Low | Critical | **P2** |
| Audit Log Exposure | Audit Data | Medium | Medium | **P3** |
| Weak Password Reset | User Accounts | Medium | High | **P2** |
| JWT Vulnerabilities | API Access | Low | Medium | **P3** |
| Cookie Security | User Sessions | Medium | Medium | **P2** |

**Priority Legend:**
- **P1**: Critical - Address immediately
- **P2**: High - Address soon
- **P3**: Medium - Address when possible

---

## 6. Mitigation Recommendations

*(To be implemented in later stages)*

### SQL Injection
- Use parameterized queries
- Input validation and sanitization
- ORM usage instead of raw SQL

### CSRF
- Implement CSRF tokens
- SameSite cookie attribute
- Verify Origin/Referer headers

### Broken Authentication
- Strong password policy
- Multi-factor authentication
- Secure session management
- Rate limiting on login attempts

### XSS
- Input sanitization
- Output encoding
- Content Security Policy (CSP)

---

## Appendix

### A. Architecture Diagram
See: `docs/architecture.svg`

### B. Data Flow Diagram
See: `docs/dataflow.svg`

### C. Reconnaissance Artifacts
- Stack Inventory: `recon/stack_inventory.md`
- API Endpoints: `recon/api_endpoints.md`
```

---

## ⏰ 2-Day Timeline

### **Day 1 (8-10 hours)**

**Morning (4-5 hours):**
- Person 1: Environment setup, application reconnaissance
- Person 2: API surface mapping, endpoint discovery

**Afternoon (4-5 hours):**
- Person 1: Threat model - assets & attackers, start architecture diagram
- Person 2: Threat model - attack surfaces, start data-flow diagram

### **Day 2 (6-8 hours)**

**Morning (3-4 hours):**
- Person 1: Complete architecture diagram
- Person 2: Complete data-flow diagram, create risk ranking table

**Afternoon (3-4 hours):**
- Both: Combine threat model document
- Both: Review and refine all documentation
- Both: Export to PDF, create git tag, finalize submission

---

## ✅ Submission Checklist

- [ ] `docs/threat_model.md` completed (2-3 pages)
- [ ] `docs/threat_model.pdf` exported
- [ ] `docs/architecture.svg` created and clear
- [ ] `docs/dataflow.svg` created and clear
- [ ] `recon/stack_inventory.md` with whatweb/curl results
- [ ] `recon/api_endpoints.md` with gobuster/dirb results
- [ ] Git tag `baseline-unpatched` created
- [ ] All files committed to repository
- [ ] Documentation reviewed for clarity and completeness

---

## 🚀 Quick Start Commands

```bash
# Create directory structure
mkdir -p docs recon backend frontend

# Initialize git (if not done)
git init
git add .
git commit -m "Initial project structure"

# After completing Stage 1, create baseline tag
git tag -a baseline-unpatched -m "Baseline unpatched version for Stage 1"
git push origin baseline-unpatched
```

---

## 📚 Resources

- **draw.io/diagrams.net**: https://app.diagrams.net/
- **OWASP Threat Modeling**: https://owasp.org/www-community/Threat_Modeling
- **whatweb**: https://github.com/urbanadventurer/WhatWeb
- **gobuster**: https://github.com/OJ/gobuster

