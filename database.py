import sqlite3


class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name) # connect to db
        self.cursor = self.conn.cursor()           # create db cursor


    def get_event_by_date(self, date):
        """
            Select the event on the specified date.
        """
        self.cursor.execute(
            "SELECT * FROM events WHERE date = ?;", [date] 
        )
        event = self.cursor.fetchone()
        return event


    def insert_reservations(self, user_id, event_id, seat_nums):
        """
            Insert reservations in the reservations table for the 
            specified seat numbers, event and user.
        """
        for seat_num in seat_nums: # make reservation for each seat in the set
            self.cursor.execute(
                "INSERT INTO reservations (user_id, event_id, seat_number) VALUES (?, ?, ?);",
                [user_id, event_id, seat_num]
            )
        self.conn.commit() # commit database changes


    def select_reservations_by_event_id(self, event_id):
        """
            Select all reservations for a particular event.
        """
        self.cursor.execute(
            "SELECT * FROM reservations WHERE event_id = ?;",
            [event_id]
        )
        reservations = self.cursor.fetchall()
        return reservations


    def select_reservations_by_day(self, day, month, year):
        """ Select reservations at a given date. """
        self.cursor.execute(
            """
                SELECT r.id, st.type, st.value FROM reservations r
                JOIN events e
                ON r.event_id = e.id
                JOIN seats s
                ON r.seat_number = s.seat_number
                JOIN seat_types st
                ON s.seat_type = st.type
                WHERE date = ?;
            """,
            [f"{day}/{month}/{year}"]
        )
        reservations = self.cursor.fetchall()
        return reservations


    def select_reservations_by_month(self, month, year):
        """ Select reservations at a month and year. """
        self.cursor.execute(
            """
                SELECT r.id, st.type, st.value FROM reservations r
                JOIN events e
                ON r.event_id = e.id
                JOIN seats s
                ON r.seat_number = s.seat_number
                JOIN seat_types st
                ON s.seat_type = st.type
                WHERE date LIKE ?;
            """,
            [f"%/{month}/{year}"]
        )
        reservations = self.cursor.fetchall()
        return reservations


    def select_reservations_by_year(self, year):
        """ Select reservations for the specified year. """
        self.cursor.execute(
            """
                SELECT r.id, st.type, st.value FROM reservations r
                JOIN events e
                ON r.event_id = e.id
                JOIN seats s
                ON r.seat_number = s.seat_number
                JOIN seat_types st
                ON s.seat_type = st.type
                WHERE date LIKE ?;
            """,
            [f"%/{year}"]
        )
        reservations = self.cursor.fetchall()
        return reservations


    def select_seats_by_type(self, type):
        """ Select seats by type from seats table. """
        self.cursor.execute(
            "SELECT * FROM seats WHERE seat_type = ?;", [type] 
        )
        seats = self.cursor.fetchall()
        return seats


    def select_all_seats(self):
        """ Select all seats from seats table. """
        self.cursor.execute("SELECT * FROM seats;")
        seats = self.cursor.fetchall()
        return seats


    def delete_reservation(self, event_id, seat_num):
        """
            Delete reservation for the given event and seat number from 
            the reservations table.
        """
        self.cursor.execute(
            "DELETE FROM reservations WHERE event_id = ? AND seat_number = ?;", 
            [event_id, seat_num]
        )
        self.conn.commit()
    

    def update_reservation(self, event_id, old_seat_num, new_seat_num):
        """
            Update the reservation of a specified event and seat number to have 
            the new seat number.
        """
        self.cursor.execute(
            "UPDATE reservations SET seat_number = ? WHERE seat_number = ? AND event_id = ?;",
            [new_seat_num, old_seat_num, event_id]
        )
        self.conn.commit()


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
