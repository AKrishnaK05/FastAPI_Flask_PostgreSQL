import os

import requests
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change_me")

API_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000/api/v1")


def call_api(method: str, endpoint: str, payload: dict | None = None) -> tuple[dict | None, str | None, int]:
    """Execute HTTP request to backend API with simple error handling."""

    url = f"{API_BASE_URL}{endpoint}"
    try:
        response = requests.request(method=method, url=url, json=payload, timeout=10)
        if response.headers.get("content-type", "").startswith("application/json"):
            data = response.json()
        else:
            data = None

        if response.status_code >= 400:
            detail = "Request failed"
            if isinstance(data, dict):
                detail = str(data.get("detail", detail))
            return None, detail, response.status_code

        return data, None, response.status_code
    except requests.RequestException:
        return None, "Backend service unavailable", 503


@app.route("/")
def home():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        payload = {
            "email": request.form.get("email", "").strip(),
            "full_name": request.form.get("full_name", "").strip(),
            "password": request.form.get("password", ""),
        }
        data, error, status_code = call_api("POST", "/users/", payload)
        if error:
            flash(f"Registration failed: {error}", "error")
            return render_template("register.html"), status_code

        flash(f"User created: {data['email']}. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        payload = {
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", ""),
        }
        data, error, status_code = call_api("POST", "/auth/token", payload)
        if error:
            flash(f"Login failed: {error}", "error")
            return render_template("login.html"), status_code

        session["token"] = data["access_token"]
        session["user"] = data["user"]
        flash("Login successful", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    token = session.get("token")
    if not user or not token:
        flash("Please login first.", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Logged out", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
