import sqlite3

conn = sqlite3.connect("reservation_system.db")


cursor = conn.cursor()

# # create users table
cursor.execute(
    """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    """
)

# create reservations table 
cursor.execute(
    """
        CREATE TABLE reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INT NOT NULL,
            date TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            UNIQUE(date, seat_number),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """
)

cursor.execute(
    """
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL UNIQUE
        );
    """
)

conn.commit()


conn.close()