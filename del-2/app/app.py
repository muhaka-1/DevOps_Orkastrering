from flask import Flask, jsonify, render_template
import os
import socket
import time
import random

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "v1")
POD_NAME = socket.gethostname()
START_TIME = time.time()

# Per-pod in-memory request counter.
# This is intentionally local to each pod so students can see that
# different replicas have separate process memory.
REQUEST_COUNT = 0


def pod_info():
    global REQUEST_COUNT
    REQUEST_COUNT += 1

    return {
        "service": "JensenStore API",
        "version": VERSION,
        "pod": POD_NAME,
        "request_count": REQUEST_COUNT,
        "uptime_seconds": int(time.time() - START_TIME),
        "status": "running",
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/info")
def api_info():
    return jsonify(pod_info())


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "version": VERSION,
        "pod": POD_NAME,
    })


@app.get("/products")
def products():
    return jsonify([
        {"id": 1, "name": "Laptop", "price": 12990},
        {"id": 2, "name": "Monitor", "price": 2990},
        {"id": 3, "name": "Keyboard", "price": 799},
    ])


if __name__ == "__main__":
    print(f"Starting JensenStore API {VERSION} on pod {POD_NAME}")
    app.run(host="0.0.0.0", port=5000)
