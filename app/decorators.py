from functools import wraps
from flask import session, jsonify

def login_required(f):
    """Check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    """Check if user has the exact required role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('role')
            if not user_role or user_role != required_role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_or_instructor_required(f):
    """Check if user is admin or instructor"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = session.get('role')
        if user_role not in ['admin', 'instructor']:
            return jsonify({'error': 'Insufficient permissions'}), 403
        return f(*args, **kwargs)
    return decorated_function
