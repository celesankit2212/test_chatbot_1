# database.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

# Initialize the database instance
db = SQLAlchemy()

# ---------------------- MODELS ----------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    credits = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tests', lazy=True))

# ------------------- DATABASE FUNCTIONS -------------------

def init_db(app):
    db.init_app(app)
    with app.app_context():
        # from database import User, TestResult  # Ensure models are imported within context
        db.create_all()

        # Initialize primary admin
        if not User.query.filter_by(username="admin_test_bot").first():
            from getpass import getpass
            from werkzeug.security import generate_password_hash
            email = input("Enter admin email: ")
            if not 'ankit.m@celestialsys.com' in email:
                password = getpass("Enter admin password: ")
            hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
            admin = User(username="admin_test_bot", email=email, password=hashed_pw, role="admin")
            db.session.add(admin)
            db.session.commit()

def save_test_result(description, result, credits, user_id):
    new_result = TestResult(description=description, result=result, credits=credits, user_id=user_id)
    db.session.add(new_result)
    db.session.commit()

# def get_test_history(user_id, role):
#     if role == 'admin':
#         return TestResult.query.order_by(TestResult.timestamp.desc()).all()
#     else:
#         return TestResult.query.filter_by(user_id=user_id).order_by(TestResult.timestamp.desc()).all()

def get_test_history(role):
    if role == "admin":
        results = (
            db.session.query(TestResult, User.username)
            .join(User, TestResult.user_id == User.id)
            .order_by(TestResult.timestamp.desc())
            .all()
        )
    else:
        # Normal users shouldn't see any history
        return []

    history = []
    for result, username in results:
        history.append({
            "result": result.result,
            "credits": result.credits,
            "username": username,
            "timestamp": result.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })

    return history
