import tkinter as tk
import tkcalendar as tkcal
from tkinter import ttk
from tkinter import messagebox

class HomePage(tk.Frame):
    def __init__(self, container):
        super().__init__(container, width=1100, height=800)

        self.container = container
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

        self.book_seats_btn = tk.Button(self, text="Book", width=7, height=1, bg="#A52A2A", fg="white", command=self.booking_popup)
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

    def booking_popup(self):
        question = messagebox.askquestion("Confirmation","Are you sure you want to buy this ticket/s?")
        if question == "yes": self.book_selected_seats()  
           

    def select_date(self):
        if self.selected_date == self.calendar.get_date():
            return
        
        self.selected_date = self.calendar.get_date()
        self.selected_date_label.configure(text=f"Selected date: {self.selected_date}")
        self.seat_grid.render(self.selected_date)

    def book_selected_seats(self):
        if not self.seat_grid.selected_seats:
            return
        
        logged_in_user_id = self.container.auth_manager.logged_in_user_id
        if not logged_in_user_id: # no user is logged in
            self.container.login_page.show(message="Please login first.", message_color="green")
            return
        
        self.container.db.insert_reservations(logged_in_user_id, self.selected_date, self.seat_grid.selected_seats)
        self.seat_grid.render(self.selected_date)

    def show(self):
        self.seat_grid.render(self.selected_date)
        self.tkraise()
        

class SeatGrid(tk.Frame):
    def __init__(self, container):
        super().__init__(container, width=400, height=200)
        self.container = container
        self.buttons = {} # button of a particular seat can be accessed by self.buttons[<seat_number>]
        self.selected_seats = set()
    
    def render(self, date):
        self.selected_seats.clear() # clear selected seats when grid is re-rendered

        logged_in_user_id = self.container.container.auth_manager.logged_in_user_id
        reservations = self.container.container.db.select_reservations_by_date(date)
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
            super().__init__(container, text=seat_num, width=5, height=1, bg="red", fg="white")

    class OwnedSeatButton(tk.Button):
        def __init__(self, container, seat_num):
            super().__init__(container, text=seat_num, width=5, height=1, bg="green", fg="white")