import email
import tkinter as tk
import tkcalendar as tkcal


class RootWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        #self.resizable(False, False)
        self.title("Reservation System")


class Navbar(tk.Frame):
    def __init__(self, container): # container == root

        super().__init__(container, width=300, height=800, bg='#A52A2A') # self == navbar
        self.grid(row=0, column=0)
        self.grid_propagate(0)

        self.home_btn = tk.Button(self, text="Home", width=37, height=2, bg="#A52A2A", fg="white")
        self.home_btn.grid(row=0)

        self.login_btn = tk.Button(self, text="Login", width=37, height=2, bg="#A52A2A", fg="white")
        self.login_btn.grid(row=1)

        self.logout_btn = tk.Button(self, text="Logout", width=37, height=2, bg="#A52A2A", fg="white")
        self.logout_btn.grid(row=1)

        self.quit_btn = tk.Button(self, text ="Close Application", width=37, height=2, bg="#A52A2A", fg="white")
        self.quit_btn.grid(row=2)

        self.login_btn.tkraise() # on starting the program login button will be shown instead of logout

    # def raise_home_page(self, container):
    #     home_page = container.__dict__["children"]["!homepage"]
    #     home_page.tkraise()

    # def raise_login_page(self, container):
    #     login_page = container.__dict__["children"]["!loginpage"]
    #     login_page.tkraise()


class HomePage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800, bg="#F8F9F9")
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title = tk.Label(self, text="Reserve Seats", font=("Arial", 30)) # home page title
        self.title.place(x=200, y=100)

        self.calendar = tkcal.Calendar(self, selectmode="day", date_pattern="d/m/yy")# home page calendar
        self.calendar.place(x=650, y=80)

    def show(self):
        self.tkraise()


class LoginPage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800, bg="#F8F9F9")
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Login", font=("Arial", 30)) # login page title
        self.title_label.place(x=200, y=100)
        
        self.error_label = tk.Label(self, text="", font=("Arial"))#error label
        self.error_label.place(x=200, y=180) 

        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10)) # login page email
        self.email_label.place(x=200, y=220)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.place(x=200, y=240)

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10)) # login page password
        self.password_label.place(x=200, y=270)
        self.password_entry = tk.Entry(self,width=50,)
        self.password_entry.place(x=200, y=290)

        self.submit_btn = tk.Button(self, text="Submit", width=10, height=1, bg="#A52A2A", fg="white", command= self.submit_data) # login submit btn
        self.submit_btn.place(x=500, y=330)
   

        self.register_label = tk.Label(self, text="Don't have an accout? Register now.")
        self.register_label.place(x=200, y=420)
        self.register_btn = tk.Button(self, text="Register", width=10, height=1)
        self.register_btn.place(x=500, y=420)
    
    def show(self):
        self.tkraise()
    
    def submit_data(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        print(email,password)

    #In case if one or more inputs are missing in register
        if not email:
            self.error_label.configure(text="Add an email please.")
            return

        if not password:
            self.error_label.configure(text="Add a password please.")
            return

        print(email, password)
        return


class RegisterPage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800, bg="#F8F9F9")
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Register", font=("Arial", 30)) # register page title
        self.title_label.place(x=200, y=100)

        self.error_label = tk.Label(self, text="", font=("Arial"))#error label
        self.error_label.place(x=200, y=140) 

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

        self.register_btn = tk.Button(self, text="Submit", width=10, height=1, bg="#A52A2A", fg="white",command= self.submit_data)
        self.register_btn.place(x=500, y=400)

    def show(self):
        self.tkraise()
    
    def submit_data(self):
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        print(name,last_name,email,password)

    #In case if one or more inputs are missing in register
        if not name:
            self.error_label.configure(text="Name is missing")
            return

        if not last_name:
            self.error_label.configure(text="Last name is missing")
            return

        if not email:
            self.error_label.configure(text="Add an email please.")
            return

        if not password:
            self.error_label.configure(text="Add a password please.")
            return

        print(name,last_name,email, password)
        return
 
if __name__ == "__main__":
    root = RootWindow()

    navbar = Navbar(root)

    home_page = HomePage(root)
    login_page = LoginPage(root)
    register_page = RegisterPage(root)

    # Add functionality to buttons
    navbar.home_btn.configure(command=home_page.show)
    navbar.login_btn.configure(command=login_page.show)
    navbar.logout_btn.configure(command=None) # to be implemented
    navbar.quit_btn.configure(command=root.destroy)
    login_page.register_btn.configure(command=register_page.show)

    

    home_page.tkraise()

    root.mainloop()
 
