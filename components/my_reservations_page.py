import tkinter as tk
from database import Database
from tkinter import ttk
from tkinter import messagebox
import tkcalendar as tkcal

class MyReservationsPage(tk.Frame):
    def __init__(self, container):
        super().__init__(container, width=1100, height=800)
        self.container = container
        self.selected_date = '01/01/22'

        self.grid(row=0, column=1)
        self.grid_propagate(False)

        self.selected_date_label = tk.Label(self, text=f"Selected date: {self.selected_date}", font=("Arial", 14))
        self.selected_date_label.place(x=400, y=80)

        self.calendar = tkcal.Calendar(self, selectmode="day", date=1, month=1, year=2022, date_pattern="dd/mm/yy")# home page calendar
        self.calendar.place(x=650, y=50)

        self.select_date_btn = tk.Button(self, text="Select Date", command=self.select_date)
        self.select_date_btn.place(x=400, y=150)

        
        
        self.select_seat_grid = self.SelectSeatGrid(self)
        self.select_seat_grid.place(x=200, y=300)
        self.select_seat_grid.render(self.selected_date)

        self.edit_seat_label = tk.Label(self, text="New Seat Number:")
        self.edit_seat_label.place(x=400, y=750)

        self.all_seat_nums = [s[1] for s in  self.container.db.select_all_seats()]
        self.edit_seat_combo = ttk.Combobox(self, width=20, value=self.all_seat_nums, state="readonly")
        self.edit_seat_combo.current(0)
        self.edit_seat_combo.place(x=600, y=750)
    
        self.edit_btn = tk.Button(self, text="Edit", width=7, height=1, bg="#A52A2A", fg="white", 
            command=self.edit_popup)
        self.edit_btn.place(x=800, y=750)

        self.delete_btn = tk.Button(self, text="Delete", width=7, height=1, bg="#A52A2A", fg="white", 
            command=self.delete_popup)
        self.delete_btn.place(x=900, y=750)

    def select_date(self):
        if self.selected_date == self.calendar.get_date():
            return
        
        self.selected_date = self.calendar.get_date()
        self.selected_date_label.configure(text=f"Selected date: {self.selected_date}")
        self.select_seat_grid.render(self.selected_date)

    

    def edit_popup(self):
        question = messagebox.askquestion("Edit","Do you want to edit this seat?")
        if question == "yes": self.edit_reservation()  
    
    def delete_popup(self):
        question = messagebox.askquestion("Delete","Do you want to delete this seat?")
        if question == "yes": self.delete_reservation()
    
    def delete_reservation(self):
        selected_seat_num = self.select_seat_grid.selected_seat
        if not selected_seat_num:
            self.show("Please select a seat to delete.")
            return
        self.container.db.delete_reservation(self.selected_date, self.select_seat_grid.selected_seat)
        self.show()

    def edit_reservation(self):
        selected_seat_num = self.select_seat_grid.selected_seat
        new_seat_num = self.edit_seat_combo.get()
        
        if not selected_seat_num or new_seat_num == '-':
            return
        
        self.container.db.update_reservation(self.selected_date, selected_seat_num, new_seat_num)
        self.show()

    def show(self, message="", message_color="red"):
        self.select_seat_grid.render(self.selected_date) # re-render the select seat grid
        self.tkraise() # raise the my reservations page

    class SelectSeatGrid(tk.Frame):
        def __init__(self, container):
            super().__init__(container, width=400, height=200)
            self.container = container
            self.buttons = {} # button of a particular seat can be accessed by self.buttons[<seat_number>]
            self.selected_seat = ""
        
        def render(self, date):
            self.selected_seat = "" # clear selected seats when grid is re-rendered
            app = self.container.container
            logged_in_user_id = app.auth_manager.logged_in_user_id
            reservations = app.db.select_reservations_by_date(date)
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