# app.py
import time

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, init_db, save_test_result, get_test_history, User
from database import db, TestResult
import threading
from test_executor import run_test


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# # Prompt for admin credentials during initial setup
# admin_email = input("Enter email for primary admin: ")
# admin_password = getpass.getpass("Enter password for primary admin: ")
#
# Initialize and setup the database
# init_db(app, admin_email, admin_password)
init_db(app)
# -------------------- AUTH ROUTES --------------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# --------------------- MAIN PAGE ---------------------

# def execute_and_save_test(test_description, user_id):
#     from test_executor import run_test
#     result = run_test()
#     credits_used = len(test_description) / 100.0
#     save_test_result(description=test_description, result=result, credits=credits_used, user_id=user_id)

def execute_and_update(result_id):
    print("----Updating Test Result on DB after execution-----")
    time.sleep(5)
    result = run_test()
    print(f"---Test executed and Result is, {result}")
    with app.app_context():
        record = TestResult.query.get(result_id)
        print(record)
        if record:
            record.result = result
            db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    from test_executor import run_test
    from integration_model import generate_test_script

    script = ""
    test_result = ""
    user_id = session['user_id']
    username = session['username']
    role = session['role']

    if request.method == 'POST':
        # Create DB entry first with Not_Executed
        test_result = "Not_Executed"


        test_description = request.form.get("test_description")
        execute_test = request.form.get("execute_test") == "yes"


        script, credit_used = generate_test_script(test_description)

        if script:
            with open("tests/test_generated.py", "w") as f:
                f.write("# AI-Generated Test for: " + test_description + "\n")
                f.write(script)

        # Insert placeholder in DB first
        placeholder = TestResult(description=test_description, result="Not_Executed", credits=credit_used,
                                    user_id=user_id)
        db.session.add(placeholder)
        db.session.commit()

        if execute_test:
            threading.Thread(target=execute_and_update, args=(placeholder.id,)).start()
            test_result = "Test is being executed in background..."

        save_test_result(description=test_description, result=test_result, credits=credit_used, user_id=user_id)

    history = []
    if role == 'admin':
        history = get_test_history(role)
    return render_template("index.html", script=script, test_result=test_result, history=history, username=username, role=role)

# -------------------- RUN APP --------------------

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
