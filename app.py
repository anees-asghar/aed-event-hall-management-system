import tkinter as tk


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

# -- LOGIN PAGE --
login_frame = tk.Frame(root, width=1100, height=800)
login_frame.grid(row=0, column=1)
login_frame.grid_propagate(False)

login_frame_title = tk.Label(login_frame, text="Login", font=("Arial", 30)) # login page title
login_frame_title.place(x=200, y=100)

home_frame.tkraise() # on starting the program the home page frame will be shown


root.mainloop()
