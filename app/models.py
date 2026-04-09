from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, instructor, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and store password using pbkdf2"""
        try:
            self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            print(f"✅ Password hash created: {self.password_hash[:20]}...")
        except Exception as e:
            print(f"❌ Error hashing password: {e}")
            raise
    
    def check_password(self, password):
        """Verify password against hash"""
        try:
            result = check_password_hash(self.password_hash, password)
            print(f"Password verification result: {result}")
            return result
        except Exception as e:
            print(f"❌ Error checking password: {e}")
            return False
    
    def has_role(self, role):
        """Check if user has specific role"""
        return self.role == role

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creator = db.relationship('User', backref='quizzes')
    questions = db.relationship('Question', backref='quiz', cascade='all, delete-orphan')
    responses = db.relationship('QuizResponse', backref='quiz', cascade='all, delete-orphan')

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class QuizResponse(db.Model):
    __tablename__ = 'quiz_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Float)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('User', backref='quiz_responses')
