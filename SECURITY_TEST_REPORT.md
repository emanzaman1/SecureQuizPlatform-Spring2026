# SECURITY TEST REPORT

## Project: SecureQuizPlatform-Spring2026

Course: CYC386 – Secure Software Design and Development
Team: Amina, Faiza, Eman
Date: April 2026

---

# 1. Introduction

This report presents the results of security testing performed on the SecureQuizPlatform web application. The objective is to identify vulnerabilities using:

* Static Application Security Testing (SAST)
* Dynamic Application Security Testing (DAST)
* Manual Penetration Testing

The testing ensures that the system meets security requirements defined during the Protection Needs Elicitation (PNE) phase.

---

# 2. Testing Scope

## 2.1 Target System

* Web-based quiz/exam platform
* Local deployment: http://127.0.0.1:5000

## 2.2 Components Tested

* Authentication system
* Exam/result endpoints
* Form submissions
* Session management
* HTTP security headers

---

# 3. Tools and Methodology

## 3.1 SAST (Static Analysis)

* Tool: GitHub CodeQL
* Method: Automated code scanning via GitHub Actions
* Trigger: Push and Pull Request events

## 3.2 DAST (Dynamic Analysis)

* Tool: OWASP ZAP
* Method: Active scan on running application
* Attack Simulation: Injection, misconfiguration, session attacks

## 3.3 Manual Testing

* Custom test cases based on OWASP Top 10 vulnerabilities
* Focus on:

  * IDOR
  * CSRF
  * Clickjacking

---

# 4. SAST Results (CodeQL)

## 4.1 Scan Summary

* Scan Status: Completed Successfully
* Vulnerabilities Found: None

## 4.2 Analysis

* No critical, high, or medium severity issues detected
* Code adheres to secure coding practices
* Input handling and authentication logic are properly implemented

## 4.3 Evidence

* Screenshots of CodeQL results are included in repository

---

# 5. DAST Results (OWASP ZAP)

## 5.1 Scan Summary

* Scan Type: Active Scan
* Target: Localhost application
* Vulnerabilities Found: None (High/Medium)

## 5.2 Analysis

* No injection flaws detected
* No insecure headers identified
* Session handling appears secure
* No exposed endpoints or misconfigurations

## 5.3 Evidence

* Screenshots of:

  * Sites Tab
  * Alerts Tab
    are attached in repository

---

# 6. Manual Security Testing

## 6.1 IDOR (Insecure Direct Object Reference)

### Test Description:

Attempted to access another user's result by modifying URL parameters.

### Test Case:

* Original: `/result/1`
* Modified: `/result/2`

### Result:

* Access denied for unauthorized user

### Conclusion:

* Proper authorization checks implemented
* User cannot access resources they do not own

---

## 6.2 CSRF (Cross-Site Request Forgery)

### Test Description:

Attempted to submit forms without CSRF tokens.

### Method:

* Removed CSRF token from request
* Sent manual POST request

### Result:

* Request rejected by server

### Conclusion:

* CSRF protection mechanism is active and effective

---

## 6.3 Clickjacking

### Test Description:

Attempted to embed application in an iframe.

### Test Code:

```html
<iframe src="http://127.0.0.1:5000"></iframe>
```

### Result:

* Application refused to load in iframe

### Conclusion:

* Clickjacking protection enabled via security headers

---

# 7. Security Controls Verification

Control	Implementation	Status
Authentication	Login system with validation	✅ Implemented
Authorization	Resource ownership checks	✅ Implemented
CSRF Protection	Tokens in forms	✅ Implemented
Clickjacking Defense	X-Frame-Options / CSP	✅ Implemented
Session Security	Token/session validation	✅ Implemented

---

# 8. Vulnerability Summary

ID	Vulnerability	Severity	Status
V-01	IDOR	High	Not Found
V-02	CSRF	Medium	Not Found
V-03	Clickjacking	Medium	Not Found
V-04	SQL Injection	High	Not Found
V-05	Session Hijacking	High	Not Found

---

# 9. Fixed Vulnerabilities

* No vulnerabilities were identified during testing.
* Therefore, no remediation actions were required.

---

# 10. Limitations

* Testing was performed on a local environment only
* No large-scale load or stress testing performed
* External integrations (if any) were not tested

---

# 11. Conclusion

The SecureQuizPlatform demonstrates a strong security posture.

All SAST, DAST, and manual testing results confirm that the application is protected against common web vulnerabilities, including IDOR, CSRF, and Clickjacking.

The system follows secure development practices and meets the security requirements defined in earlier phases.

---

# 12. Recommendations

* Perform periodic security scans after updates
* Implement logging and monitoring for real-time threat detection
* Conduct penetration testing in production environment
* Apply regular dependency updates

---

**End of Security Test Report**

