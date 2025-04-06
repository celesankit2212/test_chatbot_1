from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

# Flask app setup for SQLAlchemy (for use during migrations/scripts)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy()

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    credits_consumed = db.Column(db.Float, nullable=True)  # Add this line
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TestResult {self.description[:50]}...>"


# ------------------------
# DB Utility Functions
# ------------------------

def save_test_result(description, result, credits_consumed=None):
    new_result = TestResult(
        description=description,
        result=result,
        credits_consumed=credits_consumed  # Pass value when available
    )
    db.session.add(new_result)
    db.session.commit()

def get_test_history():
    results = TestResult.query.order_by(TestResult.timestamp.desc()).all()
    return [(result.result, result.credits_consumed) for result in results]


# ------------------------
# Manual Table Creation (optional if using Flask-Migrate)
# ------------------------

def initialize_database():
    with app.app_context():
        db.create_all()
        print("Database initialized.")


# Only run when executing this file directly
if __name__ == "__main__":
    initialize_database()
