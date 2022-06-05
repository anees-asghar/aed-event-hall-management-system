import sqlite3

class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    # User table functions

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

    # Reservation table functions

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

    def insert_reservations(self, user_id, date, seat_nums):
        for seat_num in seat_nums:
            self.cursor.execute(
                "INSERT INTO reservations (user_id, date, seat_number) VALUES (:user_id, :date, :seat_number)",
                {
                    "user_id": user_id,
                    "date": date,
                    "seat_number": seat_num
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
    
    # Authentication functions
    def register_user(self, first_name, last_name, email, password):
        self.cursor.execute("SELECT * FROM users WHERE email = :email;", {"email": email})
        user = self.cursor.fetchone()
        
        if user: return False # user with this email already exists

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
        
        return True

    def authenticate_user(self, email, password):
        self.cursor.execute(
            "SELECT * FROM users WHERE email = :email AND password = :password;", 
            {"email": email ,"password": password}
        )
        user = self.cursor.fetchone()
        
        if user: return user[0] # return user id
        else: return None


    # def valid_credentials(self, email, password):
    #     self.cursor.execute(
    #         "SELECT * FROM users WHERE email = :email AND password = :password;", 
    #         {"email": email ,"password": password}
    #     )
    #     user = self.cursor.fetchone()
        
    #     if user: return True
    #     else: return False

    def close(self):
        self.conn.close()