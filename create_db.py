import sqlite3
import datetime
import random
from os.path import exists


def create_db(db_name):
    # return if db already exists
    if exists(db_name): return 

    # connect to database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # create roles table
    cursor.execute(
        """
            CREATE TABLE roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL
            );
        """
    )

    # create users table
    cursor.execute(
        """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'App User' NOT NULL,
                FOREIGN KEY(role) REFERENCES roles(role)
            );
        """
    )

    # create events table 
    cursor.execute(
        """
            CREATE TABLE events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL
            );
        """
    )

    # create seat_types table 
    cursor.execute(
        """
            CREATE TABLE seat_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                value INT NOT NULL
            );
        """
    )

    # create seats table 
    cursor.execute(
        """
            CREATE TABLE seats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seat_number TEXT NOT NULL,
                seat_type TEXT NOT NULL,
                FOREIGN KEY(seat_type) REFERENCES seat_types(type)
            );
        """
    )

    # create reservations table 
    cursor.execute(
        """
            CREATE TABLE reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INT NOT NULL,
                event_id INT NOT NULL,
                seat_number TEXT NOT NULL,
                UNIQUE(event_id, seat_number),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(event_id) REFERENCES events(id),
                FOREIGN KEY(seat_number) REFERENCES seats(seat_number)
            );
        """
    )

    # populate the roles table
    cursor.execute(
        "INSERT INTO roles (role) VALUES (?), (?);",
        ["Admin", "App User"]
    )

    # populate the seat_types table
    cursor.execute(
        "INSERT INTO seat_types (type, value) VALUES (?, ?), (?, ?);",
        ["Normal", 4, "VIP", 12]
    )

    # populate the seats table
    valid_seat_nums = []
    vip_seats = ["6F", "7F", "8F", "9F", "6A", "7A", "8A", "9A"]
    invalid_seat_nums = ['3F','4F','5F','10F','11F','12F','3A','4A','5A','10A','11A','12A']

    cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12','13','14']
    rows = ['K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

    for c in cols:
        for r in rows:
            seat_num = c + r
            if seat_num not in invalid_seat_nums:
                valid_seat_nums.append(seat_num)

    for seat_num in valid_seat_nums:
        if seat_num in vip_seats:
            cursor.execute(
                "INSERT INTO seats (seat_number, seat_type) VALUES (?, ?)",
                [seat_num, "VIP"]
            )
        else:
            cursor.execute(
                "INSERT INTO seats (seat_number, seat_type) VALUES (?, ?)",
                [seat_num, "Normal"]
            )

    # populate the events table
    events = [
        "Medea - Euripides",
        "Macbeth - William Shakespeare",
        "Life is a Dream",
        "The Importance of Being Earnest", 
        "Trifles - Susan Glaspell",
        "Chicago - Maurine Dallas Watkins",
        "Machinal - Sophie Treadwell",
        "Death of a Salesman - Arthur Miller"
    ]
    for year in [2022, 2023]:
        for month in [m for m in range(1, 12+1)]:
            for day in [d for d in range(1, 31+1)]:
                try:
                    datetime.datetime(year, month, day) # if not a valid date, an error will be raised
                    
                    day_str = str(day) if day >= 10 else '0'+str(day)         # date format dd
                    month_str = str(month) if month >= 10 else '0'+str(month) # moth format mm
                    year_str = str(year)[-2:]                                 # year format yy

                    cursor.execute(
                        "INSERT INTO events (name, date) VALUES (?, ?);",
                        [random.choice(events), f'{day_str}/{month_str}/{year_str}']
                    )
                except:
                    continue

    # create admin user
    cursor.execute(
        "INSERT INTO users (first_name, last_name, email, password, role) VALUES (?, ?, ?, ?, ?);",
        ['admin', 'admin', 'admin', 'admin', "Admin"]
    )

    conn.commit() # commit changes
    conn.close()  # close db connection
