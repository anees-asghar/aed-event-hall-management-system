import tkinter as tk

class Navbar(tk.Frame):
    def __init__(self, container): # container == root
        super().__init__(container, width=300, height=800, bg='#A52A2A') # self == navbar
        self.container = container
        self.grid(row=0, column=0)
        self.grid_propagate(0)

        self.home_btn = tk.Button(self, text="Home", width=37, height=2, bg="#A52A2A", fg="white", 
            command=self.container.home_page.show)
        self.home_btn.grid(row=0)

        self.login_btn = tk.Button(self, text="Login", width=37, height=2, bg="#A52A2A", fg="white", 
            command=self.container.login_page.show)
        self.login_btn.grid(row=1)

        self.logout_btn = tk.Button(self, text="Logout", width=37, height=2, bg="#A52A2A", fg="white", 
            command=self.container.auth_manager.logout_user)
        self.logout_btn.grid(row=1)

        self.quit_btn = tk.Button(self, text ="Close Application", width=37, height=2, bg="#A52A2A", fg="white", 
            command=self.container.destroy)
        self.quit_btn.grid(row=2)

        self.admin_btn = tk.Button(self, text ="Admin Page", width=37, height=2, bg="#A52A2A", fg="white", 
            command=self.container.admin_page.show)
        self.admin_btn.grid(row=3)

        self.my_reservations_btn = tk.Button(self, text ="My Reservations", width=37, height=2, 
            bg="#A52A2A", fg="white", command=self.container.my_reservations_page.show)
        self.my_reservations_btn.grid(row=4)

        self.show_login_btn() # on starting the program login button will be shown instead of logout

    def show_login_btn(self):
        self.login_btn.tkraise()

    def show_logout_btn(self):
        self.logout_btn.tkraise()