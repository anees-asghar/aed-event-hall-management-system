import tkinter as tk

from database import Database
from authentication import AuthManager

from components.navbar import Navbar
from components.home_page import HomePage
from components.admin_page import AdminPage
from components.login_page import LoginPage
from components.register_page import RegisterPage
from components.my_resrvations_page import MyReservationsPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.resizable(False, False)
        self.title("Reservation System")


        self.db = Database("reservation_system.db")
        self.auth_manager = AuthManager(self.db, self)

        # create main pages
        self.navbar = Navbar(self)
        self.home_page = HomePage(self)
        self.login_page = LoginPage(self)
        self.register_page = RegisterPage(self)
        self.admin_page = AdminPage(self)
        self.my_reservations_page = MyReservationsPage(self)
        
        # add functionality to buttons
        self.navbar.home_btn.configure(command=self.home_page.show)
        self.navbar.login_btn.configure(command=self.login_page.show)
        self.navbar.logout_btn.configure(command=self.auth_manager.logout_user)
        self.navbar.admin_btn.configure(command =self.admin_page.tkraise)
        self.navbar.my_reservations_btn.configure(command=self.my_reservations_page.show)
        self.navbar.quit_btn.configure(command=self.destroy)
        self.login_page.register_btn.configure(command=self.register_page.show)


if __name__ == "__main__":
    app = App()
    app.home_page.tkraise()
    app.mainloop()