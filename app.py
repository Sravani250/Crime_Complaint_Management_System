from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "crime_secret_key"

def get_db():
    return sqlite3.connect("database.db")

# ----------------- LOGIN -----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role=?",
            (username, password, role)
        )
        user = cur.fetchone()

        if user:
            session["username"] = username
            session["role"] = role
            if role == "admin":
                return redirect("/admin")
            else:
                return redirect("/complaint")
        else:
            return "Invalid Login Credentials"

    return render_template("login.html")

# ----------------- COMPLAINT -----------------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if request.method == "POST":
        title = request.form["title"]
        category = request.form["category"]
        description = request.form["description"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO complaints (title, category, description) VALUES (?,?,?)",
            (title, category, description)
        )
        db.commit()

        return "Complaint Registered Successfully"

    return render_template("complaint.html")

# ----------------- ADMIN -----------------
@app.route("/admin")
def admin():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM complaints")
    complaints = cur.fetchall()
    return render_template("admin.html", complaints=complaints)

# ----------------- LOGOUT -----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
