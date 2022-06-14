import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkcalendar as tkcal

class MyReservationsPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, width=1100, height=800)
        self.app = app

        # put home_page inside app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # get event for the default date
        self.event = self.app.db.get_event_by_date("01/01/22") # event = (id, name, date)

        # page title
        self.title_label = tk.Label(self, text="My Reservations", font=("Arial", 30))
        self.title_label.place(x=200, y=100)

        # event title label
        self.event_title_label = tk.Label(self, font=("Arial", 14), text=f"{self.event[1]} | {self.event[2]}")
        self.event_title_label.place(x=200, y=180)

        # calendar to pick date
        self.calendar = tkcal.Calendar(self, selectmode="day", date=1, month=1, year=2022, date_pattern="dd/mm/yy")
        self.calendar.place(x=650, y=100)

        # select date button
        self.select_date_btn = tk.Button(self, text="Select Date", command=self.select_date)
        self.select_date_btn.place(x=650, y=320)

        # error label
        self.error_label = tk.Label(self, text="", fg="red", font=("Arial"))
        self.error_label.place(x=200, y=360) 

        # create seat grid (hall layout)
        self.seat_grid = SeatGrid(self, self.app)
        self.seat_grid.place(x=200, y=400)
        self.seat_grid.update()

        # book seats button
        self.update_seat_label = tk.Label(self, text="New seat number:")
        self.update_seat_label.place(x=400, y=750)

        self.all_seat_nums = [s[1] for s in  self.app.db.select_all_seats()]
        self.update_seat_num_combo = ttk.Combobox(self, width=20, value=self.all_seat_nums, state="readonly")
        self.update_seat_num_combo.current(0)
        self.update_seat_num_combo.place(x=600, y=750)
    
        self.update_seat_num_btn = tk.Button(self, text="Update", width=7, height=1, bg="#A52A2A", fg="white", 
            command=self.update_reservation)
        self.update_seat_num_btn.place(x=800, y=750)

        self.delete_seat_btn = tk.Button(self, text="Unbook", width=7, height=1, bg="#A52A2A", fg="white", 
            command=self.delete_reservation)
        self.delete_seat_btn.place(x=900, y=750)

    def select_date(self):
        date = self.calendar.get_date() # get date from calendar

        # CHECK TO SEE IF A VALID DATE IS SELECTED
        if self.event[2] == date: return # return if the same date was selected
        
        self.event = self.app.db.get_event_by_date(date) # update event
        self.event_title_label.configure(text=f"{self.event[1]} | {self.event[2]}") # update event label
        self.seat_grid.update() # update seat grid

    def delete_reservation(self):
        selected_seat_num = self.seat_grid.selected_seat_num

        # show error message if no seat is selected
        if not selected_seat_num:
            self.show("Please select a seat to unbook.")
            return

        # get user confirmation
        question = messagebox.askquestion(
            "Delete", f'Are you sure you want to unbook the seat "{selected_seat_num}"?'
        )
        if question == "no": return

        # deleter reservation from db
        self.app.db.delete_reservation(self.event[0], selected_seat_num)

        self.show() # update my res page

    def update_reservation(self):
        selected_seat_num = self.seat_grid.selected_seat_num

        # show error message if no seat is selected
        if not selected_seat_num:
            self.show("Please select a seat to edit.")
            return
            
        new_seat_num = self.update_seat_num_combo.get()

        # get user confirmation
        question = messagebox.askquestion(
            "Edit", f"Are you sure you want to update the seat {selected_seat_num} to {new_seat_num}?"
            )
        if question == "no": return
        
        if not selected_seat_num or new_seat_num == '-':
            return
        
        try:
            self.app.db.update_reservation(self.event[0], selected_seat_num, new_seat_num)
            self.show()
        except:
            self.show(f"Seat {new_seat_num} is already booked.")

    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color) # set the error message (if any)
        self.seat_grid.update()                                    # update seat grid
        self.tkraise()                                             # raise home page


class SeatButton(tk.Button):
    def __init__(self, seat_grid, seat_num):
        super().__init__(seat_grid, text=seat_num, width=5, height=1)
        self.seat_num = seat_num
        self.seat_grid = seat_grid

    def change_to_selected(self):        
        curr_selected_seat_num = self.seat_grid.selected_seat_num # seat number that is currently selected
                
        if curr_selected_seat_num: # if a seat number is already selected
            # access the button for this seat number
            curr_selected_seat_btn = self.seat_grid.seat_buttons[curr_selected_seat_num]
            # change the appearance and commandd of this seat button back to normal
            curr_selected_seat_btn.configure(
                bg="green",
                fg="white",
                command=curr_selected_seat_btn.change_to_selected
            )
        
        self.configure(bg="yellow", fg="black")             # change button appearance
        self.configure(command=self.change_to_unselected)   # change button command
        self.seat_grid.selected_seat_num = self.seat_num    # add seat number to selected
    
    def change_to_unselected(self):
        self.configure(bg="green", fg="white")              # change button appearance
        self.configure(command=self.change_to_selected)     # change button command
        self.seat_grid.selected_seat_num = ""               # remove seat number from selected


class SeatGrid(tk.Frame):
    def __init__(self, my_res_page, app):
        super().__init__(my_res_page, width=400, height=200)
        self.app = app
        self.my_res_page = my_res_page
        self.seat_buttons = {} # seat numbers are keys and SeatButton instaces are values
        self.selected_seat_num = "" # seat number selected by user

        cols = [str(i) for i in range(1, 15)]
        rows = ['K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        
        for i, r in enumerate(rows):
            for j, c in enumerate(cols):
                seat_num = c+r # for example 1K

                # ignore invalid seats (seats that are not in hall)
                if seat_num in ['3F','4F','5F','10F','11F','12F','3A','4A','5A','10A','11A','12A']: continue 

                # create a button for this seat number
                self.seat_buttons[seat_num] = SeatButton(self, seat_num)

                # place the button created in the grid
                # there are gaps between some rows and cols in hall layout for which we use padx & pady
                if c in ['2', '12'] and r in ['B', 'F']: # row spacing and column spacing needed
                    self.seat_buttons[seat_num].grid(row=i, column=j, padx=(0, 20), pady=(0, 20))

                elif c in ['2', '12']: # only column spacing needed
                    self.seat_buttons[seat_num].grid(row=i, column=j, padx=(0, 20))

                elif r in ['B', 'F']: # only row spacing needed
                    self.seat_buttons[seat_num].grid(row=i, column=j, pady=(0, 20))

                else: # no spacing needed
                    self.seat_buttons[seat_num].grid(row=i, column=j)

    def update(self):
        self.selected_seat_num = "" # clear selected seats
        
        event_id = self.my_res_page.event[0] # extract the event id
        reservations = self.app.db.select_reservations_by_event_id(event_id) # get reservations for event
        logged_in_user_id = self.app.auth_manager.logged_in_user_id # extract the logged in user id

        owned_seat_nums = []    # seats owned by user
        reserved_seat_nums = [] # seats owned by other users

        # fill the lists above
        for _, user_id, _, seat_num in reservations:
            if user_id == logged_in_user_id: owned_seat_nums.append(seat_num)
            else: reserved_seat_nums.append(seat_num)

        # give the SeatButton for each seat number different properties based on its status
        for seat_num in self.seat_buttons.keys():
            # if owned by user
            if seat_num in owned_seat_nums:
                self.seat_buttons[seat_num].configure(
                    bg="green",
                    fg="white",
                    state="normal",
                    command=self.seat_buttons[seat_num].change_to_selected
                )
            # if owned by some other user
            elif seat_num in reserved_seat_nums:
                self.seat_buttons[seat_num].configure(
                    bg="red",
                    fg="white",
                    state="disabled",
                    command=lambda: None
                )
            else:
                self.seat_buttons[seat_num].configure(
                    bg="white",
                    fg="black",
                    state="disabled",
                    command=lambda: None
                )
