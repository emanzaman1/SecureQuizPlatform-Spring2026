import os
import sys
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

if __name__ == '__main__':
    # Enable detailed error logging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    print("\n" + "="*60)
    print("🚀 SECURE QUIZ PLATFORM - DEVELOPMENT SERVER")
    print("="*60)
    print("📌 API Base URL: http://127.0.0.1:5000")
    print("📌 Register: POST /api/auth/register")
    print("📌 Login: POST /api/auth/login")
    print("📌 Profile: GET /api/auth/profile")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
