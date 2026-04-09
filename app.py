<<<<<<< HEAD
<<<<<<< HEAD
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

=======
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to SecureQuizPlatform!"

@app.route('/result/<int:id>')
def result(id):
    return f"Result page for ID {id}"

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> main
