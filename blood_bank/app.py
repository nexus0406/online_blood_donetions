from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS donors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, blood_group TEXT, email TEXT, phone TEXT, city TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, blood_group TEXT, email TEXT, phone TEXT, city TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, subject TEXT, message TEXT)")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = (
            request.form["name"],
            request.form["blood_group"],
            request.form["email"],
            request.form["phone"],
            request.form["city"]
        )
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO donors (name, blood_group, email, phone, city) VALUES (?, ?, ?, ?, ?)", data)
        donor_id = c.lastrowid  # 🔁 Add this line
        conn.commit()
        conn.close()
        return redirect(f"/profile/{donor_id}")  # 🔁 Replace thankyou with profile redirect
    return render_template("register.html")

@app.route("/request", methods=["GET", "POST"])
def blood_request():
    if request.method == "POST":
        data = (
            request.form["name"],
            request.form["blood_group"],
            request.form["email"],
            request.form["phone"],
            request.form["city"]
        )
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO requests (name, blood_group, email, phone, city) VALUES (?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
        return render_template("thankyou.html", message="Blood request submitted successfully.")
    return render_template("request.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = (
        request.form["contactName"],
        request.form["contactEmail"],
        request.form["contactSubject"],
        request.form["contactMessage"]
    )
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, email, subject, message) VALUES (?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    return render_template("thankyou.html", message="Your message has been received.")

@app.route("/admin")
def admin():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM donors")
    donors = c.fetchall()
    c.execute("SELECT * FROM requests")
    requests_data = c.fetchall()
    c.execute("SELECT * FROM contacts")
    contacts = c.fetchall()
    conn.close()
    return render_template("admin.html", donors=donors, requests=requests_data, contacts=contacts)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
@app.route("/profile/<int:donor_id>")
def view_profile(donor_id):
    ...
@app.route("/profile/<int:donor_id>")
def view_profile(donor_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM donors WHERE id = ?", (donor_id,))
    donor = c.fetchone()
    conn.close()
    if donor:
        return render_template("profile.html", donor=donor)
    else:
        return "Profile not found", 404
from flask import Flask, render_template, request, redirect, url_for, session

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Check if the credentials are correct
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True  # Create a session to remember the admin
            return redirect("/admin_dashboard")
        else:
            return "Invalid credentials, please try again.", 401
    
    return render_template("admin_login.html")
@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect("/admin")
    
    # Fetch donors and requests from the database
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM donors")
    donors = c.fetchall()
    c.execute("SELECT * FROM requests")
    requests = c.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", donors=donors, requests=requests)
