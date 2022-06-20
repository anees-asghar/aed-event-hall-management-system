import tkinter as tk
import tkcalendar as tkcal
from tkinter import messagebox
from tkinter import simpledialog


class HomePage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg="#F1EEE9")
        self.app = app # store the app instance
        # get event for the default date
        self.event = self.app.db.get_event_by_date("01/01/22") # event = (id, name, date)

        # put home_page inside app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # page title
        self.title_label = tk.Label(self, bg="#F1EEE9", text="Reserve Seats", font=("Helvetica", 30))
        self.title_label.place(relx=0.15, rely=0.10, relheight=0.06) 

        # event title label
        self.event_title_label = tk.Label(self, bg="#F1EEE9", font=("Helvetica", 13), text=f"{self.event[1]} | {self.event[2]}")
        self.event_title_label.place(relx=0.15, rely=0.20, relheight=0.06)


        # --- CALENDAR ---

        # calendar to pick date
        self.calendar = tkcal.Calendar(self, selectmode="day", date=1, month=1, year=2022, date_pattern="dd/mm/yy")
        self.calendar.place(relx=0.6, rely=0.10, relwidth=0.25, relheight=0.25)

        # select date button
        self.select_date_btn = tk.Button(self, text="Select Date", bg="#15133C", fg="white", 
            relief="flat", command=self.select_date)
        self.select_date_btn.place(relx=0.6, rely=0.355, relwidth=0.25, relheight=0.045)


        # error label
        self.error_label = tk.Label(self, text="", bg="#F1EEE9", fg="red", font=("Helvetica", 10))
        self.error_label.place(relx=0.15, rely=0.26, relheight=0.04)


        # --- SEAT GRID ---

        # seat grid legend frame
        legend = tk.Frame(self, bg="#F1EEE9")
        legend.place(relx=0.15, rely=0.3, relheight=0.13, relwidth=0.43)

        legend_btn_1 = tk.Button(legend, relief="flat", bg="#2AAA8A")
        legend_btn_1.place(relx=0, rely=0.125, relwidth=0.08, relheight=0.25)
        legend_label_1 = tk.Label(legend, text="Owned Seat", bg="#F1EEE9", font=("Helvetica", 9))
        legend_label_1.place(relx=0.1, rely=0.125, relheight=0.25)

        legend_btn_2 = tk.Button(legend, relief="flat", bg="white")
        legend_btn_2.place(relx=0.33, rely=0.125, relwidth=0.08, relheight=0.25)
        legend_label_2 = tk.Label(legend, text="Open Seat", bg="#F1EEE9", font=("Helvetica", 9))
        legend_label_2.place(relx=0.43, rely=0.125, relheight=0.25)

        legend_btn_3 = tk.Button(legend, relief="flat", bg="#DE3163")
        legend_btn_3.place(relx=0.67, rely=0.125, relwidth=0.08, relheight=0.25)
        legend_label_3 = tk.Label(legend, text="Reserved Seat", bg="#F1EEE9", font=("Helvetica", 9))
        legend_label_3.place(relx=0.77, rely=0.125, relheight=0.25)

        legend_btn_4 = tk.Button(legend, relief="flat", bg="#FFBF00")
        legend_btn_4.place(relx=0, rely=0.625, relwidth=0.08, relheight=0.25)
        legend_label_4 = tk.Label(legend, text="Selected Seat", bg="#F1EEE9", font=("Helvetica", 9))
        legend_label_4.place(relx=0.1, rely=0.625, relheight=0.25)

        legend_btn_5 = tk.Button(legend, relief="flat", bg="#F1EEE9", text="👑")
        legend_btn_5.place(relx=0.33, rely=0.625, relwidth=0.08, relheight=0.25)
        legend_label_5 = tk.Label(legend, text="VIP Seat", bg="#F1EEE9", font=("Helvetica", 9))
        legend_label_5.place(relx=0.43, rely=0.625, relheight=0.25)

        # create seat grid (hall)
        self.seat_grid = SeatGrid(self, self.app)
        self.seat_grid.place(relx=0.15, rely=0.45, relwidth=0.70, relheight=0.45)
        self.seat_grid.update()
        
        
        # price label
        self.price_label = tk.Label(self, bg="#F1EEE9", text="Normal Seat - 4€          VIP Seat - 12€")
        self.price_label.place(relx=0.15, rely=0.92, relwidth=0.49, relheight=0.05)

        # pick seats for me button
        self.pick_seats_btn = tk.Button(self, text="Pick Seats For Me", bg="#15133C", fg="white", 
            relief="flat", padx=12, command=self.seat_grid.auto_pick_seats)
        self.pick_seats_btn.place(relx=0.74, rely=0.92, relheight=0.05, anchor="ne")

        # book seats button
        self.book_seats_btn = tk.Button(self, text="Book", bg="#15133C", fg="white", 
            relief="flat", command=self.confirm_book_seats)
        self.book_seats_btn.place(relx=0.85, rely=0.92, relwidth=0.10, relheight=0.05, anchor="ne")


    def select_date(self):
        date = self.calendar.get_date() # get date from calendar

        # show error msg if no date is selected
        if not date:
            self.show("Please select a date.")
            return

        if self.event[2] == date: return # return if the same date was selected
        
        self.event = self.app.db.get_event_by_date(date) # update event
        self.event_title_label.configure(text=f"{self.event[1]} | {self.event[2]}") # update event label
        self.seat_grid.update() # update seat grid


    def confirm_book_seats(self):
        # show error msg if no seats are selected
        if not self.seat_grid.selected_seats:
            self.show("Please select seats in grid to reserve them.")
            return

        response = messagebox.askquestion(
            "Confirmation", 
            "Are you sure you want to book the selected seats?"
        )
        if response == "yes": self.book_selected_seats()


    def book_selected_seats(self):
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
        
        self.show() # refresh the home page


    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color) # set the error message (if any)
        self.seat_grid.update()                                    # update seat grid
        self.tkraise()                                             # raise home page


class SeatGrid(tk.Frame):
    def __init__(self, home_page, app):
        super().__init__(home_page, bg="#F1EEE9")
        self.app = app # store the app instance
        self.home_page = home_page # store the home_page instance
        self.seat_buttons = {} # seat numbers are keys and SeatButton instaces are values
        self.selected_seats = set() # the set of selected seats

        cols = [str(i) for i in range(1, 15)]
        rows = ['K', 'J', 'I', 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']
        
        for i, r in enumerate(rows):
            for j, c in enumerate(cols):
                seat_num = c+r # for example 1K

                # ignore invalid seats (seats that are not in hall)
                if seat_num in ['3F','4F','5F','10F','11F','12F','3A','4A','5A','10A','11A','12A']: continue 

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

                # place seat button in seat grid
                self.seat_buttons[seat_num].place(relx=rel_x, rely=rel_y, relwidth=0.065, relheight=0.085)
                
        # decorate VIP seats differently
        vip_seats = [seat_num for (_, seat_num, _) in self.app.db.select_seats_by_type("VIP")]
        for n in vip_seats:
            self.seat_buttons[n].configure(text="👑")

    def update(self):
        self.selected_seats.clear() # clear selected seats
        
        event_id = self.home_page.event[0] # extract the event id
        reservations = self.app.db.select_reservations_by_event_id(event_id) # get reservations for event
        logged_in_user_id = self.app.auth_manager.logged_in_user_id          # extract the logged in user id

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
                    bg="#2AAA8A",
                    fg="white",
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

    def auto_pick_seats(self):
        # ask user the number of seats to pick
        seat_count = simpledialog.askinteger(
            title="Picks Seats For Me", 
            prompt="Enter the number of seats to pick:"
        )

        event_id = self.home_page.event[0]                                   # extract the event id
        reservations = self.app.db.select_reservations_by_event_id(event_id) # get reservations for event
        reserved_seat_nums = [r[3] for r in reservations]                    # seats owned by other users
        valid_seat_nums = [s[1] for s in self.app.db.select_all_seats()]     # get all valid seat nums

        picked_seats = set() # set of seats picked by app

        # loop over the seat numbers to find seats open to book
        cols = [str(i) for i in range(1, 15)]
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

        for r in rows:
            for c in cols:
                seat_num = c + r
                if seat_num in valid_seat_nums and seat_num not in reserved_seat_nums: # seat is valid and open
                    picked_seats.add(seat_num)
                    if len(picked_seats) == seat_count: break # break if the count of seat requested is reached

            if len(picked_seats) == seat_count: break # break if the count of seat requested is reached

        # show error message if user requested more seats than total seats available
        if len(picked_seats) != seat_count:
            self.home_page.error_label.configure(
                text="Sorry, the requested number of seats aren't available."
            )
            return

        # update the seat buttons for the picked seat numbers (state selected)
        for s in picked_seats:
            # change seat button appearance and command
            self.seat_buttons[s].configure(
                bg="#FFBF00", 
                command=self.seat_buttons[s].change_to_open
            )
            self.selected_seats.add(s) # add seat number to selected


class SeatButton(tk.Button):
    def __init__(self, seat_grid, seat_num):
        super().__init__(seat_grid, text=seat_num, relief="flat")
        self.seat_num = seat_num   # store the seat number
        self.seat_grid = seat_grid # store the seat grid (parent)

    def change_to_selected(self):
        self.configure(bg="#FFBF00")                        # change button appearance
        self.configure(command=self.change_to_open)         # change button command
        self.seat_grid.selected_seats.add(self.seat_num)    # add seat number to selected
    
    def change_to_open(self):
        self.configure(bg="white")                          # change button appearance
        self.configure(command=self.change_to_selected)     # change button command
        self.seat_grid.selected_seats.remove(self.seat_num) # remove seat number from selected
