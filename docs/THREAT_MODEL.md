# PNE Report – Online Exam Platform
**Team:** Amina, Faiza, Eman | **Date:** 4 April 2026 | **Course:** CYC386

## 1. Assets
| ID | Asset | Sensitivity |
|----|-------|-------------|
| A-01 | User Credentials (passwords) | CRITICAL |
| A-02 | Exam Question Papers | HIGH |
| A-03 | Student Exam Results | HIGH |
| A-04 | Session Tokens / JWT | CRITICAL |
| A-05 | Student Personal Info (name, email, ID) | MEDIUM |
| A-06 | Web App Source Code | HIGH |
| A-07 | Database | CRITICAL |
| A-08 | CI/CD Pipeline | MEDIUM |
| A-09 | Admin Panel | HIGH |
| A-10 | Exam Integrity | HIGH |

## 2. Stakeholders
| Role | Access |
|------|--------|
| Student | LOW |
| Instructor | MEDIUM |
| Admin | HIGH |
| Developer | SYSTEM |

**Threat Actors:** Malicious Student, External Attacker, Insider Threat, Script Kiddie

## 3. Threats (Mandatory OWASP)
### IDOR
- **Attack:** Change `?student_id=101` → `102` to see others' results
- **Risk:** HIGH likelihood, HIGH impact
- **Asset:** A-03

### CSRF
- **Attack:** Fake site sends state-changing request using victim's session
- **Risk:** MEDIUM likelihood, HIGH impact
- **Asset:** A-02, A-09

### Clickjacking
- **Attack:** Invisible iframe tricks user into clicking quiz buttons
- **Risk:** MEDIUM likelihood, HIGH impact
- **Asset:** A-10

### Additional Threats
SQL Injection, Brute Force, Session Hijacking, Privilege Escalation

## 4. Protection Needs
| Asset | Confidentiality | Integrity | Priority |
|-------|----------------|-----------|----------|
| A-01 | CRITICAL | HIGH | P1 |
| A-02 | HIGH | CRITICAL | P1 |
| A-03 | HIGH | CRITICAL | P1 |
| A-04 | CRITICAL | HIGH | P1 |
| A-07 | HIGH | CRITICAL | P1 |
| A-09 | HIGH | HIGH | P2 |

## 5. Security Requirements
| ID | Requirement |
|----|-------------|
| SR-01 | Ownership check on every endpoint (IDOR fix) |
| SR-02 | CSRF tokens + SameSite=Strict cookies |
| SR-03 | X-Frame-Options: DENY + CSP frame-ancestors 'none' |
| SR-04 | bcrypt for passwords; JWT expiry 30 min |
| SR-05 | Role-based access control (RBAC) middleware |

## 6. Next Steps
- Create DFDs (Level 0 & 1)
- Apply STRIDE + CVSS scoring
- Deliver `THREAT_MODEL.pdf`
