from flask import Blueprint, jsonify, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    """Home page"""
    if session.get('user_id'):
        return jsonify({
            'message': 'Welcome to Secure Quiz Platform',
            'user': session.get('username'),
            'role': session.get('role'),
            'available_routes': {
                'auth': '/api/auth/login, /api/auth/register, /api/auth/logout, /api/auth/profile',
                'quiz': '/api/quiz/create, /api/quiz/<id>, /api/quiz/<id>/results'
            }
        }), 200
    else:
        return jsonify({
            'message': 'Welcome to Secure Quiz Platform',
            'status': 'Not logged in',
            'quick_start': {
                'register': 'POST /api/auth/register',
                'login': 'POST /api/auth/login'
            }
        }), 200

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200
