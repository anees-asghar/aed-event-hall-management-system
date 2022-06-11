import tkinter as tk

class Navbar(tk.Frame):
    def __init__(self, container): # container == root
        super().__init__(container, width=300, height=800, bg='#A52A2A') # self == navbar
        self.container = container
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

        self.admin_btn = tk.Button(self, text ="Admin Page", width=37, height=2, bg="#A52A2A", fg="white")
        self.admin_btn.grid(row=3)

        self.my_reservations_btn = tk.Button(self, text ="My Reservations", width=37, height=2, bg="#A52A2A", fg="white")
        self.my_reservations_btn.grid(row=4)

    def show_login_btn(self):
        self.login_btn.tkraise()

    def show_logout_btn(self):
        self.logout_btn.tkraise()