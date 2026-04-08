from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user with input validation"""
    try:
        data = request.get_json()
        
        # INPUT VALIDATION
        if not data or not data.get('username') or not data.get('password') or not data.get('email'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        username = str(data.get('username')).strip()
        email = str(data.get('email')).strip()
        password = data.get('password')
        role = str(data.get('role', 'student')).strip()
        
        # Whitelist roles (prevent privilege escalation)
        if role not in ['student', 'instructor']:
            role = 'student'
        
        # Validate username length
        if len(username) < 3 or len(username) > 80:
            return jsonify({'error': 'Username must be 3-80 characters'}), 400
        
        # Basic email validation
        if '@' not in email or len(email) > 120:
            return jsonify({'error': 'Invalid email'}), 400
        
        # Password strength check
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(username=username, email=email, role=role)
        user.set_password(password)   # Hashes the password securely
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful', 
            'user_id': user.id,
            'role': user.role
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500
