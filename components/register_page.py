import re
import tkinter as tk

class RegisterPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, width=1100, height=800)
        self.app = app

        # put register page inside app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # page title
        self.title_label = tk.Label(self, text="Register", font=("Arial", 30))
        self.title_label.place(x=200, y=100)

        # error message label (empty on startup)
        self.error_label = tk.Label(self, text="", fg="red", font=("Arial"))
        self.error_label.place(x=200, y=170) 

        # first name label and entry field
        self.first_name = tk.Label(self, text="First Name:", font=("Arial", 10))
        self.first_name.place(x=200, y=210)
        self.first_name_entry = tk.Entry(self, width=50) 
        self.first_name_entry.place(x=200, y=230)

        # last name label and entry field
        self.last_name_label  = tk.Label(self, text="Last Name:", font=("Arial", 10))
        self.last_name_label.place(x=200, y=260)
        self.last_name_entry = tk.Entry(self, width=50)
        self.last_name_entry.place(x=200, y=280)

        # email label and entry field
        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10))
        self.email_label.place(x=200, y=310)
        self.email_entry= tk.Entry(self, width=50)
        self.email_entry.place(x=200, y=330)

        # password label and entry field
        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10))
        self.password_label.place(x=200, y=360)
        self.password_entry = tk.Entry(self, width=50, show="*")
        self.password_entry.place(x=200, y=380)

        # register button
        self.register_btn = tk.Button(self, text="Submit", width=10, height=1, bg="#A52A2A", fg="white", 
            command= self.submit_data)
        self.register_btn.place(x=500, y=430)
    
    def submit_data(self):
        # get data from the input fields
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # check if first_name field is empty
        if not first_name:
            self.show(message="Please add a first name.")
            return

        # check if last_name field is empty
        if not last_name:
            self.show(message="Please add a last name.")
            return

        # check if email field is empty
        if not email:
            self.show(message="Please add a email.")
            return

        # check if email format is valid
        if not self.is_email_valid(email):
            self.show(message="Invalid email. Please try again.")
            return

        # check if password field is empty
        if not password:
            self.show(message="Please add a password.")
            return

        success = self.app.auth_manager.register_user(first_name, last_name, email, password) # register user

        if success: # if logged in successfully
            # redirect to login page with success message
            self.app.login_page.show("User registered successfully.", "green") 
        
        else: # if not registered successfully (email already in use)
            self.show(message="User with this email already exists.")
        
    def is_email_valid(self, email):
        """
            Return True if the format of the given email address is valid, False if not.
        """
        # WILL BE UNCOMMENTED IN THE END
        # regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # if re.fullmatch(regex, email):
        #     return True
        # return False
        return True

    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color) # set the error message (if any)
        self.first_name_entry.delete(0, "end")                     # clear the first name entry field
        self.last_name_entry.delete(0, "end")                      # clear the last name entry field
        self.email_entry.delete(0, 'end')                          # clear the email entry field
        self.password_entry.delete(0, 'end')                       # clear the password entry field
        self.tkraise()                                             # raise the register page
