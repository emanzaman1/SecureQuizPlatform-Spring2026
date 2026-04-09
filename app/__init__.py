from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz.db')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session security
    app.config['SESSION_COOKIE_SECURE'] = False  # Set True for HTTPS in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
    
    # Disable CSRF for API endpoints (will re-enable for forms later)
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'  # Clickjacking fix
        response.headers['Content-Security-Policy'] = "frame-ancestors 'none'"
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.quiz import quiz_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    
    print("✅ SUCCESS: All blueprints registered!")
    print("✅ Available routes:")
    print("   - GET  /")
    print("   - GET  /health")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - POST /api/auth/logout")
    print("   - GET  /api/auth/profile")
    print("   - POST /api/quiz/create")
    print("   - GET  /api/quiz/<id>")
    print("   - PUT  /api/quiz/<id>")
    print("   - DELETE /api/quiz/<id>")
    print("   - GET  /api/quiz/<id>/results")
    
    return app
