import tkinter as tk
import tkcalendar as tkcal


class RootWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.resizable(False, False)
        self.title("Reservation System")


class Navbar(tk.Frame):
    def __init__(self, container, home_page, login_page): # container == root
        self.home_page = home_page # temporary
        self.login_page = login_page # temporary

        super().__init__(container, width=300, height=800, bg='#A52A2A') # self == navbar
        self.grid(row=0, column=0)
        self.grid_propagate(0)

        self.home_btn = tk.Button(self, text="Home", width=37, height=2, bg="#A52A2A", fg="white", 
            command=lambda: self.home_page.tkraise())
        self.home_btn.grid(row=0)

        self.login_btn = tk.Button(self, text="Login", width=37, height=2, bg="#A52A2A", fg="white", 
            command=lambda: self.login_page.tkraise())
        self.login_btn.grid(row=1)

        self.logout_btn = tk.Button(self, text="Logout", width=37, height=2, bg="#A52A2A", fg="white")
        self.logout_btn.grid(row=1)

        self.quit_btn = tk.Button(self, text ="Close Application", width=37, height=2, bg="#A52A2A", fg="white", 
            command=lambda: container.destroy())
        self.quit_btn.grid(row=2)

        self.login_btn.tkraise() # on starting the program login button will be shown instead of logout


class HomePage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800)
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title = tk.Label(self, text="Reserve Seats", font=("Arial", 30)) # home page title
        self.title.place(x=200, y=100)

        self.calendar = tkcal.Calendar(self, selectmode="day", date_pattern="d/m/yy")# home page calendar
        self.calendar.place(x=650, y=80)


class LoginPage(tk.Frame):
    def __init__(self, container, register_page):
        self.register_page = register_page # temporary

        super().__init__(container, width=1100, height=800)
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Login", font=("Arial", 30)) # login page title
        self.title_label.place(x=200, y=100)

        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10)) # login page email
        self.email_label.place(x=200, y=180)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.place(x=200, y=200)

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10)) # login page password
        self.password_label.place(x=200, y=230)
        self.password_entry = tk.Entry(self,width=50,)
        self.password_entry.place(x=200, y=250)

        self.submit_btn = tk.Button(self, text="Submit", width=10, height=1, bg="#A52A2A", fg="white") # login submit btn
        self.submit_btn.place(x=500, y=290)

        self.register_label = tk.Label(self, text="Don't have an accout? Register now.")
        self.register_label.place(x=200, y=380)
        self.register_btn = tk.Button(self, text="Register", width=10, height=1, command=lambda: self.register_page.tkraise())
        self.register_btn.place(x=500, y=380)


class RegisterPage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800)
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Register", font=("Arial", 30)) # register page title
        self.title_label.place(x=200, y=100)

        self.name_label = tk.Label(self, text="Name:", font=("Arial", 10)) # register page name 
        self.name_label.place(x=200, y=180)
        self.name_entry = tk.Entry(self,width=50) 
        self.name_entry .place(x=200, y=200)

        self.last_name_label  = tk.Label(self, text="Last name:", font=("Arial", 10)) # register page last name 
        self.last_name_label.place(x=200, y=230)
        self.last_name_entry = tk.Entry(self,width=50)
        self.last_name_entry.place(x=200, y=250)

        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10)) # register page email
        self.email_label.place(x=200, y=280)
        self.email_entry= tk.Entry(self,width=50)
        self.email_entry.place(x=200, y=300)

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10)) # register page password
        self.password_label.place(x=200, y=330)
        self.password_entry = tk.Entry(self,width=50)
        self.password_entry.place(x=200, y=350)

        self.register_btn = tk.Button(self, text="Submit", width=10, height=1, bg="#A52A2A", fg="white")
        self.register_btn.place(x=500, y=400)


if __name__ == "__main__":
    root = RootWindow()
    home_page = HomePage(root)
    register_page = RegisterPage(root)
    login_page = LoginPage(root, register_page)

    home_page.tkraise()

    navbar = Navbar(root, home_page, login_page)

    root.mainloop()
 
