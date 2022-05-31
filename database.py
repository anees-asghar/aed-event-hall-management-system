import sqlite3

conn = sqlite3.connect("test.db")

cursor = conn.cursor()

# cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)",
#     {
#         'first_name': 'Anees',
#         'last_name': 'Asghar',
#         'email': 'a@b.com',
#         'password': '12345'
#     }
# )

conn.commit()

conn.close()