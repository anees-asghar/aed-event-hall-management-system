import sqlite3

conn = sqlite3.connect("test.db")


cursor = conn.cursor()

# # create users table
cursor.execute(
    """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            password TEXT
        );
    """
)

# create reservations table 
cursor.execute(
    """
        CREATE TABLE reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT,
            date TEXT,
            seat_number TEXT
        );
    """
)

conn.commit()


conn.close()