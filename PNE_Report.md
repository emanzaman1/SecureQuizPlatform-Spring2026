# Protection Needs Elicitation (PNE) Report
**Project:** Online Exam/Quiz Platform  
**Course:** CYC386 – Secure Software Design and Development  
**Member:** amina, faiza, eman
**Date:** 4 April 2026  

---

## 1. Assets

| Asset ID | Asset Name | Type | Description | Sensitivity |
|----------|-----------|------|-------------|-------------|
| A-01 | User Credentials | Data | Usernames & hashed passwords | CRITICAL |
| A-02 | Exam Question Papers | Data | Questions created by instructors | HIGH |
| A-03 | Student Exam Results | Data | Scores and answers submitted | HIGH |
| A-04 | Session Tokens / JWT | Data | Authentication tokens per user | CRITICAL |
| A-05 | Student Personal Info | Data | Name, email, student ID | MEDIUM |
| A-06 | Web Application Code | Software | Flask/FastAPI source code | HIGH |
| A-07 | Database | Infrastructure | SQLite/PostgreSQL storing all data | CRITICAL |
| A-08 | CI/CD Pipeline | Infrastructure | GitHub Actions workflows | MEDIUM |
| A-09 | Admin Panel | Feature | System configuration & user mgmt | HIGH |
| A-10 | Exam Integrity | Process | Ensuring no cheating during exam | HIGH |

---

## 2. Stakeholders

### 2.1 Internal Stakeholders

| ID | Role | Description | Access Level |
|----|------|-------------|--------------|
| S-01 | Student | Takes exams, views own results only | LOW |
| S-02 | Instructor | Creates exams, views results | MEDIUM |
| S-03 | Admin | Manages users, full system access | HIGH |
| S-04 | Developer | Builds and maintains the platform | SYSTEM |

### 2.2 External Stakeholders / Threat Actors

| ID | Threat Actor | Motivation | Capability |
|----|-------------|------------|------------|
| T-01 | Malicious Student | Cheat in exam, see others answers | LOW-MEDIUM |
| T-02 | External Attacker | Data theft, system disruption | MEDIUM-HIGH |
| T-03 | Insider Threat | Instructor leaking question papers | MEDIUM |
| T-04 | Script Kiddie | Random attacks using known tools | LOW |

---

## 3. Threat Identification

### 3.1 IDOR – Insecure Direct Object Reference

**What it is:**  
Jab koi student URL mein ID change karke doosre student ki result ya exam dekh le.

**Example Attack:**  
- Normal URL:   `/results?student_id=101` (apni result)  
- Attacker URL: `/results?student_id=102` (doosre ki result)  

**Who does it:** Malicious Student (T-01)  
**Asset at Risk:** Student Exam Results (A-03), Exam Question Papers (A-02)  
**Impact:** Unauthorized data access, exam cheating  
**Likelihood:** HIGH – very easy to do manually  

---

### 3.2 CSRF – Cross-Site Request Forgery

**What it is:**  
Attacker ek fake website banata hai jo secretly quiz platform pe request bhejti hai — victim ke browser se — bina unko pata chale.

**Example Attack:**  
1. Instructor logged in hai quiz platform pe  
2. Attacker email bhejta hai fake link ke saath  
3. Instructor click karta hai  
4. Background mein exam settings change ho jaati hain (instructor ki session use karke)  

**Who does it:** External Attacker (T-02)  
**Asset at Risk:** Exam Settings, User Accounts (A-02, A-09)  
**Impact:** Unauthorized actions performed on behalf of user  
**Likelihood:** MEDIUM  

---

### 3.3 Clickjacking

**What it is:**  
Attacker quiz page ko ek invisible iframe mein daalta hai apni website ke upar — user sochta hai kuch aur click kar raha hai lekin actually quiz submit ho raha hai.

**Example Attack:**  
1. Fake website dikhti hai: "Win a Prize! Click here!"  
2. Neeche invisible layer mein quiz platform hai  
3. User click karta hai "Win Prize" pe  
4. Actually quiz submit ho jaata hai ya answer change ho jaata hai  

**Who does it:** External Attacker (T-02), Malicious Student (T-01)  
**Asset at Risk:** Exam Integrity (A-10)  
**Impact:** Exam manipulation, unintended actions by user  
**Likelihood:** MEDIUM  

---

### 3.4 Additional Threats

| ID | Threat | Description | Asset at Risk |
|----|--------|-------------|---------------|
| TH-04 | SQL Injection | Malicious input in login or search fields | A-07 |
| TH-05 | Brute Force | Repeated login attempts to guess password | A-01 |
| TH-06 | Session Hijacking | Stealing JWT token from network or storage | A-04 |
| TH-07 | Privilege Escalation | Student accessing instructor features | A-09 |

---

## 4. Protection Needs

### 4.1 Confidentiality Needs
- Student results sirf us student ko dikhni chahiye  
- Exam papers sirf instructor ko accessible hone chahiye  
- Passwords kabhi plaintext store na hon  

### 4.2 Integrity Needs
- Exam submissions change na ho sakein after submit  
- Scores modify na ho sakein by unauthorized users  
- CSRF tokens ensure karein ke requests genuine hain  

### 4.3 Availability Needs
- Exam ke doran system crash na ho  
- Rate limiting ho taake DoS attacks se bachein  

### 4.4 Protection Needs Table

| Asset | Confidentiality | Integrity | Availability | Priority |
|-------|----------------|-----------|--------------|----------|
| User Credentials (A-01) | CRITICAL | HIGH | MEDIUM | P1 |
| Exam Papers (A-02) | HIGH | CRITICAL | HIGH | P1 |
| Student Results (A-03) | HIGH | CRITICAL | HIGH | P1 |
| Session Tokens (A-04) | CRITICAL | HIGH | LOW | P1 |
| Database (A-07) | HIGH | CRITICAL | HIGH | P1 |
| Admin Panel (A-09) | HIGH | HIGH | MEDIUM | P2 |

---

## 5. Security Requirements

### SR-01: IDOR Prevention
- **Requirement:** Every data access endpoint MUST verify that the requesting user owns that resource  
- **Implementation:** Server-side ownership check before returning any exam or result data  
- **Addresses:** Threat TH-01, Asset A-02, A-03  

### SR-02: CSRF Protection
- **Requirement:** All state-changing forms MUST include CSRF tokens; cookies must have SameSite=Strict  
- **Implementation:** Flask-WTF CSRF middleware on all POST/PUT/DELETE endpoints  
- **Addresses:** Threat TH-02, Asset A-02, A-09  

### SR-03: Clickjacking Prevention
- **Requirement:** Application MUST set X-Frame-Options: DENY and CSP frame-ancestors none on all responses  
- **Implementation:** Security headers middleware applied globally  
- **Addresses:** Threat TH-03, Asset A-10  

### SR-04: Authentication Security
- **Requirement:** Passwords MUST be hashed with bcrypt; JWT tokens must expire after 30 minutes  
- **Implementation:** bcrypt library for hashing, JWT expiry configuration  
- **Addresses:** Threat TH-05, TH-06, Asset A-01, A-04  

### SR-05: Role-Based Access Control (RBAC)
- **Requirement:** Role checks on every protected route  
- Student cannot access /instructor/* endpoints  
- Instructor cannot access /admin/* endpoints  
- **Implementation:** Middleware role verification on all protected routes  
- **Addresses:** Threat TH-07, Asset A-09