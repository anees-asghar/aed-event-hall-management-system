import tkinter as tk
import tkcalendar as tkcal
from tkinter import messagebox


class HomePage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg="#F1EEE9")
        self.app = app

        # put home_page inside app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # get event for the default date
        self.event = self.app.db.get_event_by_date("01/01/22") # event = (id, name, date)

        # page title
        self.title_label = tk.Label(self, bg="#F1EEE9", text="Reserve Seats", font=("Helvetica", 30))
        self.title_label.place(relx=0.15, rely=0.10, relheight=0.06) 

        # event title label
        self.event_title_label = tk.Label(self, bg="#F1EEE9", font=("Helvetica", 14), text=f"{self.event[1]} | {self.event[2]}")
        self.event_title_label.place(relx=0.15, rely=0.20, relheight=0.06)

        # calendar to pick date
        self.calendar = tkcal.Calendar(self, selectmode="day", date=1, month=1, year=2022, date_pattern="dd/mm/yy")
        self.calendar.place(relx=0.6, rely=0.10, relwidth=0.25, relheight=0.25)

        # select date button
        self.select_date_btn = tk.Button(self, text="Select Date", bg="#15133C", fg="white", 
            relief="flat", command=self.select_date)
        self.select_date_btn.place(relx=0.6, rely=0.355, relwidth=0.25, relheight=0.045)

        # create seat grid (hall)
        self.seat_grid = SeatGrid(self, self.app)
        self.seat_grid.place(relx=0.15, rely=0.45, relwidth=0.70, relheight=0.45)
        self.seat_grid.update()

        # book seats button
        self.book_seats_btn = tk.Button(self, text="Book", bg="#15133C", fg="white", 
            relief="flat", command=self.confirm_book_seats)
        self.book_seats_btn.place(relx=0.85, rely=0.92, relwidth=0.10, relheight=0.05, anchor="ne")

    def select_date(self):
        date = self.calendar.get_date() # get date from calendar

        # CHECK TO SEE IF A VALID DATE IS SELECTED
        if self.event[2] == date: return # return if the same date was selected
        
        self.event = self.app.db.get_event_by_date(date) # update event
        self.event_title_label.configure(text=f"{self.event[1]} | {self.event[2]}") # update event label
        self.seat_grid.update() # update seat grid

    def confirm_book_seats(self):
        response = messagebox.askquestion(
            "Confirmation", 
            "Are you sure you want to book the selected seats?"
            )
        if response == "yes": self.book_selected_seats()

    def book_selected_seats(self):
        # ADD AN ERROR MESSAGE IF NO SEATS ARE SELECTED
        if not self.seat_grid.selected_seats: return # return if no seats are selected
        
        user_id = self.app.auth_manager.logged_in_user_id # get logged in user id
        
        if not user_id: # no user is logged in
            self.app.login_page.show(message="Please login first.") # redirect to login page with message
            return

        # make reservations for the selected seats
        self.app.db.insert_reservations(
            user_id, 
            event_id=self.event[0], 
            seat_nums=self.seat_grid.selected_seats
        )
        
        self.seat_grid.update() # update seat grid

    def show(self):
        self.seat_grid.update() # update seat grid
        self.tkraise()          # raise home page


class SeatButton(tk.Button):
    def __init__(self, seat_grid, seat_num):
        super().__init__(seat_grid, text=seat_num, relief="flat", width=5, height=1)
        self.seat_num = seat_num
        self.seat_grid = seat_grid

    def change_to_selected(self):
        self.configure(bg="yellow")                         # change button appearance
        self.configure(command=self.change_to_open)         # change button command
        self.seat_grid.selected_seats.add(self.seat_num)    # add seat number to selected
    
    def change_to_open(self):
        self.configure(bg="white")                          # change button appearance
        self.configure(command=self.change_to_selected)     # change button command
        self.seat_grid.selected_seats.remove(self.seat_num) # remove seat number from selected


class SeatGrid(tk.Frame):
    def __init__(self, home_page, app):
        super().__init__(home_page, bg="#F1EEE9")
        self.app = app
        self.home_page = home_page
        self.seat_buttons = {} # seat numbers are keys and SeatButton instaces are values
        self.selected_seats = set() # the set of selected seats

        cols = [str(i) for i in range(1, 15)]
        rows = ['K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        offset_x = 0
        offset_y = 0
        
        for i, r in enumerate(rows):
            for j, c in enumerate(cols):
                seat_num = c+r # for example 1K

                # ignore invalid seats (seats that are not in hall)
                if seat_num in ['3F','4F','5F','10F','11F','12F','3A','4A','5A','10A','11A','12A']: continue 

                # if c in ['2', '12']: offset_y += 0.045

                # create a button for this seat number
                self.seat_buttons[seat_num] = SeatButton(self, seat_num)

                # calculate the relative x coordinate for this seat button within seat grid
                if j >= 2:
                    if j >= 12: rel_x = j * 0.065 + 0.09
                    else: rel_x = j * 0.065 + 0.045
                else:
                    rel_x = j * 0.065
                
                # calculate the relative x coordinate for this seat button within seat grid
                if i >= 6:
                    rel_y = i * 0.085 + 0.065
                else:
                    rel_y = i * 0.085


                self.seat_buttons[seat_num].place(relx=rel_x, rely=rel_y, relwidth=0.065, relheight=0.085)

                # place the button created in the grid
                # there are gaps between some rows and cols in hall layout for which we use padx & pady
                # if c in ['2', '12'] and r in ['B', 'F']: # row spacing and column spacing needed
                #     self.seat_buttons[seat_num].grid(row=i, column=j, padx=(0, 20), pady=(0, 20))

                # elif c in ['2', '12']: # only column spacing needed
                #     self.seat_buttons[seat_num].grid(row=i, column=j, padx=(0, 20))

                # elif r in ['B', 'F']: # only row spacing needed
                #     self.seat_buttons[seat_num].grid(row=i, column=j, pady=(0, 20))

                # else: # no spacing needed
                #     self.seat_buttons[seat_num].grid(row=i, column=j)
                
        # decorate VIP seats differently
        vip_seats = [seat_num for (_, seat_num, _) in self.app.db.select_seats_by_type("VIP")]
        for n in vip_seats:
            self.seat_buttons[n].configure(text="👑")

    def update(self):
        self.selected_seats.clear() # clear selected seats
        
        event_id = self.home_page.event[0] # extract the event id
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
                    bg="#9FE2BF",
                    fg="black",
                    command=lambda: None
                )
            # if owned by some other user
            elif seat_num in reserved_seat_nums:
                self.seat_buttons[seat_num].configure(
                    bg="#DE3163",
                    fg="white",
                    command=lambda: None
                )
            # if open to book
            else:
                self.seat_buttons[seat_num].configure(
                    bg="white",
                    fg="black",
                    command=self.seat_buttons[seat_num].change_to_selected
                )
