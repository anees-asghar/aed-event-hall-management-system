from multiprocessing.sharedctypes import Value
import tkinter as tk
import tkcalendar as tkcal
from database import Database
from tkinter import ttk


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

        self.admin_btn = tk.Button(self, text ="Admin Page", width=37, height=2, bg="#A52A2A", fg="white")
        self.admin_btn.grid(row=3)

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

        self.book_seats_btn = tk.Button(self, text="Book", width=7, height=1, bg="#A52A2A", fg="white", command=self.book_selected_seats)
        self.book_seats_btn.place(x=800, y=750)

        #Seat Label
        self.empty_seat_label = tk.Label(self, text="Empty seat", font=("Georgia"))#empty seat label
        self.empty_seat_label.place(x=200, y=230) 
        self.empty_seat_btn = tk.Button(self, text="", width=5, height=1, bg="white")
        self.empty_seat_btn.place(x=300, y=230)
    
        self.seat_taken_label = tk.Label(self, text="Seat Taken", font=("Georgia"))#seat takenlabel
        self.seat_taken_label.place(x=200, y=260) 
        self.seat_taken_btn = tk.Button(self, text="", width=5, height=1, bg="red")
        self.seat_taken_btn.place(x=300, y=260)
    
        self.chosen_seat_label = tk.Label(self, text="Chosen seat", font=("Georgia"))#chosen seat label
        self.chosen_seat_label.place(x=200, y=290) 
        self.chosen_seat_btn = tk.Button(self, text="", width=5, height=1, bg="green")
        self.chosen_seat_btn.place(x=300, y=290)

        self.vip_seat_label = tk.Label(self, text="VIP seat", font=("Georgia"))#vip seat label
        self.vip_seat_label.place(x=200, y=320)
        self.vip_seat_btn = tk.Button(self, text="👑", width=5, height=1)
        self.vip_seat_btn.place(x=300, y=320) 

        
        

    def select_date(self):
        if self.selected_date == self.calendar.get_date():
            return
        
        self.selected_date = self.calendar.get_date()
        self.selected_date_label.configure(text=f"Selected date: {self.selected_date}")
        self.seat_grid.render(self.selected_date)

    def book_selected_seats(self):
        if not self.seat_grid.selected_seats:
            return
        
        global logged_in_user_id
        if not logged_in_user_id: # no user is logged in
            login_page.show(message="Please login first.", message_color="green")
            return
        
        db.insert_reservations(logged_in_user_id, self.selected_date, self.seat_grid.selected_seats)
        self.seat_grid.render(self.selected_date)

    def show(self):
        self.seat_grid.render(self.selected_date)
        self.tkraise()
        

class SeatGrid(tk.Frame):
    def __init__(self, container):
        super().__init__(container, width=400, height=200)
        self.buttons = {} # button of a particular seat can be accessed by self.buttons[<seat_number>]
        self.selected_seats = set()
    
    def render(self, date):
        self.selected_seats.clear() # clear selected seats when grid is re-rendered

        global logged_in_user_id
        reservations = db.fetch_reservations_by_date(date)
        reserved_seats_data = {seat_num: {"owner_id": user_id} for _, user_id, _, seat_num in reservations}

        cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12','13','14']
        rows = ['K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        seats_to_ignore = ['3F','4F','5F','10F','11F','12F','3A','4A','5A','10A','11A','12A'] # seats that dont exist in the hall
        
        for i, r in enumerate(rows):
            for j, c in enumerate(cols):
                seat_num = c+r # for example 1A
                
                if seat_num in seats_to_ignore: # ignore the seat_num for which button isn't needed
                    continue 

                if seat_num in reserved_seats_data.keys(): # if the seat is reserved

                    if reserved_seats_data[seat_num]["owner_id"] == logged_in_user_id: # seat owned by logged in user
                        self.buttons[seat_num] = self.OwnedSeatButton(self, seat_num)
                    else: # seat owned by different user
                        self.buttons[seat_num] = self.ReservedSeatButton(self, seat_num)
                        
                else: # if the seat is not reserved
                    self.buttons[seat_num] = self.OpenSeatButton(self, seat_num)

                # place the button created in the grid
                if c in ['2', '12'] and r in ['B', 'F']: # row spacing and column spacing needed
                    self.buttons[seat_num].grid(row=i, column=j, padx=(0, 20), pady=(0, 20))
                elif c in ['2', '12']: # only column spacing needed
                    self.buttons[seat_num].grid(row=i, column=j, padx=(0, 20))
                elif r in ['B', 'F']: # only row spacing needed
                    self.buttons[seat_num].grid(row=i, column=j, pady=(0, 20))
                else: # no spacing needed
                    self.buttons[seat_num].grid(row=i, column=j)
    
        # decorate VIP seats differently
        for n in ["6F", "7F", "8F", "9F", "6A", "7A", "8A", "9A"]:
            self.buttons[n].configure(text="👑")
        
    class OpenSeatButton(tk.Button):
        def __init__(self, container, seat_num):
            super().__init__(container, text=seat_num, width=5, height=1, bg="white", command=self.change_to_selected)
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
            self.container.selected_seats.remove(self.seat_num)

    class ReservedSeatButton(tk.Button):
        def __init__(self, container, seat_num):
            super().__init__(container, text=seat_num, width=5, height=1, bg="red")

    class OwnedSeatButton(tk.Button):
        def __init__(self, container, seat_num):
            super().__init__(container, text=seat_num, width=5, height=1, bg="green")


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

        user_id = db.authenticate_user(email, password) # checks if a user with this email and password exists
                                                        # and returns the user_id

        if user_id:
            global logged_in_user_id
            logged_in_user_id = user_id # set global logged_in_user_id
            home_page.show() # redirect user to home page
            navbar.logout_btn.tkraise() # show logout button instead of login 
            
            
            # self.selected_name = "Teste" #########Francisco
            # self.name_label = tk.Label(self, text=f"{self.selected_name}", font=("Arial", 14))
            # self.name_label.place(x=1000, y=20)
        else:
            self.show(message="User with these credentials does not exist.") # show login page with error message
    
    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color) # clear the error message
        self.email_entry.delete(0, 'end') # clear the email entry
        self.password_entry.delete(0, 'end') # clear the password entry
        self.tkraise()

class RegisterPage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800)
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

        success = db.register_user(first_name, last_name, email, password)

        if success:
            login_page.show() # redirect to login page
        else:
            self.show(message="User with this email already exists.") # show register page with error message

    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color)
        self.first_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.email_entry.delete(0, 'end') 
        self.password_entry.delete(0, 'end')
        self.tkraise()

class AdminPage(tk.Frame):
    def __init__(self, container):

        super().__init__(container, width=1100, height=800)
        self.grid(row=0, column=1)
        #self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Admin Page", font=("Arial", 30)) # admin page title
        self.title_label.place(x=200, y=100)

        # Earnings_1_day
        self.Earnings_1_day_label = tk.Label(self, text="Total Earnings in one day:", font=("Arial", 10)) 
        self.Earnings_1_day_label.place(x=200, y=200)

        
        
        #def comboclick(self,event):
            #tk.Label(self, text = combo.get()).place(x=600, y=450)
        # for months in months_admin:
        #     for days in days_odd_admin:
        #         if months == ["April","June","August","October","December"]:
        #             #days = 
        #             pass

        days_odd_admin = [i for i in range(1,31+1)]
        days_pair_admin = [i for i in range(1,30+1)]
        days_fab_admin =[i for i in range(1,28+1)]

        months_admin = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        years_admin = ["2022","2023"]
        self.clicked = tk.StringVar()
        self.clicked.set(months_admin[0])
        self.clicked.set(years_admin[0])
        # self.dropdown_menu = tk.OptionMenu(self, self.clicked, *months_admin)
        # self.dropdown_menu.place(x=200, y=450)

        comboM = ttk.Combobox(self, value = months_admin)
        comboM.current(0)
        #combo.bind("<<ComboboxSelected>>", comboclick)
        comboM.place(x=400, y=250)
        
        comboY = ttk.Combobox(self, value = years_admin)
        comboY.current(0)
        #combo.bind("<<ComboboxSelected>>", comboclick)
        comboY.place(x=600, y=250)
        #################################
        
        # Earnings_1_month
        self.Earnings_1_month_label = tk.Label(self, text="Total Earnings in one month:", font=("Arial", 10)) 
        self.Earnings_1_month_label.place(x=200, y=400)

        
        #def comboclick(self,event):
            #tk.Label(self, text = combo.get()).place(x=600, y=450)
            
        one_month_admin = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        one_year_admin = ["2022","2023"]
        self.clicked = tk.StringVar()
        self.clicked.set(one_month_admin[0])
        self.clicked.set(one_year_admin[0])
        # self.dropdown_menu = tk.OptionMenu(self, self.clicked, *one_month_admin)
        # self.dropdown_menu.place(x=200, y=450)

        comboM = ttk.Combobox(self, value = one_month_admin)
        comboM.current(0)
        #combo.bind("<<ComboboxSelected>>", comboclick)
        comboM.place(x=200, y=450) 

        comboY = ttk.Combobox(self, value = one_year_admin)
        comboY.current(0)
        #combo.bind("<<ComboboxSelected>>", comboclick)
        comboY.place(x=400, y=450)


        ########################## 1 year
        self.Earnings_1_year_label = tk.Label(self, text="Total Earnings in one year:", font=("Arial", 10)) 
        self.Earnings_1_year_label.place(x=200, y=600)
        

        #def comboclick(self,event):
            #tk.Label(self, text = combo.get()).place(x=600, y=450)
            
        only_year =["2022","2023"]
        self.clicked = tk.StringVar()
        self.clicked.set(only_year[0])
        # self.dropdown_menu = tk.OptionMenu(self, self.clicked, *only_year)
        # self.dropdown_menu.place(x=200, y=450)

        combo = ttk.Combobox(self, value = only_year)
        combo.current(0)
        #combo.bind("<<ComboboxSelected>>", comboclick)
        combo.place(x=200, y=650) 

       

if __name__ == "__main__":
    logged_in_user_id = None # no logged in user by default

    db = Database("reservation_system.db")

    root = App()

    # create main pages
    navbar = Navbar(root)
    home_page = HomePage(root)
    login_page = LoginPage(root)
    register_page = RegisterPage(root)
    admin_page = AdminPage(root)

    # add functionality to buttons
    navbar.home_btn.configure(command=home_page.show)
    navbar.login_btn.configure(command=login_page.show)
    navbar.logout_btn.configure(command=navbar.login_btn.tkraise)
    navbar.quit_btn.configure(command=root.destroy)
    navbar.admin_btn.configure(command =admin_page.tkraise)
    login_page.register_btn.configure(command=register_page.show)

    home_page.show()

    root.mainloop()
    db.close()
 