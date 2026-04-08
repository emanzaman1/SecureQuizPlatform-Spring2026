from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Quiz, QuizResponse, User
from app.decorators import login_required, admin_or_instructor_required

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')

def check_quiz_ownership(quiz_id, user_id):
    """IDOR FIX: Verify user owns the quiz before allowing modification"""
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return None, jsonify({'error': 'Quiz not found'}), 404
    
    # Only the creator can modify/delete the quiz
    if quiz.creator_id != user_id:
        return None, jsonify({'error': 'Unauthorized - not quiz owner'}), 403
    
    return quiz, None, 200


@quiz_bp.route('/create', methods=['POST'])
@login_required
@admin_or_instructor_required
def create_quiz():
    """Create new quiz (instructor/admin only)"""
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        # INPUT VALIDATION
        if not data or not data.get('title'):
            return jsonify({'error': 'Missing quiz title'}), 400
        
        title = str(data.get('title')).strip()
        description = str(data.get('description', '')).strip()
        
        if len(title) < 3 or len(title) > 200:
            return jsonify({'error': 'Title must be 3-200 characters'}), 400
        
        # Create quiz with creator_id (prevents IDOR)
        quiz = Quiz(
            title=title,
            description=description,
            creator_id=user_id
        )
        
        db.session.add(quiz)
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz created successfully',
            'quiz_id': quiz.id,
            'creator_id': quiz.creator_id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create quiz'}), 500


@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
@login_required
def get_quiz(quiz_id):
    """Retrieve quiz details with IDOR protection"""
    user_id = session.get('user_id')
    user_role = session.get('role')
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Students can view any quiz (for taking it), instructors see their own
    if user_role == 'student' or quiz.creator_id == user_id or user_role == 'admin':
        return jsonify({
            'quiz_id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'creator_id': quiz.creator_id,
            'questions_count': len(quiz.questions) if quiz.questions else 0
        }), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 403


@quiz_bp.route('/<int:quiz_id>', methods=['PUT'])
@login_required
def update_quiz(quiz_id):
    """Update quiz (IDOR FIX: Only owner can update)"""
    user_id = session.get('user_id')
    
    # IDOR protection
    quiz, error_response, status = check_quiz_ownership(quiz_id, user_id)
    if error_response:
        return error_response, status
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if 'title' in data:
            title = str(data['title']).strip()
            if len(title) < 3 or len(title) > 200:
                return jsonify({'error': 'Title must be 3-200 characters'}), 400
            quiz.title = title
            
        if 'description' in data:
            quiz.description = str(data['description']).strip()
        
        db.session.commit()
        return jsonify({'message': 'Quiz updated successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update quiz'}), 500


@quiz_bp.route('/<int:quiz_id>', methods=['DELETE'])
@login_required
def delete_quiz(quiz_id):
    """Delete quiz (IDOR FIX: Only owner can delete)"""
    user_id = session.get('user_id')
    
    # IDOR protection
    quiz, error_response, status = check_quiz_ownership(quiz_id, user_id)
    if error_response:
        return error_response, status
    
    try:
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({'message': 'Quiz deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete quiz'}), 500


@quiz_bp.route('/<int:quiz_id>/results', methods=['GET'])
@login_required
def get_results(quiz_id):
    """Get quiz results with proper authorization"""
    user_id = session.get('user_id')
    user_role = session.get('role')
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # IDOR + RBAC protection
    if user_role == 'student':
        # Students can only see their own results
        results = QuizResponse.query.filter_by(quiz_id=quiz_id, user_id=user_id).all()
    elif user_role in ['instructor', 'admin']:
        # Instructors can only see results of quizzes they created
        if quiz.creator_id != user_id and user_role != 'admin':
            return jsonify({'error': 'Unauthorized - not quiz owner'}), 403
        results = QuizResponse.query.filter_by(quiz_id=quiz_id).all()
    else:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'quiz_id': quiz_id,
        'results': [{
            'response_id': r.id,
            'student_id': r.user_id,
            'score': r.score,
            'submitted_at': r.submitted_at.isoformat() if r.submitted_at else None
        } for r in results]
    }), 200
