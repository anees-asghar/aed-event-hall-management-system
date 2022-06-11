import tkinter as tk

class RegisterPage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800)
        self.container = container
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Register", font=("Arial", 30)) # register page title
        self.title_label.place(x=200, y=100)

        self.error_label = tk.Label(self, text="", fg="red", font=("Arial"))#error label
        self.error_label.place(x=200, y=170) 

        self.first_name = tk.Label(self, text="Name:", font=("Arial", 10)) # register page name 
        self.first_name.place(x=200, y=210)
        self.first_name_entry = tk.Entry(self,width=50) 
        self.first_name_entry.place(x=200, y=230)

        self.last_name_label  = tk.Label(self, text="Last name:", font=("Arial", 10)) # register page last name 
        self.last_name_label.place(x=200, y=260)
        self.last_name_entry = tk.Entry(self,width=50)
        self.last_name_entry.place(x=200, y=280)

        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10)) # register page email
        self.email_label.place(x=200, y=310)
        self.email_entry= tk.Entry(self,width=50)
        self.email_entry.place(x=200, y=330)

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10)) # register page password
        self.password_label.place(x=200, y=360)
        self.password_entry = tk.Entry(self,width=50)
        self.password_entry.place(x=200, y=380)

        self.register_btn = tk.Button(self, text="Submit", width=10, height=1, bg="#A52A2A", fg="white", 
            command= self.submit_data)
        self.register_btn.place(x=500, y=430)

    
    def submit_data(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        #In case if one or more inputs are missing in register
        if not first_name:
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

        success = self.container.auth_manager.register_user(first_name, last_name, email, password)

        if success:
            self.container.login_page.show() # redirect to login page
        else:
            self.show(message="User with this email already exists.") # show register page with error message

    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color)
        self.first_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.email_entry.delete(0, 'end') 
        self.password_entry.delete(0, 'end')
        self.tkraise()