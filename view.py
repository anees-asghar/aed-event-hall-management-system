import tkinter as tk
import tkcalendar as tkcal
from database import Database
from tkinter import ttk


class AuthManager:
    def __init__(self, db):
        self.db = db
        self.logged_in_user_id = None

    def authenticate_user(self, email, password):
        user = self.db.select_user_by_email_password(email, password) # get user with this email and password
        if user: # if such a user exists return their user id
            return user[0]  # user[0] == user id
        return None # if such a user doesn't exist return None
    
    def login_user(self, email, password):
        user_id = self.authenticate_user(email, password)
        if user_id:
            self.logged_in_user_id = user_id # set logged in user id
            return True
        else:
            return False

    def logout_user(self):
        self.logged_in_user_id = None # set logged in used id to none
        home_page.show() # redirect to home page
        navbar.show_login_btn() # show login button in navbar instead of logout

    def register_user(self, first_name, last_name, email, password):
        # check if user with this email exists
        user = self.db.select_user_by_email(email)
        if user: return False

        # register user
        self.db.insert_user(first_name, last_name, email, password)
        return True


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

        self.admin_btn = tk.Button(self, text ="Admin Page", width=37, height=2, bg="#A52A2A", fg="white")
        self.admin_btn.grid(row=3)

        self.my_reservations_btn = tk.Button(self, text ="My Reservations", width=37, height=2, bg="#A52A2A", fg="white")
        self.my_reservations_btn.grid(row=4)

    def show_login_btn(self):
        self.login_btn.tkraise()

    def show_logout_btn(self):
        self.logout_btn.tkraise()


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
        self.empty_seat_btn = tk.Button(self, text="", width=5, height=1, bg="white",state="disabled")
        self.empty_seat_btn.place(x=300, y=230)
    
        self.seat_taken_label = tk.Label(self, text="Seat Taken", font=("Georgia"))#seat takenlabel
        self.seat_taken_label.place(x=200, y=260) 
        self.seat_taken_btn = tk.Button(self, text="", width=5, height=1, bg="red",state="disabled")
        self.seat_taken_btn.place(x=300, y=260)
    
        self.chosen_seat_label = tk.Label(self, text="Chosen seat", font=("Georgia"))#chosen seat label
        self.chosen_seat_label.place(x=200, y=290) 
        self.chosen_seat_btn = tk.Button(self, text="", width=5, height=1, bg="green",state="disabled")
        self.chosen_seat_btn.place(x=300, y=290)

        self.vip_seat_label = tk.Label(self, text="VIP seat", font=("Georgia"))#vip seat label
        self.vip_seat_label.place(x=200, y=320)
        self.vip_seat_btn = tk.Button(self, text="👑", width=5, height=1,state="disabled")
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
        
        logged_in_user_id = auth_manager.logged_in_user_id
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

        logged_in_user_id = auth_manager.logged_in_user_id
        reservations = db.select_reservations_by_date(date)
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
        
        success = auth_manager.login_user(email, password)
        if success:
            home_page.show() # redirect user to home page
            navbar.show_logout_btn() # show logout button instead of login 
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

        success = auth_manager.register_user(first_name, last_name, email, password)

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
        self.grid_propagate(False)

        self.title_label = tk.Label(self, text="Admin Page", font=("Arial", 30)) # admin page title
        self.title_label.place(x=200, y=100)

        self.sales_by_label = tk.Label(self, text="Sales by:", font=("Arial", 20)) 
        self.sales_by_label.place(x=200, y=200)

        #Drop down menu for earnings
        self.days_admin = [(str(i) if i >= 10 else '0' + str(i)) for i in range(1, 32)]
        self.months_admin = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.years_admin = ["2022","2023"]

      
        self.days_clicked = ttk.Combobox(self, value = self.days_admin) #command=
        self.days_clicked.current(0)
        #combo.bind("<<ComboboxSelected>>", comboclick)
        self.days_clicked.place(x=200, y=350)

        self.month_clicked = ttk.Combobox(self, value = self.months_admin)
        self.month_clicked.current(0)
        #combo.bind("<<ComboboxSelected>>", comboclick)
        self.month_clicked.place(x=400, y=350)
        
        self.year_clicked = ttk.Combobox(self, value = self.years_admin)
        self.year_clicked.current(0)
        #combo.bind("<<ComboboxSelected>>", comboclick)
        self.year_clicked.place(x=600, y=350)

   
        #Radio buttons
        
        self.radio_button_value = tk.IntVar()

        self.radio_day_btn = tk.Radiobutton ( self,variable = self.radio_button_value,value = 0, text="Day",command = self.day_radio_selected)
        self.radio_day_btn.place(x=200, y =300)

        self.radio_month_btn = tk.Radiobutton ( self,variable = self.radio_button_value,value = 1, text="Month",command = self.month_radio_selected)
        self.radio_month_btn.place(x=400, y =300)

        self.radio_year_btn = tk.Radiobutton ( self,variable = self.radio_button_value,value = 2, text="Year" ,command = self.year_radio_selected)
        self.radio_year_btn.place (x=600, y = 300)
        
        self.submit_date_btn = tk.Button(self,text= "Submit", command=self.submit)
        self.submit_date_btn.place (x=800, y = 300)

        self.date_label = tk.Label(self, text="On 22 Jan 2022")
        self.date_label.place(x=200, y=450)

        self.tickets_sold_label = tk.Label(self, text="Tickets sold: 342")
        self.tickets_sold_label.place(x=400, y=450)

        self.tickets_value_label = tk.Label(self, text="Total Value: 4500$")
        self.tickets_value_label.place(x=600, y=450)
       

    def submit(self):
        radio_option_selected = self.radio_button_value.get()

        day = self.days_clicked.get() #get the value of the days_clicked
        month = self.month_clicked.get()
        year = self.year_clicked.get()

        if radio_option_selected == 0: # user requested data by date
            month_num = self.months_admin.index(month)+1
            month_num = str(month_num) if month_num >= 10 else '0' + str(month_num)
            date = f"{day}/{month_num}/{year[-2:]}"

            reservations = db.select_reservations_by_date(date)

            vip_seats = ["6F", "7F", "8F", "9F", "6A", "7A", "8A", "9A"]
            total_tickets_sold = len(reservations)
            total_tickets_value = 0

            for r in reservations:
                if r[-1] in vip_seats: # r[-1] = seat number of the reservation
                    total_tickets_value += 12
                else:
                    total_tickets_value += 4

            # show data on the page
            self.date_label.configure(text=f"On {day} {month} {year}")
            self.tickets_sold_label.configure(text=f"Tickets sold: {total_tickets_sold}")
            self.tickets_value_label.configure(text=f"Total Value: {total_tickets_value}$")

        elif radio_option_selected == 1: # user requested data by month

            month_num = self.months_admin.index(month)+1
            month_num = str(month_num) if month_num >= 10 else '0' + str(month_num)
            year_abbr = year[-2:]

            reservations = db.select_reservations_by_month(month=month_num, year=year_abbr)

            vip_seats = ["6F", "7F", "8F", "9F", "6A", "7A", "8A", "9A"]
            total_tickets_sold = len(reservations)
            total_tickets_value = 0

            for r in reservations:
                if r[-1] in vip_seats: # r[-1] = seat number of the reservation
                    total_tickets_value += 12
                else:
                    total_tickets_value += 4

            self.date_label.configure(text=f"On {month} {year}")
            self.tickets_sold_label.configure(text=f"Tickets sold: {total_tickets_sold}")
            self.tickets_value_label.configure(text=f"Total Value: {total_tickets_value}$")

        elif radio_option_selected == 2: # user requested data by year
            year_abbr = year[-2:]

            reservations = db.select_reservations_by_year(year=year_abbr)

            vip_seats = ["6F", "7F", "8F", "9F", "6A", "7A", "8A", "9A"]
            total_tickets_sold = len(reservations)
            total_tickets_value = 0

            for r in reservations:
                if r[-1] in vip_seats: # r[-1] = seat number of the reservation
                    total_tickets_value += 12
                else:
                    total_tickets_value += 4

            self.date_label.configure(text=f"On {year}")
            self.tickets_sold_label.configure(text=f"Tickets sold: {total_tickets_sold}")
            self.tickets_value_label.configure(text=f"Total Value: {total_tickets_value}$")
           
    def day_radio_selected(self):
        self.days_clicked.configure(state="enabled")
        self.month_clicked.configure(state="enabled")
        self.year_clicked.configure(state="enabled")

    def month_radio_selected(self):
        self.days_clicked.configure(state="disabled")
        self.month_clicked.configure(state="enabled")
        self.year_clicked.configure(state="enabled")

    def year_radio_selected(self):
        self.days_clicked.configure(state="disabled")
        self.month_clicked.configure(state="disabled")
        self.year_clicked.configure(state="enabled")


class MyReservationsPage(tk.Frame):
    def __init__(self, container):
        super().__init__(container, width=1100, height=800)
        self.selected_date = '01/01/22'
        self.normal_open_seats = []
        self.vip_open_seats = []

        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.select_seat_grid = self.SelectSeatGrid(self)
        self.select_seat_grid.place(x=200, y=200)
        self.select_seat_grid.render(self.selected_date)

        self.edit_seat_label = tk.Label(self, text="New Seat Number:")
        self.edit_seat_label.place(x=400, y=750)
        self.edit_seat_entry = tk.Entry(self, width=20)
        self.edit_seat_entry.place(x=600, y=750)
    
        self.edit_btn = tk.Button(self, text="Edit", width=7, height=1, bg="#A52A2A", fg="white", 
            command=self.edit_reservation)
        self.edit_btn.place(x=800, y=750)

        self.delete_btn = tk.Button(self, text="Delete", width=7, height=1, bg="#A52A2A", fg="white", 
            command=self.delete_reservation)
        self.delete_btn.place(x=900, y=750)
    
    def delete_reservation(self):
        selected_seat_num = self.select_seat_grid.selected_seat
        if not selected_seat_num:
            self.show("Please select a seat to delete.")
            return
        db.delete_reservation(self.selected_date, self.select_seat_grid.selected_seat)
        self.show()

    def edit_reservation(self):
        old_seat_num = self.select_seat_grid.selected_seat
        new_seat_num = self.edit_seat_entry.get()
        db.update_reservation(self.selected_date, old_seat_num, new_seat_num)
        self.show()

    def show(self, message="", message_color="red"):

        self.select_seat_grid.render(self.selected_date) # re-render the select seat grid
        self.edit_seat_entry.delete(0, 'end') # clear the edit seat entry field
        self.tkraise() # raise the my reservations page

    class SelectSeatGrid(tk.Frame):
        def __init__(self, container):
            super().__init__(container, width=400, height=200)
            self.buttons = {} # button of a particular seat can be accessed by self.buttons[<seat_number>]
            self.selected_seat = ""
        
        def render(self, date):
            self.selected_seat = "" # clear selected seats when grid is re-rendered

            logged_in_user_id = auth_manager.logged_in_user_id
            reservations = db.select_reservations_by_date(date)
            user_seats = [r[3] for r in reservations if r[1] == logged_in_user_id] # r[1] == user_id and r[3] == seat_num

            cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12','13','14']
            rows = ['K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
            seats_to_ignore = ['3F','4F','5F','10F','11F','12F','3A','4A','5A','10A','11A','12A'] # seats that dont exist in the hall
            
            for i, r in enumerate(rows):
                for j, c in enumerate(cols):
                    seat_num = c+r # for example 1A
                    
                    if seat_num in seats_to_ignore: # ignore the seat_num for which button isn't needed
                        continue 

                    if seat_num in user_seats: # if the seat is reserved
                        self.buttons[seat_num] = self.OwnedSeatButton(self, seat_num)
                    else: # if the seat is not reserved
                        self.buttons[seat_num] = self.DisabledSeatButton(self, seat_num)

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
            
        class OwnedSeatButton(tk.Button):
            def __init__(self, container, seat_num):
                super().__init__(container, text=seat_num, width=5, height=1, bg="green", 
                    command=self.change_to_selected)
                self.seat_num = seat_num
                self.container = container

            def change_to_selected(self):
                curr_selected_seat_num = self.container.selected_seat # seat number that is currently selected
                
                if curr_selected_seat_num: # if a seat number is already selected
                    # access the button for this seat number
                    curr_selected_seat_btn = self.container.buttons[curr_selected_seat_num]
                    # change the appearance and commandd of this seat button back to normal
                    curr_selected_seat_btn.configure(
                        bg="green",
                        command=curr_selected_seat_btn.change_to_selected
                    )
                
                self.configure(bg="yellow") # change button appearance
                self.configure(command=self.change_to_unselected) # change button command

                self.container.selected_seat = self.seat_num # set selected_seat in seat grid
            
            def change_to_unselected(self):
                self.configure(bg="green") # change button appearance
                self.configure(command=self.change_to_selected) # change button command

                self.container.selected_seat = "" # reset selected seat in seat grid
            
        class DisabledSeatButton(tk.Button):
            def __init__(self, container, seat_num):
                super().__init__(container, text=seat_num, width=5, height=1, bg="white", state="disabled")


if __name__ == "__main__":
    logged_in_user_id = None # no logged in user by default

    db = Database("reservation_system.db")
    auth_manager = AuthManager(db)

    root = App()

    # create main pages
    navbar = Navbar(root)
    home_page = HomePage(root)
    login_page = LoginPage(root)
    register_page = RegisterPage(root)
    admin_page = AdminPage(root)
    my_reservations_page = MyReservationsPage(root)
    
    # add functionality to buttons
    navbar.home_btn.configure(command=home_page.show)
    navbar.login_btn.configure(command=login_page.show)
    navbar.logout_btn.configure(command=auth_manager.logout_user)
    navbar.admin_btn.configure(command =admin_page.tkraise)
    navbar.my_reservations_btn.configure(command=my_reservations_page.show)
    navbar.quit_btn.configure(command=root.destroy)
    login_page.register_btn.configure(command=register_page.show)

    my_reservations_page.tkraise()

    root.mainloop()
    db.close()
 