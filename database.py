import sqlite3

class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()

    def insert_reservations(self, user_id, date, seat_nums):
        """
            Insert reservations in the reservation table for the 
            specified seat numbers, date and user.
        """
        for seat_num in seat_nums: # make reservation for each seat in the set
            self.cursor.execute(
                "INSERT INTO reservations (user_id, date, seat_number) VALUES (:user_id, :date, :seat_number)",
                {
                    "user_id": user_id,
                    "date": date,
                    "seat_number": seat_num
                }
            )
        self.conn.commit() # commit database changes

    def select_reservations_by_date(self, date):
        """
            Select and return the reservations of a specified date from the reservations table.
        """
        self.cursor.execute(
            "SELECT * FROM reservations WHERE date = :date;", {"date": date}
        )
        reservations = self.cursor.fetchall()
        return reservations

    def select_user_by_email(self, email):
        """
            Select and return the user with this email from users table.
        """
        self.cursor.execute("SELECT * FROM users WHERE email = :email;", {"email": email})
        user = self.cursor.fetchone()
        return user

    def select_user_by_email_password(self, email, password):
        """
            Select and return the user with this email and password from users table.
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE email = :email AND password = :password;", 
            {"email": email ,"password": password}
        )
        user = self.cursor.fetchone()
        return user

    def insert_user(self, first_name, last_name, email, password):
        """ Insert a new user into users table. """
        self.cursor.execute(
            "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)",
            {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password
            }
        )
        self.conn.commit() # commit changes

    def close(self):
        """ Close the database connection. """
        self.conn.close()
