

import tkinter as tk
import tkcalendar as tkcal


# --- ROOT WINDOW ---
root = tk.Tk()
root.geometry("1400x800")
root.resizable(False, False)
root.title("Reservation System")


# --- NAVIGATION BAR ---
navbar = tk.Frame(root, width=300, height=800, bg='#A52A2A')
navbar.grid(row=0, column=0)
navbar.grid_propagate(0)


# -- NAVIGATION BUTTONS --
home_btn = tk.Button(navbar, text="Home", width=37, height=2, bg="#A52A2A", fg="white", command=lambda: home_frame.tkraise())
home_btn.grid(row=0)

login_btn = tk.Button(navbar, text="Login", width=37, height=2, bg="#A52A2A", fg="white", command=lambda: login_frame.tkraise())
login_btn.grid(row=1)

logout_btn = tk.Button(navbar, text="Logout", width=37, height=2, bg="#A52A2A", fg="white")
logout_btn.grid(row=1)

login_btn.tkraise() # on starting the program login button will be shown instead of logout


quit_btn = tk.Button(navbar, text ="Close Application", width=37, height=2, bg="#A52A2A", fg="white", command=lambda: root.destroy())
quit_btn.grid(row=2)


# --- BODY FRAMES ---

# --- HOME PAGE ---
home_frame = tk.Frame(root, width=1100, height=800)
home_frame.grid(row=0, column=1)
home_frame.grid_propagate(False)

home_frame_title = tk.Label(home_frame, text="Reserve Seats", font=("Arial", 30)) # home page title
home_frame_title.place(x=200, y=100)

home_frame_calendar = tkcal.Calendar(home_frame, selectmode = "day", date_pattern = "d/m/yy")# home page calendar
home_frame_calendar.place(x=650, y=80)



# -- LOGIN PAGE --
login_frame = tk.Frame(root, width=1100, height=800)
login_frame.grid(row=0, column=1)
login_frame.grid_propagate(False)

login_frame_title = tk.Label(login_frame, text="Login", font=("Arial", 30)) # login page title
login_frame_title.place(x=200, y=100)

login_frame_say_email = tk.Label(login_frame, text="Email:", font=("Arial", 10)) # login page email
login_frame_say_email.place(x=200, y=180)

login_frame_email = tk.Entry(login_frame,width=50)
login_frame_email.place(x=200, y=200)

login_frame_say_pass = tk.Label(login_frame, text="Password:", font=("Arial", 10)) # login page password
login_frame_say_pass.place(x=200, y=230)

login_frame_pass = tk.Entry(login_frame,width=50,)
login_frame_pass.place(x=200, y=250)

login_frame_submit_btn = tk.Button(login_frame, text="Submit", width=10, height=1, bg="#A52A2A", fg="white") # login submit btn
login_frame_submit_btn.place(x=400, y=290)



# -- REGISTER PAGE -- #needs fix and to be implemented
# register_frame = tk.Frame(root, width=1100, height=800)
# register_frame.grid(row=0, column=1)
# register_frame.grid_propagate(False)

# register_frame_title = tk.Label(register_frame, text="Register", font=("Arial", 30)) # register page title
# register_frame_title.place(x=200, y=100)

# register_frame_say_name = tk.Label(register_frame, text="Nome:", font=("Arial", 10)) # register page name #needs fix
# register_frame_say_name.place(x=200, y=180)

# register_frame_name = tk.Entry(register_frame,width=50) #needs fix
# register_frame_name.place(x=200, y=200)

# register_frame_say_last_name = tk.Label(register_frame, text="Nome:", font=("Arial", 10)) # register page last name #needs fix
# register_frame_say_last_name.place(x=200, y=180)

# register_frame_last_lame = tk.Entry(register_frame,width=50) #needs fix
# register_frame_last_lame.place(x=200, y=200)

# register_frame_say_email = tk.Label(register_frame, text="Email:", font=("Arial", 10)) # register page email
# register_frame_say_email.place(x=200, y=180)

# register_frame_email = tk.Entry(register_frame,width=50)
# register_frame_email.place(x=200, y=200)

# register_frame_say_pass = tk.Label(register_frame, text="Password:", font=("Arial", 10)) # register page password
# register_frame_say_pass.place(x=200, y=230)

# register_frame_pass = tk.Entry(register_frame,width=50,)
# register_frame_pass.place(x=200, y=250)

# register_frame_say_nif = tk.Label(register_frame, text="Password:", font=("Arial", 10)) # register page nif #needs fix
# register_frame_say_nif.place(x=200, y=230)

# register_frame_nif = tk.Entry(register_frame,width=50,) #needs fix
# register_frame_nif.place(x=200, y=250)


# register_frame_submit_btn = tk.Button(register_frame, text="Submit", width=10, height=1, bg="#A52A2A", fg="white")
# register_frame_submit_btn.place(x=400, y=290)




home_frame.tkraise() # on starting the program the home page frame will be shown

root.mainloop()
