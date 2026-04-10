# SecureQuizPlatform-Spring2026

## Project Overview
SecureQuizPlatform-Spring2026 is a Flask-based web application developed as part of a secure software development project.  
The project demonstrates secure coding practices, CI/CD integration, and security testing using automated and manual methods.

## Features
- Flask web application
- Quiz result page
- CI/CD pipeline using GitHub Actions
- Static Application Security Testing (SAST) using CodeQL
- Dynamic Application Security Testing (DAST) using OWASP ZAP
- Manual security validation

## Project Structure
SecureQuizPlatform-Spring2026/
│── app.py  
│── requirements.txt  
│── README.md  
│── SECURITY_TEST_REPORT.md  
│── tests/  
│   └── test_dummy.py  
│── docs/  
│── .github/  
│   └── workflows/  
│       └── ci-cd.yml  

## CI/CD Pipeline
The project uses GitHub Actions for:
- Installing dependencies
- Running pytest tests
- Verifying code automatically on push and pull request

## Security Testing
### SAST
- CodeQL enabled through GitHub Security tab

### DAST
- OWASP ZAP active scan performed on:
- http://127.0.0.1:5000

### Manual Testing
- IDOR tested
- CSRF tested
- Clickjacking tested

## Running the Project Locally
1. Install dependencies:
pip install -r requirements.txt

2. Run application:
python app.py

3. Open browser:
http://127.0.0.1:5000

## Team Workflow
- Feature branches used for development
- Pull requests required before merging
- Main branch protected

## Status
Project completed successfully with CI/CD passing.