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