from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User
from app.decorators import login_required
from datetime import timedelta
import traceback
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user with input validation"""
    try:
        print("\n📝 REGISTER REQUEST RECEIVED")
        print(f"Headers: {dict(request.headers)}")
        
        # Get JSON data
        data = request.get_json(force=True, silent=True)
        print(f"Received data: {data}")
        
        if not data:
            print("❌ No JSON data")
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # INPUT VALIDATION
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        email = data.get('email', '').strip()
        
        print(f"Username: {username}, Email: {email}, Password: {'*' * len(password)}")
        
        if not username or not password or not email:
            return jsonify({'error': 'Missing required fields: username, password, email'}), 400
        
        role = str(data.get('role', 'student')).strip()
        
        # Whitelist roles
        if role not in ['student', 'instructor']:
            role = 'student'
        
        # Validate username length
        if len(username) < 3 or len(username) > 80:
            return jsonify({'error': 'Username must be 3-80 characters'}), 400
        
        # Validate email format
        if '@' not in email or len(email) > 120:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 409
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create user with hashed password
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        print(f"✅ Creating user: {username} with role: {role}")
        
        db.session.add(user)
        db.session.commit()
        
        print(f"✅ User registered successfully! ID: {user.id}")
        
        return jsonify({
            'message': 'Registration successful',
            'user_id': user.id,
            'username': user.username,
            'role': user.role
        }), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ REGISTRATION ERROR: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Secure login with session management"""
    try:
        print("\n🔐 LOGIN REQUEST RECEIVED")
        print(f"Headers: {dict(request.headers)}")
        
        # Get JSON data
        data = request.get_json(force=True, silent=True)
        print(f"Received data: {data}")
        
        if not data:
            print("❌ No JSON data")
            return jsonify({'error': 'No JSON data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        print(f"Login attempt - Username: {username}, Password: {'*' * len(password)}")
        
        # INPUT VALIDATION
        if not username or not password:
            print("❌ Missing credentials")
            return jsonify({'error': 'Missing username or password'}), 400
        
        # Query user by username
        user = User.query.filter_by(username=username).first()
        print(f"User found: {user is not None}")
        
        if not user:
            print(f"❌ User '{username}' not found in database")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        password_correct = user.check_password(password)
        print(f"Password correct: {password_correct}")
        
        if not password_correct:
            print("❌ Password incorrect")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create secure session
        print("✅ Creating session...")
        session.clear()
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        session.permanent = True
        session.permanent_session_lifetime = timedelta(minutes=30)
        
        print(f"✅ Login successful! User: {username}, Role: {user.role}")
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'username': user.username,
            'role': user.role
        }), 200
    
    except Exception as e:
        print(f"\n❌ LOGIN ERROR: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Clear session securely"""
    print("\n👋 LOGOUT REQUEST")
    session.clear()
    print("✅ Session cleared")
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile"""
    print("\n👤 PROFILE REQUEST")
    user_id = session.get('user_id')
    print(f"User ID from session: {user_id}")
    
    user = User.query.get(user_id)
    
    if not user:
        print("❌ User not found")
        return jsonify({'error': 'User not found'}), 404
    
    print(f"✅ Profile retrieved for user: {user.username}")
    
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat()
    }), 200
