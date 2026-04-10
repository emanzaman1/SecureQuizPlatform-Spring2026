# SECURITY TEST REPORT

## Project: SecureQuizPlatform-Spring2026

---

## 1. SAST (Static Application Security Testing)

* Tool Used: GitHub CodeQL
* Scan Type: Automated Static Code Analysis
* Trigger: GitHub Actions (on push & pull request)

### Results:

* CodeQL scan completed successfully.
* No critical, high, or medium vulnerabilities were detected.
* Code quality and security standards are maintained.

### Evidence:

* Screenshots of CodeQL scan results are attached in the repository.

---

## 2. DAST (Dynamic Application Security Testing)

* Tool Used: OWASP ZAP
* Scan Type: Active Scan
* Target: Localhost application (`http://127.0.0.1:5000`)

### Results:

* ZAP active scan completed successfully.
* No high or medium risk vulnerabilities detected.
* Application endpoints responded securely to automated attack simulations.

### Evidence:

* Screenshots of "Sites" and "Alerts" tabs are attached.

---

## 3. Manual Security Testing

Manual testing was performed to validate common web vulnerabilities:

### 3.1 IDOR (Insecure Direct Object Reference)

* Test: Modified URL from `/result/1` to `/result/2`
* Result: Unauthorized access was blocked.
* Conclusion: Proper access control is implemented.

---

### 3.2 CSRF (Cross-Site Request Forgery)

* Test: Attempted form submission without CSRF token
* Result: Request was rejected.
* Conclusion: CSRF protection mechanism is working correctly.

---

### 3.3 Clickjacking

* Test: Embedded application inside an `<iframe>`
* Result: Application refused to load inside iframe.
* Conclusion: Clickjacking protection (e.g., X-Frame-Options) is enabled.

---

## 4. Fixed Vulnerabilities

* No vulnerabilities were identified during SAST, DAST, or manual testing.
* Therefore, no fixes were required at this stage.

---

## 5. Conclusion

The SecureQuizPlatform application demonstrates a strong security posture.
All automated and manual security tests indicate that the system is resistant to common web vulnerabilities.

Continuous monitoring and regular security testing are recommended to maintain this security level.

---
