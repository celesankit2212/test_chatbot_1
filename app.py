 
from flask import Flask, render_template, request
# from transformers_integration import generate_test_script
from get_openai_prompts import open_gpt_and_get_prompt_output
from test_executor import run_test

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    script = ""
    test_result = ""
    if request.method == "POST":
        test_description = request.form.get("test_description")
        if test_description:
            # script = generate_test_script(test_description)
            script = open_gpt_and_get_prompt_output(test_description)
            with open("tests/generated_test.py", "w") as f:
                f.write(script)
            test_result = run_test()
    return render_template("index.html", script=script, test_result=test_result)

if __name__ == "__main__":
    app.run(debug=True)

#login-button
##email-input
