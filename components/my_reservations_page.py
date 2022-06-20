import tkinter as tk
from tkinter import messagebox
import tkcalendar as tkcal
from tkinter import simpledialog

class MyReservationsPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg="#F1EEE9")
        self.app = app # store app instance

        # put home_page inside app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # get event for the default date
        self.event = self.app.db.get_event_by_date("01/01/22") # event = (id, name, date)

        # page title
        self.title_label = tk.Label(self, bg="#F1EEE9", text="My Reservations", font=("Helvetica", 30))
        self.title_label.place(relx=0.15, rely=0.10, relheight=0.06)

        # event title label
        self.event_title_label = tk.Label(self, bg="#F1EEE9", font=("Helvetica", 13), text=f"{self.event[1]} | {self.event[2]}")
        self.event_title_label.place(relx=0.15, rely=0.20, relheight=0.06)

        # calendar to pick date
        self.calendar = tkcal.Calendar(self, selectmode="day", date=1, month=1, year=2022, date_pattern="dd/mm/yy")
        self.calendar.place(relx=0.6, rely=0.10, relwidth=0.25, relheight=0.25)

        # select date button
        self.select_date_btn = tk.Button(self, text="Select Date", bg="#15133C", fg="white", 
            relief="flat", command=self.select_date)
        self.select_date_btn.place(relx=0.6, rely=0.355, relwidth=0.25, relheight=0.045)

        # # error label
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

        # create seat grid (hall layout)
        self.seat_grid = SeatGrid(self, self.app)
        self.seat_grid.place(relx=0.15, rely=0.45, relwidth=0.70, relheight=0.45)
        self.seat_grid.update()


        # help label
        self.help_label = tk.Label(self, bg="#F1EEE9", text="Please select a reservation (green) to edit or delete it.")
        self.help_label.place(relx=0.15, rely=0.92, relwidth=0.49, relheight=0.05)

        # edit reservation button
        self.edit_btn = tk.Button(self, text="Edit", bg="#15133C", fg="white", 
            relief="flat", command=self.edit_reservation)
        self.edit_btn.place(relx=0.74, rely=0.92, relwidth=0.10, relheight=0.05, anchor="ne")

        # delete reservation button
        self.delete_btn = tk.Button(self, text="Delete", bg="#D2042D", fg="white", 
            relief="flat", command=self.delete_reservation)
        self.delete_btn.place(relx=0.85, rely=0.92, relwidth=0.10, relheight=0.05, anchor="ne")


    def select_date(self):
        date = self.calendar.get_date() # get date from calendar

        # if no date chosen
        if not date:
            self.show("Please select a date.")
            return

        if self.event[2] == date: return # return if the same date was selected
        
        self.event = self.app.db.get_event_by_date(date) # update event
        self.event_title_label.configure(text=f"{self.event[1]} | {self.event[2]}") # update event label
        self.seat_grid.update() # update seat grid


    def delete_reservation(self):
        selected_seat_num = self.seat_grid.selected_seat_num

        # show error message if no seat is selected
        if not selected_seat_num:
            self.show("Please select a reservation to delete.")
            return

        # get user confirmation
        question = messagebox.askquestion(
            "Delete", f'Are you sure you want to delete the reservation for seat "{selected_seat_num}"?'
        )
        if question == "no": return

        # delete reservation from db
        self.app.db.delete_reservation(self.event[0], selected_seat_num)

        self.show() # update my res page


    def edit_reservation(self):
        selected_seat_num = self.seat_grid.selected_seat_num

        # show error message if no seat is selected
        if not selected_seat_num:
            self.show("Please select a reservation to edit.")
            return

        # get new seat number from user
        new_seat_num = simpledialog.askstring(title="Change Reservation", prompt="Enter the new seat number:")

        # get all normal and vip seats from db
        normal_seats = [s[1] for s in self.app.db.select_seats_by_type('Normal')]
        vip_seats = [s[1] for s in self.app.db.select_seats_by_type('VIP')]
        
        # show error msg if user input is not a valid seat number
        if new_seat_num not in normal_seats + vip_seats:
            self.show("Please enter a valid seat number.")
            return
        
        # show error msg if user tries to change from normal to vip seat
        if selected_seat_num in normal_seats and new_seat_num in vip_seats:
            self.show("Cannot edit seat number from a Normal to a VIP seat.")
            return
        
        # show error msg if user tries to change from vip to normal seat
        if selected_seat_num in vip_seats and new_seat_num in normal_seats:
            self.show("Cannot edit seat number from a VIP to a Normal seat.")
            return
        
        try: # if successfully updated
            self.app.db.update_reservation(self.event[0], selected_seat_num, new_seat_num)
            self.show()
        except: # if seat is already booked
            self.show(f"Seat {new_seat_num} is already booked.")


    def show(self, message="", message_color="red"):
        self.error_label.configure(text=message, fg=message_color) # set the error message (if any)
        self.seat_grid.update()                                    # update seat grid
        self.tkraise()                                             # raise home page


class SeatButton(tk.Button):
    def __init__(self, seat_grid, seat_num):
        super().__init__(seat_grid, text=seat_num, relief="flat")
        self.seat_num = seat_num
        self.seat_grid = seat_grid

    def change_to_selected(self):        
        curr_selected_seat_num = self.seat_grid.selected_seat_num # seat number that is currently selected
                
        if curr_selected_seat_num: # if a seat number is already selected
            # access the button for this seat number
            curr_selected_seat_btn = self.seat_grid.seat_buttons[curr_selected_seat_num]
            # change the appearance and command of this seat button back to normal
            curr_selected_seat_btn.configure(
                bg="#2AAA8A",
                fg="white",
                command=curr_selected_seat_btn.change_to_selected
            )
        
        self.configure(bg="#FFBF00", fg="black")             # change button appearance
        self.configure(command=self.change_to_unselected)   # change button command
        self.seat_grid.selected_seat_num = self.seat_num    # add seat number to selected
    
    def change_to_unselected(self):
        self.configure(bg="#2AAA8A", fg="white")              # change button appearance
        self.configure(command=self.change_to_selected)     # change button command
        self.seat_grid.selected_seat_num = ""               # remove seat number from selected


class SeatGrid(tk.Frame):
    def __init__(self, my_res_page, app):
        super().__init__(my_res_page, bg="#F1EEE9")
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
                    bg="#2AAA8A",
                    fg="white",
                    command=self.seat_buttons[seat_num].change_to_selected
                )
            # if owned by some other user
            elif seat_num in reserved_seat_nums:
                self.seat_buttons[seat_num].configure(
                    bg="#DE3163",
                    fg="white",
                    command=lambda: None
                )
            # unreserved seats
            else:
                self.seat_buttons[seat_num].configure(
                    bg="white",
                    fg="black",
                    command=lambda: None
                )
