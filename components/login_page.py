import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, width=1100, height=800)
        self.app = app

        # put login_page inside app
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        # page title
        self.title_label = tk.Label(self, text="Login", font=("Arial", 30))
        self.title_label.place(x=200, y=100)

        # error message label (empty on startup)
        self.error_label = tk.Label(self, text="", fg="red", font=("Arial"))
        self.error_label.place(x=200, y=180) 

        # email label and entry field
        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10))
        self.email_label.place(x=200, y=220)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.place(x=200, y=240)

        # password label and entry
        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10))
        self.password_label.place(x=200, y=270)
        self.password_entry = tk.Entry(self, width=50, show='*')
        self.password_entry.place(x=200, y=290)
        
        # login button
        self.login_btn = tk.Button(self, text="Login", width=10, height=1, bg="#A52A2A", fg="white", 
            command= self.submit_data) # login submit btn
        self.login_btn.place(x=500, y=330)

        # label and button to redirect to register page
        self.register_label = tk.Label(self, text="Don't have an account? Register now.")
        self.register_label.place(x=200, y=420)
        self.register_btn = tk.Button(self, text="Register", width=10, height=1, 
            command=self.app.register_page.show)
        self.register_btn.place(x=500, y=420)
    
    def submit_data(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # in case if one or more inputs are missing in register
        if not email:
            self.show(message="Add an email please.")
            return

        if not password:
            self.show(message="Add a password please.")
            return
        
        # login user
        success = self.app.auth_manager.login_user(email, password)
        if success: # if logged in successfully
            self.app.home_page.show()         # redirect to home page
            self.app.navbar.show_logout_btn() # show logout button in navbar 
        
        else: # if not logged in successfully (invalid credentials)
            self.show(message="User with these credentials does not exist.")
    
    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color) # set the error message (if any)
        self.email_entry.delete(0, 'end')                          # clear the email entry
        self.password_entry.delete(0, 'end')                       # clear the password entry
        self.tkraise()                                             # raise the login_page
