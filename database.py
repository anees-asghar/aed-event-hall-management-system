import tkinter as tk
import tkcalendar as tkcal
import sqlite3
import view as v

#DOUBTS AND QUESTIONS




# --- ROOT WINDOW ---
root = tk.Tk()
root.geometry("1400x800")
root.resizable(False, False)
root.title("Reservation System")

#SQLIETE HAS 5 data types:text, intergers, real, noul, blob

#Create a database or connect to one
conn = sqlite3.connect("users_book.db")

#Create cursor
#A cursor can be viewed as a pointer to one row in a set of rows. The cursor can only reference one row at a time, but can move to other rows of the result set as needed.
c = conn.cursor()

#Create table

# c.execute("""USERS INFORMATION adresses 
#                 (first_name text,last_name text,email text,password text)""")
        
      
#Submit function for database
def submit():
        conn = sqlite3.connect("users_book.db")
        c = conn.cursor()

        #Insert into table
        c.execute("INSERT TO adresses VALUES(:name, :last_name, :email, :password)",
        {
                "first_name" : v.name.get(), 
                "last_name" : v.last_name.get(),
                "email" : v.email.get(),
                "password" : v.password.get()            
        })
                
        #Commit Changes 
        conn.commit()

        #Close Connection 
        conn.close()

        
        

#Commit Changes 
conn.commit()

#Close Connection 
conn.close()

root.mainloop()