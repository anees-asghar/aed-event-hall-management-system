import tkinter as tk

class LoginPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg="#F1EEE9")
        self.app = app

        # put login_page inside app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # login form frame
        login_form_frame = tk.Frame(self, bg="#F1EEE9")
        login_form_frame.place(relx=0.5, rely=0.1, relheight=0.5, relwidth=0.5, anchor="n")

        # page title
        self.title_label = tk.Label(login_form_frame, bg="#F1EEE9", text="Login", font=("Helvetica", 30))
        self.title_label.place(relx=0, rely=0, relwidth=1, relheight=0.3)

        # email label and entry field
        self.email_label = tk.Label(login_form_frame, bg="#F1EEE9", text="Email:", font=("Helvetica", 11))
        self.email_label.place(relx=0, rely=0.3, relheight=0.1)
        self.email_entry = tk.Entry(login_form_frame, font=("Helvetica", 10), borderwidth=5, relief="flat")
        self.email_entry.place(relx=0.4, rely=0.3, relwidth=0.6, relheight=0.1)
        self.email_entry.focus_set()

        # password label and entry
        self.password_label = tk.Label(login_form_frame, bg="#F1EEE9", text="Password:", font=("Helvetica", 11))
        self.password_label.place(relx=0, rely=0.45, relheight=0.1)
        self.password_entry = tk.Entry(login_form_frame, font=("Helvetica", 10), borderwidth=5, relief="flat", show='*')
        self.password_entry.place(relx=0.4, rely=0.45, relwidth=0.6, relheight=0.1)
        
        # error message label (empty on startup)
        self.error_label = tk.Label(login_form_frame, text="", bg="#F1EEE9", fg="red", font=("Helvetica", 10))
        self.error_label.place(relx=0, rely=0.6, relheight=0.1)

        # login button
        self.login_btn = tk.Button(login_form_frame, text="Login", bg="#15133C", fg="white", relief="flat", 
            command= self.submit_data)
        self.login_btn.place(relx=0.8, rely=0.6, relwidth=0.2, relheight=0.1)

        # label and button to redirect to register page
        self.register_btn = tk.Button(login_form_frame, bg="#F1EEE9", text="Don't have an account? Register Now!", 
            relief="flat", command=self.app.register_page.show)
        self.register_btn.place(relx=0, rely=0.75, relheight=0.1)
    
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
