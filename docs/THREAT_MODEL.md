# Threat Model – Online Exam/Quiz Platform
**Course:** CYC386 – Secure Software Design  
**Member:** amina ,faiza ,eman
**Date:** April 2026  
**Methodology:** STRIDE + CVSS v3.1  

---

## 1. Data Flow Diagrams (DFDs)

### 1.1 System Overview DFD

**External Entities:**
- Student (Browser)
- Instructor (Browser)
- Admin (Browser)

**Processes:**
- P1: Authentication & Login
- P2: Exam Management
- P3: Exam Taking Interface
- P4: Result Processing

**Data Stores:**
- DS1: User Database (credentials, roles)
- DS2: Exam Database (questions, settings)
- DS3: Results Database (scores, answers)

**Data Flows:**
- Student → P1: Username + Password
- P1 → DS1: Credential Verification Query
- DS1 → P1: User Role + Auth Result
- P1 → Student: JWT Session Token
- Instructor → P2: Exam Questions + Settings
- P2 → DS2: Store Exam Data
- Student → P3: Exam Answers
- P3 → DS3: Store Submitted Answers
- P4 → Student: Final Score + Results

> DFD Diagram: See DFD_QuizPlatform.png in /docs folder

---

### 1.2 Trust Boundaries

| Boundary | Description |
|----------|-------------|
| TB-1 | Internet ↔ Web Application (public boundary) |
| TB-2 | Web Application ↔ Database (internal boundary) |
| TB-3 | Student Zone ↔ Instructor Zone (role boundary) |

---

## 2. STRIDE Threat Analysis

### 2.1 STRIDE Table

| ID | Threat | Category | Component | Description | Impact |
|----|--------|----------|-----------|-------------|--------|
| ST-01 | Fake Student Login | Spoofing | P1: Authentication | Attacker uses stolen credentials to login as another student | Unauthorized exam access |
| ST-02 | Answer Tampering | Tampering | P3: Exam Interface | Student modifies submitted answers via HTTP request manipulation | Unfair grade inflation |
| ST-03 | Exam Submission Denial | Repudiation | DS3: Results DB | Student claims they never submitted exam to retake it | Academic integrity issue |
| ST-04 | IDOR – Result Access | Info Disclosure | DS3: Results DB | Student changes result ID in URL to see others' scores | Privacy violation |
| ST-05 | IDOR – Exam Access | Info Disclosure | DS2: Exam DB | Student accesses future exam papers via URL manipulation | Exam integrity breach |
| ST-06 | CSRF Attack | Tampering | P2: Exam Management | Forged request changes exam settings using instructor session | Unauthorized changes |
| ST-07 | Clickjacking | Tampering | P3: Exam Interface | Quiz page embedded in hidden iframe to manipulate clicks | Exam manipulation |
| ST-08 | Brute Force Login | Spoofing | P1: Authentication | Automated password guessing attack on login endpoint | Account takeover |
| ST-09 | SQL Injection | Tampering | DS1/DS2/DS3 | Malicious SQL in input fields to extract/modify database | Full data breach |
| ST-10 | Session Hijacking | Spoofing | P1: Authentication | Stealing JWT token to impersonate logged-in user | Account takeover |
| ST-11 | Privilege Escalation | Elevation | P2: Exam Management | Student accesses instructor-only endpoints | Unauthorized exam creation |
| ST-12 | DoS – Exam Spam | Denial of Service | P3: Exam Interface | Flooding server with exam submissions to crash it | Service unavailability |

---

### 2.2 Detailed Threat Analysis (3 Mandatory)

#### ST-04: IDOR – Result Access
- **Attack Vector:** Network
- **Description:** Student changes `result_id=101` to `result_id=102` in URL
- **Affected Asset:** Results Database (DS3)
- **Trust Boundary Crossed:** TB-3 (Student Zone)
- **Current Control:** None (vulnerable)
- **Required Fix:** Server-side ownership verification before returning data

#### ST-06: CSRF Attack  
- **Attack Vector:** Network
- **Description:** Attacker tricks instructor into clicking malicious link; forged POST request modifies exam settings
- **Affected Asset:** Exam Database (DS2)
- **Trust Boundary Crossed:** TB-1 (Internet boundary)
- **Current Control:** None (vulnerable)
- **Required Fix:** CSRF tokens on all forms + SameSite=Strict cookies

#### ST-07: Clickjacking
- **Attack Vector:** Network
- **Description:** Quiz interface embedded in invisible iframe on attacker's site; user unknowingly submits exam
- **Affected Asset:** Exam Interface (P3)
- **Trust Boundary Crossed:** TB-1 (Internet boundary)
- **Current Control:** None (vulnerable)
- **Required Fix:** X-Frame-Options: DENY + CSP frame-ancestors 'none'

---

## 3. CVSS v3.1 Risk Scoring

### 3.1 Scoring Guide

| Metric | Options |
|--------|---------|
| Attack Vector (AV) | Network(N), Adjacent(A), Local(L), Physical(P) |
| Attack Complexity (AC) | Low(L), High(H) |
| Privileges Required (PR) | None(N), Low(L), High(H) |
| User Interaction (UI) | None(N), Required(R) |
| Confidentiality (C) | None(N), Low(L), High(H) |
| Integrity (I) | None(N), Low(L), High(H) |
| Availability (A) | None(N), Low(L), High(H) |

---

### 3.2 CVSS Scores Table

| ID | Threat | AV | AC | PR | UI | C | I | A | Score | Severity | Priority |
|----|--------|----|----|----|----|---|---|---|-------|----------|----------|
| ST-04 | IDOR – Result Access | N | L | L | N | H | N | N | 6.5 | MEDIUM | P1 |
| ST-05 | IDOR – Exam Access | N | L | L | N | H | H | N | 8.1 | HIGH | P1 |
| ST-06 | CSRF Attack | N | L | N | R | N | H | N | 6.5 | MEDIUM | P1 |
| ST-07 | Clickjacking | N | L | N | R | N | L | N | 4.3 | MEDIUM | P2 |
| ST-08 | Brute Force | N | L | N | N | H | H | N | 9.1 | CRITICAL | P1 |
| ST-09 | SQL Injection | N | L | N | N | H | H | H | 9.8 | CRITICAL | P1 |
| ST-10 | Session Hijacking | N | H | N | N | H | H | N | 7.4 | HIGH | P1 |
| ST-11 | Privilege Escalation | N | L | L | N | H | H | N | 8.1 | HIGH | P1 |
| ST-12 | DoS – Exam Spam | N | L | N | N | N | N | H | 7.5 | HIGH | P2 |

---

### 3.3 Risk Priority Summary

#### 🔴 CRITICAL (Score 9.0+) – Fix Immediately
- ST-09: SQL Injection (9.8)
- ST-08: Brute Force Login (9.1)

#### 🟠 HIGH (Score 7.0–8.9) – Fix in Phase 3
- ST-05: IDOR Exam Access (8.1)
- ST-11: Privilege Escalation (8.1)
- ST-10: Session Hijacking (7.4)
- ST-12: DoS Attack (7.5)

#### 🟡 MEDIUM (Score 4.0–6.9) – Fix in Phase 3b
- ST-04: IDOR Result Access (6.5)
- ST-06: CSRF Attack (6.5)
- ST-07: Clickjacking (4.3)

---

## 4. Mitigation Summary

| ID | Threat | Mitigation | Responsible |
|----|--------|------------|-------------|
| ST-04/05 | IDOR | Object-level authorization on every endpoint | Member 3 |
| ST-06 | CSRF | CSRF tokens + SameSite cookies | Member 3 |
| ST-07 | Clickjacking | X-Frame-Options + CSP headers | Member 3 |
| ST-08 | Brute Force | Rate limiting + account lockout | Member 3 |
| ST-09 | SQL Injection | Parameterized queries only | Member 3 |
| ST-10 | Session Hijacking | JWT expiry + HTTPS only | Member 3 |
| ST-11 | Privilege Escalation | RBAC middleware on all routes | Member 3 |
| ST-12 | DoS | Rate limiting + input validation | Member 3 |
