from flask import Flask, session, request, render_template, url_for, redirect
from concurrent.futures import ThreadPoolExecutor
from test_executor import run_test
from integration_model import generate_test_script

app = Flask(__name__)

# Secret key for session management (Required by Flask sessions)
app.secret_key = 'abcd1234@#'

# Executor for running long tasks in the background
executor = ThreadPoolExecutor(max_workers=2)


def generate_and_run_test_in_background(test_description):
    script = generate_test_script(test_description)

    # Save generated script to file
    if script:
        with open("tests/gen_test.py", "w") as f:
            f.write("# AI-Generated Selenium Test Script for: " + test_description + "\n")
            f.write(script)

    # Run the test and capture the result
    test_result = run_test()

    # Save the test result to the database or storage
    # save_test_result(test_description, test_result)

    # Store results in the session
    session['script'] = script
    session['test_result'] = test_result

    return script, test_result


@app.route("/", methods=["GET", "POST"])
def index():
    script = session.get('script', "")
    test_result = session.get('test_result', "")
    # history = get_test_history()  # Fetch history from the database

    if request.method == "POST":
        test_description = request.form.get("test_description")
        if test_description:
            # Run the generated and test functions in the background
            future = executor.submit(generate_and_run_test_in_background, test_description)
            # Wait for the task to complete and get results
            future.result()  # Ensure the background task completes

            # Redirect to the same page to avoid re-submission if the user refreshes the page
            return redirect(url_for("index"))

    return render_template("index.html", script=script, test_result=test_result)


if __name__ == "__main__":
    app.run(debug=True)
