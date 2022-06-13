import sys
import sqlite3

if len(sys.argv) != 5:
    print("Invalid syntax.")
    print("Usage -> python create_admin.py <first_name> <last_name> <email> <password>")
    sys.exit()

conn = sqlite3.connect("test2.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO users (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?);",
    [sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], "Admin"]
)

conn.commit()
conn.close()