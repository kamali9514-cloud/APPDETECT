from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)

# 🔐 VERY IMPORTANT (Fixes session error)
app.secret_key = "super_secret_key_123456"

# ==============================
# DATABASE INITIALIZATION
# ==============================

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Table for history
    c.execute('''
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appname TEXT,
            result TEXT,
            date TEXT
        )
    ''')

    # Table for safe apps list
    c.execute('''
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    # Insert default safe apps (only if not exists)
    try:
        c.execute("INSERT INTO apps (name) VALUES (?)", ("whatsapp",))
        c.execute("INSERT INTO apps (name) VALUES (?)", ("instagram",))
        c.execute("INSERT INTO apps (name) VALUES (?)", ("facebook",))
    except:
        pass

    conn.commit()
    conn.close()


# ==============================
# DATABASE CONNECTION FUNCTION
# ==============================

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# ==============================
# ROUTES
# ==============================

# 🏠 Home
@app.route("/")
def home():
    return render_template("index.html")


# 🔐 Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email and password:
            session["user"] = email
            flash("Login Successful")
            return redirect(url_for("check_app"))

    return render_template("login.html")


# 🚪 Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


# 🧪 Check Page
@app.route("/check_app")
def check_app():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("check.html")


# 🔎 Check Logic
@app.route("/check", methods=["POST"])
def check():

    if "user" not in session:
        return redirect(url_for("login"))

    appname = request.form["appname"]

    conn = get_db_connection()
    app_data = conn.execute(
        "SELECT * FROM apps WHERE name = ?",
        (appname.lower(),)
    ).fetchone()
    conn.close()

    if app_data:
        result = "Safe Application ✅"
    else:
        result = "Suspicious Application ⚠️"

    # Save to history
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO checks (appname, result, date) VALUES (?, ?, ?)",
        (appname, result, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

    return render_template("result.html", appname=appname, result=result)


# 📜 History Page
@app.route("/history")
def history():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM checks ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    return render_template("history.html", data=data)
# ℹ About
@app.route("/about")
def about():
    return render_template("about.html")


# 🛠 Service
@app.route("/service")
def service():
    return render_template("service.html")


# ==============================
# RUN APP
# ==============================

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
