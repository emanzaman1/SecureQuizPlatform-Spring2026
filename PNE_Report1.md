Protection Needs Elicitation (PNE) Report
Project: Online Examination and Quiz Platform
Course: CYC386 – Secure Software Design and Development
Group Members: Amina, Faiza, Eman
Date: 4 April 2026

1. Asset Identification
Assets are any components—data, software, infrastructure, or processes—that require protection to ensure the secure operation of the system.
Asset ID	Asset Name	Type	Description	Sensitivity
A-01	User Credentials	Data	Usernames and securely hashed passwords	Critical
A-02	Exam Question Papers	Data	Questions authored by instructors	High
A-03	Student Exam Results	Data	Exam answers and calculated scores	High
A-04	Session Tokens / JWT	Data	Authentication tokens issued to users	Critical
A-05	Student Personal Information	Data	Name, email address, and student ID	Medium
A-06	Web Application Code	Software	Backend source code (Flask/FastAPI)	High
A-07	Database	Infrastructure	SQLite/PostgreSQL database storing all platform data	Critical
A-08	CI/CD Pipeline	Infrastructure	GitHub Actions workflows	Medium
A-09	Admin Panel	Feature	User management and system configuration interface	High
A-10	Exam Integrity	Process	Mechanisms ensuring fairness and preventing cheating	High
________________________________________
2. Stakeholder Analysis
2.1 Internal Stakeholders
ID	Role	Description	Access Level
S-01	Student	Takes exams and views own results only	Low
S-02	Instructor	Creates exams and reviews student performance	Medium
S-03	Administrator	Manages users and system configurations	High
S-04	Developer	Develops, deploys, and maintains the platform	System
2.2 External Stakeholders / Threat Actors
ID	Threat Actor	Motivation	Capability
T-01	Malicious Student	Cheating or accessing others’ data	Low–Medium
T-02	External Attacker	Data theft or system disruption	Medium–High
T-03	Insider Threat	Leaking sensitive exam materials	Medium
T-04	Script Kiddie	Exploiting known vulnerabilities	Low
________________________________________
3. Threat Identification
3.1 Insecure Direct Object Reference (IDOR)
Description:
An IDOR vulnerability occurs when a user manipulates object identifiers (such as IDs in URLs or parameters) to access resources belonging to other users without proper authorization checks.
Example Attack Scenario:
•	Legitimate URL: /results?student_id=101
•	Malicious manipulation: /results?student_id=102
Threat Actor: Malicious Student (T-01)
Assets at Risk: Student Exam Results (A-03), Exam Question Papers (A-02)
Impact: Unauthorized disclosure of sensitive academic data, exam cheating
Likelihood: High, as such attacks require minimal technical skill
________________________________________
3.2 Cross-Site Request Forgery (CSRF)
Description:
CSRF attacks force authenticated users to execute unwanted actions on a web application by exploiting their active session.
Example Attack Scenario:
1.	An instructor is logged into the exam platform
2.	The attacker sends a phishing email containing a malicious link
3.	The instructor clicks the link
4.	Unauthorized actions (e.g., modifying exam settings) are executed using the instructor’s session
Threat Actor: External Attacker (T-02)
Assets at Risk: Exam Configuration, User Accounts (A-02, A-09)
Impact: Unauthorized system modifications
Likelihood: Medium
________________________________________
3.3 Clickjacking
Description:
Clickjacking involves embedding the legitimate application inside an invisible iframe on a malicious website, tricking users into performing unintended actions.
Example Attack Scenario:
1.	User visits a fake website offering a reward
2.	The quiz platform is loaded invisibly in the background
3.	User clicks a visible button
4.	The click actually submits or alters an exam attempt
Threat Actors: External Attacker (T-02), Malicious Student (T-01)
Asset at Risk: Exam Integrity (A-10)
Impact: Manipulated submissions and compromised fairness
Likelihood: Medium
________________________________________
3.4 Additional Identified Threats
ID	Threat	Description	Asset at Risk
TH-04	SQL Injection	Malicious SQL payloads in input fields	A-07
TH-05	Brute Force Attacks	Repeated login attempts to guess credentials	A-01
TH-06	Session Hijacking	Theft or reuse of JWT/session tokens	A-04
TH-07	Privilege Escalation	Unauthorized access to higher-privilege features	A-09
________________________________________
4. Protection Needs Analysis
4.1 Confidentiality Requirements
•	Student exam results must only be accessible to the respective student
•	Exam papers must be restricted to authorized instructors
•	Credentials must never be stored or transmitted in plaintext
4.2 Integrity Requirements
•	Exam submissions must not be alterable after final submission
•	Scores must be protected from unauthorized modification
•	All state-changing requests must be validated as legitimate
4.3 Availability Requirements
•	The system must remain operational during examinations
•	Rate limiting must be enforced to mitigate denial-of-service attacks
4.4 Protection Needs Summary
Asset	Confidentiality	Integrity	Availability	Priority
User Credentials (A-01)	Critical	High	Medium	P1
Exam Papers (A-02)	High	Critical	High	P1
Student Results (A-03)	High	Critical	High	P1
Session Tokens (A-04)	Critical	High	Low	P1
Database (A-07)	High	Critical	High	P1
Admin Panel (A-09)	High	High	Medium	P2
________________________________________
5. Security Requirements Specification
SR-01: Prevention of IDOR Vulnerabilities
•	Requirement: Every data access request must verify ownership and authorization
•	Implementation: Enforce server-side access control checks before returning any resource
•	Mitigates: IDOR threats
•	Assets Protected: A-02, A-03
________________________________________
SR-02: CSRF Protection
•	Requirement: All state-changing requests must include a valid CSRF token
•	Implementation: Use Flask-WTF CSRF middleware and enforce SameSite=Strict cookies
•	Mitigates: CSRF attacks
•	Assets Protected: A-02, A-09
________________________________________
SR-03: Clickjacking Protection
•	Requirement: The application must not be embeddable in iframes
•	Implementation: Apply X-Frame-Options: DENY and CSP frame-ancestors 'none' headers globally
•	Mitigates: Clickjacking
•	Assets Protected: A-10
________________________________________
SR-04: Secure Authentication Management
•	Requirement: Passwords must be hashed using a strong algorithm and sessions must expire
•	Implementation: Use bcrypt for password hashing and configure JWT expiry to 30 minutes
•	Mitigates: Brute force and session hijacking
•	Assets Protected: A-01, A-04
________________________________________
SR-05: Role-Based Access Control (RBAC)
•	Requirement: Access to system functionality must be strictly role-based 
o	Students cannot access instructor or admin endpoints
o	Instructors cannot access admin-only functionality
•	Implementation: Role verification middleware on all protected routes
•	Mitigates: Privilege escalation
•	Assets Protected: A-09

