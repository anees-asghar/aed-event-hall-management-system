import sqlite3

conn = sqlite3.connect("reservation_system.db")


cursor = conn.cursor()

cursor.execute(
    """
        CREATE TABLE seat_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL UNIQUE,
            cost INT NOT NULL
        );
    """
)

cursor.execute(
    """
        CREATE TABLE seats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seat_number TEXT NOT NULL UNIQUE,
            seat_type TEXT NOT NULL, 
            FOREIGN KEY(seat_type) REFERENCES seat_types(type)
        );
    """
)

cursor.execute(
    "INSERT INTO seat_types (type, cost) VALUES (?, ?), (?, ?);",
    ['Normal', 4, 'VIP', 12]
)

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
            [seat_num, 'VIP']
        )
    else:
        cursor.execute(
            "INSERT INTO seats (seat_number, seat_type) VALUES (?, ?)",
            [seat_num, 'Normal']
        )

conn.commit()

conn.close()
