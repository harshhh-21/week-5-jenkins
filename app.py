from flask import Flask, jsonify
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "v1")


@app.route("/")
def home():
    return f"""
    <html>
        <head>
            <title>Week 9 CI/CD Application</title>
        </head>
        <body>
            <h1>DevOps CI/CD Demo</h1>
            <h2>Application Version: {APP_VERSION}</h2>
            <p>Application deployed using Jenkins.</p>
            <p>Docker + Jenkins + GitHub</p>
        </body>
    </html>
    """


@app.route("/health")
def health():
    if os.getenv("FAIL_HEALTH") == "true":
        return jsonify({
            "status": "failed",
            "version": APP_VERSION
        }), 500

    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    }), 200


def add(a, b):
    return a + b


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
