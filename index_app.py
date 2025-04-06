from flask import Flask, render_template, request, session, redirect, url_for, flash
from test_executor import run_test
from integration_model import generate_test_script
from database import save_test_result, get_test_history

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Use a secure random key in production

@app.route("/", methods=["GET", "POST"])
def index():
    # Placeholder values
    script = ""
    test_result = ""
    history = get_test_history()

    if request.method == "POST":
        test_description = request.form.get("test_description")
        if test_description:
            # Step 1: Generate test script using AI model
            script, credit_used = generate_test_script(test_description)

            # Step 2: Save generated script to file
            if script:
                with open("tests/generated_test.py", "w") as f:
                    f.write(f"# AI-Generated Selenium Test Script\n# Description: {test_description}\n\n")
                    f.write(script)

            # Step 3: Execute the test and capture results
            test_result = run_test()

            # Simulate consumed credits
            credits_consumed = credit_used # Replace with actual OpenAI usage if available

            save_test_result(test_description, test_result, credits_consumed)
            print(test_description, test_result, credits_consumed)

    return render_template(
        "index_app.html",
        script=script,
        test_result=test_result,
        history=history
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html", error=str(e)), 500

if __name__ == "__main__":
    app.run(debug=True)
