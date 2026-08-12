import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Varun@123",
    database="faculty_attendance"
)

print("Database Connected Successfully")
