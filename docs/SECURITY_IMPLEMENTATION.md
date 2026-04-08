# Security Implementation Details - Secure Quiz Platform

**Implemented by Member 3**  
**Phase 3: Core Implementation + Vulnerability Fixes**

## 1. IDOR (Insecure Direct Object References) Fix

### Vulnerability
- Users could access or modify any quiz/results by changing the `quiz_id` in the URL.
- Example: Student A could view/edit Student B’s quiz or see others' scores.

### Fix Applied
- Created `check_quiz_ownership()` helper in `app/routes/quiz.py`
- All modification endpoints (PUT, DELETE) now verify `quiz.creator_id == current_user_id`
- Results endpoint restricts students to **their own** responses only
- Instructors/admins can only view results of quizzes they created

### Code Evidence
- `app/routes/quiz.py`: `check_quiz_ownership()` function
- GET/PUT/DELETE `/api/quiz/<int:quiz_id>` routes
- `/api/quiz/<int:quiz_id>/results` with role-based filtering

## 2. CSRF (Cross-Site Request Forgery) Fix

### Vulnerability
- Malicious sites could trick logged-in users into submitting unwanted requests (e.g., creating quizzes or changing settings).

### Fix Applied
- Enabled `Flask-WTF` CSRFProtect in `app/__init__.py`
- All state-changing routes (POST, PUT, DELETE) now require a valid CSRF token
- `SameSite=Strict` cookies + secure session configuration
- CSRF token automatically available in all templates

### Code Evidence
- `app/__init__.py`: `csrf = CSRFProtect()` + `WTF_CSRF_ENABLED`
- `app/templates/base.html`: `<meta name="csrf-token">` + `makeSecureRequest()` helper
- CSRF token sent via `X-CSRFToken` header in AJAX calls

## 3. Clickjacking Fix

### Vulnerability
- Attacker could embed the quiz platform in a hidden iframe to trick users into clicking malicious elements.

### Fix Applied
- Set strong anti-framing headers on **every response**
- `X-Frame-Options: DENY`
- `Content-Security-Policy: frame-ancestors 'none'`

### Code Evidence
- `app/__init__.py`: `@app.after_request` hook (`set_security_headers`)

## 4. Additional Security Measures

- **Password Security**: `werkzeug.security` with `pbkdf2:sha256` + strong minimum length (8+ chars)
- **Input Validation**: Length checks, whitelisting roles (`student`/`instructor`), stripping input
- **Session Security**: `HttpOnly`, `Secure`, `SameSite=Strict`, 30-minute timeout
- **Role-Based Access Control (RBAC)**: Custom decorators for different user types
- **Database Relationships**: Proper foreign keys with cascade delete where appropriate

## Testing Results

| Vulnerability       | Before Fix | After Fix |
|---------------------|------------|-----------|
| IDOR (Quiz Access)  | Possible   | Blocked (403) |
| CSRF Attacks        | Possible   | Blocked (400/403) |
| Clickjacking        | Possible   | Blocked by browser |
| Weak Passwords      | Accepted   | Enforced 8+ chars + hashing |
| Unauthorized Role Escalation | Possible | Blocked by whitelist |

**Next Steps**: Coordinate with Member 1 for CI/CD pipeline and full test suite integration.

---
*Last Updated: April 2026*
