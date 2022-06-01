import tkinter as tk
import tkcalendar as tkcal
from database import Database


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800")
        self.resizable(False, False)
        self.title("Reservation System")


class Navbar(tk.Frame):
    def __init__(self, container): # container == root

        super().__init__(container, width=300, height=800, bg='#A52A2A') # self == navbar
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


class HomePage(tk.Frame):

    def __init__(self, container):

        super().__init__(container, width=1100, height=800)
        self.selected_date = "01/01/22"

        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title = tk.Label(self, text="Reserve Seats", font=("Arial", 30)) # home page title
        self.title.place(x=200, y=100)

        self.selected_date_label = tk.Label(self, text=f"Selected date: {self.selected_date}", font=("Arial", 14))
        self.selected_date_label.place(x=200, y=180)

        self.calendar = tkcal.Calendar(self, selectmode="day", date=1, month=1, year=2022, date_pattern="dd/mm/yy")# home page calendar
        self.calendar.place(x=650, y=100)

        self.select_date_btn = tk.Button(self, text="Select Date", command=self.select_date)
        self.select_date_btn.place(x=650, y=320)

        self.seat_grid = SeatGrid(self)
        self.seat_grid.render(self.selected_date)
        self.seat_grid.place(x=200, y=400)

        self.book_seats_btn = tk.Button(self, text="Book", command=self.book_selected_seats)
        self.book_seats_btn.place(x=200, y=700)

    def select_date(self):
        if self.selected_date == self.calendar.get_date():
            return
        
        self.selected_date = self.calendar.get_date()
        self.selected_date_label.configure(text=f"Selected date: {self.selected_date}")
        self.seat_grid.render(self.selected_date)

    def book_selected_seats(self):
        if not self.seat_grid.selected_seats:
            return

        db.insert_reservations(logged_in_user_id, self.selected_date, self.seat_grid.selected_seats)
        self.seat_grid.render(self.selected_date)

    def show(self):
        self.tkraise()
        

class SeatGrid(tk.Frame):
    def __init__(self, container):
        super().__init__(container, width=400, height=200)
        self.buttons = {}
        self.selected_seats = set()
    
    def render(self, date):
        reservations = db.fetch_reservations_by_date(date)
        reserved_seats_data = {seat_num: {"owner_id": user_id} for _, user_id, _, seat_num in reservations}

        nums = ['1', '2', '3', '4', '5']
        letts = ['A', 'B', 'C', 'D', 'E']

        for i, l in enumerate(letts):
            for j, n in enumerate(nums):
                seat_num = n+l
                if seat_num in reserved_seats_data.keys(): # if the seat is reserved
                    if reserved_seats_data[seat_num]["owner_id"] == logged_in_user_id: # seat owned by logged in user
                        self.buttons[seat_num] = self.OwnedSeatButton(self, seat_num)
                        self.buttons[seat_num].grid(row=i, column=j)
                    else: # seat owned by different user
                        self.buttons[seat_num] = self.ReservedSeatButton(self, seat_num)
                        self.buttons[seat_num].grid(row=i, column=j)
                else: # if the seat is not reserved
                    self.buttons[seat_num] = self.OpenSeatButton(self, seat_num)
                    self.buttons[seat_num].grid(row=i, column=j)

    class OpenSeatButton(tk.Button):
        def __init__(self, container, seat_num):
            super().__init__(container, text=seat_num, width=10, height=2, bg="white", command=self.change_to_selected)
            self.seat_num = seat_num
            self.container = container

        def change_to_selected(self):
            # change button appearance
            self.configure(bg="yellow")
            self.configure(command=self.change_to_open) # change button command

            # add seat number to selected
            self.container.selected_seats.add(self.seat_num) # seat_grid == self.container
        
        def change_to_open(self):
            # change button appearance
            self.configure(bg="white")
            self.configure(command=self.change_to_selected)

            # remove seat number from selected
            self.parent_grid.selected_seats.remove(self.seat_num)

    class ReservedSeatButton(tk.Button):
        def __init__(self, container, seat_num):
            super().__init__(container, text=seat_num, width=10, height=2, bg="red")

    class OwnedSeatButton(tk.Button):
        def __init__(self, container, seat_num):
            super().__init__(container, text=seat_num, width=10, height=2, bg="green")


class LoginPage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800)
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

        user_id = db.login_user(email, password)
        if user_id:
            logged_in_user_id = user_id
            home_page.show()
            #Idea: When the user is logged in, top right corner, label saying the name of the user
        else:
            self.error_label.configure(text="User with these credentials does not exist.")
        
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
    
    def show(self):
        self.tkraise()


class RegisterPage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800)
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Register", font=("Arial", 30)) # register page title
        self.title_label.place(x=200, y=100)

        self.error_label = tk.Label(self, text="", fg="red", font=("Arial"))#error label
        self.error_label.place(x=200, y=140) 

        self.name_label = tk.Label(self, text="Name:", font=("Arial", 10)) # register page name 
        self.name_label.place(x=200, y=180)
        self.name_entry = tk.Entry(self,width=50) 
        self.name_entry.place(x=200, y=200)

        self.last_name_label  = tk.Label(self, text="Last name:", font=("Arial", 10)) # register page last name 
        self.last_name_label.place(x=200, y=230)
        self.last_name_entry = tk.Entry(self,width=50)
        self.last_name_entry.place(x=200, y=250)

        self.email_label = tk.Label(self, text="Email:", font=("Arial", 10)) # register page email
        self.email_label.place(x=200, y=280)
        self.email_entry= tk.Entry(self,width=50)
        self.email_entry.place(x=200, y=300)

        self.password_label = tk.Label(self, text="Password:", font=("Arial", 10)) # register page password
        self.password_label.place(x=200, y=330)
        self.password_entry = tk.Entry(self,width=50)
        self.password_entry.place(x=200, y=350)

        self.register_btn = tk.Button(self, text="Submit", width=10, height=1, bg="#A52A2A", fg="white", 
            command= self.submit_data)
        self.register_btn.place(x=500, y=400)


    def show(self):
        self.tkraise()
    
    def submit_data(self):
        name = self.name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        #In case if one or more inputs are missing in register
        if not name:
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

        print(name,last_name,email,password)


if __name__ == "__main__":
    logged_in_user_id = 0 # will be changed

    db = Database("test.db")

    root = App()

    # create main pages
    navbar = Navbar(root)
    home_page = HomePage(root)
    login_page = LoginPage(root)
    register_page = RegisterPage(root)

    # Add functionality to buttons
    navbar.home_btn.configure(command=home_page.show)
    navbar.login_btn.configure(command=login_page.show)
    navbar.logout_btn.configure(command=None) # to be implemented
    navbar.quit_btn.configure(command=root.destroy)
    login_page.register_btn.configure(command=register_page.show)

    home_page.show()

    root.mainloop()
    db.close()
 
