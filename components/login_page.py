import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, container):
        super().__init__(container, width=1100, height=800)
        self.container = container

        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Login", font=("Arial", 30)) # login page title
        self.title_label.place(x=200, y=100)

        self.error_label = tk.Label(self, text="", fg="red", font=("Arial"))#error label
        self.error_label.place(x=200, y=180) 

        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10)) # login page email
        self.email_label.place(x=200, y=220)
        self.email_entry = tk.Entry(self, width=50)
        self.email_entry.place(x=200, y=240)

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10)) # login page password
        self.password_label.place(x=200, y=270)
        self.password_entry = tk.Entry(self,width=50,)
        self.password_entry.place(x=200, y=290)

        self.submit_btn = tk.Button(self, text="Submit", width=10, height=1, bg="#A52A2A", fg="white", 
            command= self.submit_data) # login submit btn
        self.submit_btn.place(x=500, y=330)

        self.register_label = tk.Label(self, text="Don't have an account? Register now.")
        self.register_label.place(x=200, y=420)
        self.register_btn = tk.Button(self, text="Register", width=10, height=1)
        self.register_btn.place(x=500, y=420)
    
    def submit_data(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # in case if one or more inputs are missing in register
        if not email:
            self.error_label.configure(text="Add an email please.")
            return

        if not password:
            self.error_label.configure(text="Add a password please.")
            return
        
        success = self.container.auth_manager.login_user(email, password)
        if success:
            self.container.home_page.show() # redirect user to home page
            self.container.navbar.show_logout_btn() # show logout button instead of login 
        else:
            self.show(message="User with these credentials does not exist.") # show login page with error message
    
    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color) # clear the error message
        self.email_entry.delete(0, 'end') # clear the email entry
        self.password_entry.delete(0, 'end') # clear the password entry
        self.tkraise()

