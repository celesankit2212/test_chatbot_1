from flask import Flask, render_template, request
from openai_integration import generate_test_script

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    script = ""
    if request.method == "POST":
        test_description = request.form.get("test_description")
        if test_description:
            script = generate_test_script(test_description)
    return render_template("index.html", script=script)


if __name__ == "__main__":
    app.run(debug=True)
