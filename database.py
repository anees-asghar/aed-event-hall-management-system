import sqlite3


class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()


    def insert_reservations(self, user_id, date, seat_nums):
        """
            Insert reservations in the database reservation table for the 
            specified seat numbers and date for the logged in user.
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
    

    def fetch_reservations_by_date(self, date):
        """
            Fetch and return the reservations of a specified date from the database.
        """
        self.cursor.execute(
            "SELECT * FROM reservations WHERE date = :date;", {"date": date}
        )
        reservations = self.cursor.fetchall()
        return reservations

    def select_user_by_email(self, email):
        """
            Return from database the user with the specified email.
            Return None if no such user exists.
        """
        self.cursor.execute("SELECT * FROM users WHERE email = :email;", {"email": email})
        user = self.cursor.fetchone()
        
        if user: return user
        else: return None
    

    def insert_user(self, first_name, last_name, email, password):
        """
            Register a new user.
            Return True if registered successfully, False if user with the 
            specified email already exists.
        """
        # return false if user with this email already exists
        self.cursor.execute("SELECT * FROM users WHERE email = :email;", {"email": email})
        user = self.cursor.fetchone()
        if user: return False

        # insert new user into database users table
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
        
        return True # registration was a success


    def authenticate_user(self, email, password):
        """
            Check if a user with this email and password exists.
        """
        self.cursor.execute(
            "SELECT * FROM users WHERE email = :email AND password = :password;", 
            {"email": email ,"password": password}
        )
        user = self.cursor.fetchone()
        
        if user: return user[0] # if such a user exists, return their user_id
        else: return None # if not return None


    def close(self):
        """ Close the database connection. """
        self.conn.close()
