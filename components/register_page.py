import re
import tkinter as tk

class RegisterPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg="#F1EEE9")
        self.app = app

        # put register page inside app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # register form frame
        register_form_frame = tk.Frame(self, bg="#F1EEE9")
        register_form_frame.place(relx=0.5, rely=0.1, relheight=0.5, relwidth=0.5, anchor="n")

        # page title
        self.title_label = tk.Label(register_form_frame, text="Register", bg="#F1EEE9", font=("Helvetica", 30))
        self.title_label.place(relx=0, rely=0, relheight=0.3, relwidth=1)

        # first name label and entry field
        self.first_name = tk.Label(register_form_frame, text="First Name:", bg="#F1EEE9", font=("Helvetica", 11))
        self.first_name.place(relx=0, rely=0.3, relheight=0.1)
        self.first_name_entry = tk.Entry(register_form_frame, font=("Helvetica", 10), borderwidth=5, relief="flat") 
        self.first_name_entry.place(relx=0.4, rely=0.3, relheight=0.1, relwidth=0.6)
        self.first_name_entry.focus_set()

        # last name label and entry field
        self.last_name_label  = tk.Label(register_form_frame, text="Last Name:", bg="#F1EEE9", font=("Helvetica", 11))
        self.last_name_label.place(relx=0, rely=0.45, relheight=0.1)
        self.last_name_entry = tk.Entry(register_form_frame, font=("Helvetica", 10), borderwidth=5, relief="flat")
        self.last_name_entry.place(relx=0.4, rely=0.45, relheight=0.1, relwidth=0.6)

        # email label and entry field
        self.email_label = tk.Label(register_form_frame, text="Email:", bg="#F1EEE9", font=("Helvetica", 11))
        self.email_label.place(relx=0, rely=0.6, relheight=0.1)
        self.email_entry= tk.Entry(register_form_frame, font=("Helvetica", 10), borderwidth=5, relief="flat")
        self.email_entry.place(relx=0.4, rely=0.6, relheight=0.1, relwidth=0.6)

        # password label and entry field
        self.password_label = tk.Label(register_form_frame, text="Password:", bg="#F1EEE9", font=("Helvetica", 11))
        self.password_label.place(relx=0, rely=0.75, relheight=0.1)
        self.password_entry = tk.Entry(register_form_frame, font=("Helvetica", 10), borderwidth=5, relief="flat", show="*")
        self.password_entry.place(relx=0.4, rely=0.75, relheight=0.1, relwidth=0.6)

        # error message label (empty on startup)
        self.error_label = tk.Label(register_form_frame, text="", bg="#F1EEE9", fg="red", font=("Helvetica"))
        self.error_label.place(relx=0, rely=0.9, relheight=0.1) 

        # register button
        self.register_btn = tk.Button(register_form_frame, text="Register", bg="#15133C", fg="white", 
            relief="flat", command= self.submit_data)
        self.register_btn.place(relx=0.8, rely=0.9, relheight=0.1, relwidth=0.2)
    
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
