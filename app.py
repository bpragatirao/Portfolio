from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table
conn = get_db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
)
""")
conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["first_name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )
        conn.commit()
        conn.close()

        return redirect("/contact")

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
