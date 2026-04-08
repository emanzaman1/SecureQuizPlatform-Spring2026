from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # ================== CONFIGURATION ==================
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz.db')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # CSRF Protection
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # Strong Session Security (helps prevent CSRF)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    
    # Import all models
    with app.app_context():
        from app.models import User, Quiz, Question, QuizResponse
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.quiz import quiz_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    
    # ================== SECURITY HEADERS (Clickjacking + others) ==================
    @app.after_request
    def set_security_headers(response):
        # Prevent MIME-type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Clickjacking Protection
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'none';"
        
        # XSS Protection (for older browsers)
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
    
    return app
