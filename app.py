from flask import Flask, render_template, request, redirect, session
import mysql.connector
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit

app = Flask(__name__)
app.secret_key = "attendance_secret"

# -------------------------
# DATABASE CONNECTION
# -------------------------

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="",
        password="",
        database="faculty_attendance"
    )

db = get_db()
cursor = db.cursor(buffered=True)


# -------------------------
# AUTO ABSENT FUNCTION
# -------------------------

def mark_absent_automatically():
    """
    Runs every day at 15:00 (3 PM).
    Any faculty who has no attendance record for today gets marked as 'Absent'.
    """
    try:
        conn = get_db()
        cur = conn.cursor(buffered=True)

        today = datetime.now().strftime("%Y-%m-%d")

        # Get all faculty usernames
        cur.execute("SELECT username FROM users WHERE role='faculty'")
        all_faculty = cur.fetchall()

        for (faculty_name,) in all_faculty:
            # Check if attendance already exists for today
            cur.execute(
                "SELECT * FROM attendance WHERE name=%s AND date=%s",
                (faculty_name, today)
            )
            record = cur.fetchone()

            if not record:
                # No attendance found -> mark Absent
                cur.execute(
                    """
                    INSERT INTO attendance (name, date, time_in, time_out, status)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (faculty_name, today, None, None, "Absent")
                )
                print(f"Absent auto-marked: {faculty_name} on {today}")

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"[Auto-Absent Error] {e}")


# -------------------------
# SCHEDULER - Runs daily at 3 PM
# -------------------------

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=mark_absent_automatically,
    trigger="cron",
    hour=15,
    minute=0,
    id="auto_absent_job",
    replace_existing=True
)
scheduler.start()

# Shut down scheduler gracefully when app exits
atexit.register(lambda: scheduler.shutdown())


# -------------------------
# HOME
# -------------------------

@app.route("/")
def home():
    return redirect("/login")


# -------------------------
# LOGIN SYSTEM
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()

        if user:

            session["username"] = username
            role = user[3]

            if role == "admin":
                return redirect("/admin_dashboard")

            else:
                return redirect("/faculty_dashboard/"+username)

        else:
            return "Invalid login"

    return render_template("auth/login.html")


# -------------------------
# ADMIN DASHBOARD
# -------------------------

@app.route("/admin_dashboard")
def admin_dashboard():

    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT username FROM users WHERE role='faculty'")
    faculty = cursor.fetchall()

    return render_template("admin/admin_dashboard.html", faculty=faculty)

# -------------------------
# REGISTER FACULTY
# -------------------------

@app.route("/register_faculty", methods=["GET", "POST"])
def register_faculty():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        query = "INSERT INTO users (username,password,role) VALUES (%s,%s,%s)"
        values = (username, password, "faculty")

        cursor.execute(query, values)
        db.commit()

        return redirect("/capture_face/" + username)

    return render_template("admin/register_faculty.html")


# -------------------------
# FACE CAPTURE
# -------------------------

@app.route("/capture_face/<username>")
def capture_face(username):

    subprocess.call([
        "python",
        "face_recognition_module/capture_faces.py",
        username
    ])

    return redirect("/admin_dashboard")


# -------------------------
# FACULTY DASHBOARD
# -------------------------

@app.route("/faculty_dashboard/<username>")
def faculty_dashboard(username):
    name = username
    return render_template("faculty/faculty_dashboard.html", name=name)


# -------------------------
# CAMERA ATTENDANCE
# -------------------------

@app.route("/camera_attendance/<username>")
def camera_attendance(username):

    subprocess.call([
        "python",
        "face_recognition_module/recognize_face.py",
        username
    ])

    return redirect("/faculty_dashboard/"+username)


# -------------------------
# MANUAL TRIGGER (Admin) - Force run absent check immediately
# -------------------------

@app.route("/trigger_absent_check")
def trigger_absent_check():
    if session.get("username"):
        mark_absent_automatically()
        return redirect("/admin_dashboard")
    return redirect("/login")


# -------------------------
# ANALYTICS PAGE
# -------------------------

@app.route("/analytics")
def analytics():

    cursor = db.cursor()
    cursor.execute("SELECT name, status FROM attendance")
    data = cursor.fetchall()

    present = {}
    late = {}
    half = {}
    absent = {}

    for name, status in data:
        if status == "Present":
            present[name] = present.get(name, 0) + 1

        elif status == "Late":
            late[name] = late.get(name, 0) + 1

        elif status == "Half-Day":
            half[name] = half.get(name, 0) + 1

        elif status == "Absent":
            absent[name] = absent.get(name, 0) + 1

    return render_template("analytics/graph.html",
                           present=present,
                           late=late,
                           half=half,
                           absent=absent)


# -------------------------
# LOGOUT
# -------------------------

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


# -------------------------
# RUN SERVER
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
