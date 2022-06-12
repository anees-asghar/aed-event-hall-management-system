import tkinter as tk

class Navbar(tk.Frame):
    def __init__(self, app):
        super().__init__(app, width=300, height=800, bg='#A52A2A')
        self.app = app

        # put navbar inside app window
        self.grid(row=0, column=0)
        self.grid_propagate(0)

        # home page button
        self.home_page_btn = tk.Button(self, text="Home", width=37, height=2, 
            bg="#A52A2A", fg="white", command=self.app.home_page.show)
        self.home_page_btn.grid(row=0)

        # admin page button
        self.admin_page_btn = tk.Button(self, text ="Admin Page", width=37, height=2, 
            bg="#A52A2A", fg="white", command=self.app.admin_page.show)
        self.admin_page_btn.grid(row=1)

        # my reservations page button
        self.my_res_page_btn = tk.Button(self, text ="My Reservations", width=37, height=2, 
            bg="#A52A2A", fg="white", command=self.app.my_reservations_page.show)
        self.my_res_page_btn.grid(row=1)

        # register page button
        self.register_page_btn = tk.Button(self, text ="Register", width=37, height=2, 
            bg="#A52A2A", fg="white", command=self.app.register_page.show)
        self.register_page_btn.grid(row=1)
        
        # logout button
        self.logout_btn = tk.Button(self, text="Logout", width=37, height=2, bg="#A52A2A", 
            fg="white", command=self.app.auth_manager.logout_user)
        self.logout_btn.grid(row=2)

        # login page button
        self.login_page_btn = tk.Button(self, text="Login", width=37, height=2, bg="#A52A2A", 
            fg="white", command=self.app.login_page.show)
        self.login_page_btn.grid(row=2)

        # exit app button
        self.exit_app_btn = tk.Button(self, text ="Exit App", width=37, height=2, bg="#A52A2A", fg="white", 
            command=self.app.destroy)
        self.exit_app_btn.grid(row=3)

    def show_login_page_btn(self):
        self.login_page_btn.tkraise()

    def show_logout_btn(self):
        self.logout_btn.tkraise()

    def show_register_page_btn(self):
        self.register_page_btn.tkraise()

    def show_admin_page_btn(self):
        self.admin_page_btn.tkraise()

    def show_my_res_page_btn(self):
        self.my_res_page_btn.tkraise()
