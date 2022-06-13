import tkinter as tk

from create_db import create_db
from database import Database
from authentication import AuthManager

from components.navbar import Navbar
from components.home_page import HomePage
from components.admin_page import AdminPage
from components.login_page import LoginPage
from components.register_page import RegisterPage
from components.my_reservations_page import MyReservationsPage


class App(tk.Tk):
    def __init__(self, db_name):
        super().__init__()
        self.geometry("1400x800")           # set window dimensions
        self.resizable(False, False)        # make window unresizable
        self.title("Reservation System")    # set window title

        self.db = Database(db_name)               # connect to database
        self.auth_manager = AuthManager(app=self) # authentication manager class instance

        # create the body pages
        self.home_page = HomePage(self)
        self.register_page = RegisterPage(self)
        self.login_page = LoginPage(self)
        self.admin_page = AdminPage(self)
        # self.my_reservations_page = MyReservationsPage(self)

        self.navbar = Navbar(self) # create the navbar


if __name__ == "__main__":
    DB_NAME = "reservation_system.db"

    create_db(DB_NAME)   # create db if doesn't exist
    app = App(DB_NAME)   # create an app instance
    app.home_page.show() # show home_page on startup
    app.mainloop()       # run the app
    app.db.close()       # close db connection