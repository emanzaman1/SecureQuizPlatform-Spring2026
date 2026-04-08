from flask import Flask, request, render_template_string

app = Flask(__name__)

# Simple homepage
@app.route("/")
def home():
    return "<h1>Welcome to SecureQuizPlatform!</h1>"

# Example quiz result page
@app.route("/result/<int:quiz_id>")
def result(quiz_id):
    return f"<h2>Result for Quiz ID: {quiz_id}</h2>"

if __name__ == "__main__":
    app.run(debug=True)