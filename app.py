import tkinter as tk


# --- ROOT WINDOW ---
root = tk.Tk()
root.geometry("1400x800")
root.resizable(False, False)
root.title("Reservation System")


# --- NAVIGATION BAR ---
navbar = tk.Frame(root, highlightbackground="blue", highlightthickness=1, width=200)
navbar.grid(row=0, column=0, sticky=tk.N+tk.W) # make navbar stick to top left through sticky

# navigation buttons

home_btn = tk.Button(navbar, text="Home", width=30, height=2, command=lambda: home_frame.tkraise())
home_btn.grid(row=0, column=0)

logout_btn = tk.Button(navbar, text="Logout", width=30, height=2)
logout_btn.grid(row=1, column=0)

login_btn = tk.Button(navbar, text="Login", width=30, height=2, command=lambda: login_frame.tkraise())
login_btn.grid(row=1, column=0)


# --- BODY FRAMES ---

# --- LOGIN PAGE ---
login_frame = tk.Frame(root, highlightbackground="red", highlightthickness=1)
login_frame.grid(row=0, column=1, sticky=tk.N)

# login title label
login_title = tk.Label(login_frame, width=140, height=39, text="Login")
login_title.grid(row=0, column=0)

# --- HOME PAGE ---

home_frame = tk.Frame(root, highlightbackground="red", highlightthickness=1)
home_frame.grid(row=0, column=1, sticky=tk.N)

# home title label
home_title = tk.Label(home_frame, width=140, height=39, text="Home Page")
home_title.grid(row=0, column=0)

# home_frame.grid_forget()
# login_frame.tkraise() # temporary

root.mainloop()
