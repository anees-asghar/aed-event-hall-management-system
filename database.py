import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def insert_user(self, first_name, last_name, email, password):
        self.cursor.execute(
            "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)",
            {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password
            }
        )
        self.conn.commit()

    def fetch_users(self):
        self.cursor.execute("SELECT * FROM users;")
        users = self.cursor.fetchall()
        return users

    def insert_reservation(self, user_id, date, seat_number):
        self.cursor.execute(
            "INSERT INTO reservations (user_id, date, seat_number) VALUES (:user_id, :date, :seat_number)",
            {
                "user_id": user_id,
                "date": date,
                "seat_number": seat_number
            }
        )
        self.conn.commit()

    def fetch_reservations(self):
        self.cursor.execute("SELECT * FROM reservations;")
        reservations = self.cursor.fetchall()
        return reservations
    
    def fetch_reservations_by_date(self, date):
        self.cursor.execute(
            "SELECT * FROM reservations WHERE date = :date;", {"date": date}
        )
        reservations = self.cursor.fetchall()
        return reservations
    
    def close(self):
        self.conn.close()