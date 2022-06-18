import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, width=1100, height=800)
        self.app = app

        # put login_page inside app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # page title
        self.title_label = tk.Label(self, text="Login", font=("Arial", 30))
        self.title_label.place(relx=0.10, rely=0.10, relwidth=0.3, relheight=0.06)

        # error message label (empty on startup)
        self.error_label = tk.Label(self, text="", fg="red", font=("Arial"))
        self.error_label.place(relx=0.15, rely=0.22, relwidth=0.3, relheight=0.02)

        # email label and entry field
        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10))
        self.email_label.place(relx=0.19, rely=0.28, relwidth=0.06, relheight=0.02)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.place(relx=0.20, rely=0.32, relwidth=0.3, relheight=0.03)

        # password label and entry
        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10))
        self.password_label.place(relx=0.20, rely=0.37, relwidth=0.06, relheight=0.02)
        self.password_entry = tk.Entry(self, width=50, show='*')
        self.password_entry.place(relx=0.20, rely=0.42, relwidth=0.3, relheight=0.03)
        
        # login button
        self.login_btn = tk.Button(self, text="Login", width=10, height=1, bg="#A52A2A", fg="white", 
            command= self.submit_data) # login submit btn
        self.login_btn.place(relx=0.42, rely=0.48, relwidth=0.080, relheight=0.03)

        # label and button to redirect to register page
        self.register_label = tk.Label(self, text="Don't have an account? Register now.")
        self.register_label.place(relx=0.20, rely=0.54, relwidth=0.20, relheight=0.03)
        self.register_btn = tk.Button(self, text="Register", width=10, height=1, 
            command=self.app.register_page.show)
        self.register_btn.place(relx=0.42, rely=0.54, relwidth=0.080, relheight=0.03)
    
    def submit_data(self):
        # get data from the input fields
        email = self.email_entry.get()
        password = self.password_entry.get()

        # check if email field is empty
        if not email:
            self.show(message="Please add an email.")
            return

        # check if password field is empty
        if not password:
            self.show(message="Please add a password.")
            return
        
        success = self.app.auth_manager.login_user(email, password) # log in user

        if success: # if logged in successfully
            self.app.home_page.show()         # redirect to home page
            self.app.navbar.show_logout_btn() # show logout button in navbar 
            
            # show admin page button to user if user has admin role
            # if not, show my reservations page button
            if self.app.auth_manager.logged_in_user_role == "Admin":
                self.app.navbar.show_admin_page_btn()
            else:
                self.app.navbar.show_my_res_page_btn()
        
        else: # if not logged in successfully (invalid credentials)
            self.show(message="User with these credentials does not exist.")
    
    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color) # set the error message (if any)
        self.email_entry.delete(0, 'end')                          # clear the email entry field
        self.password_entry.delete(0, 'end')                       # clear the password entry field
        self.tkraise()                                             # raise the login_page
