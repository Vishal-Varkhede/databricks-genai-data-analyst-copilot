import os

from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "ok",
        "service": "genai-data-analyst-copilot"
    })


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "DATABRICKS_APP_PORT",
            "8000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
