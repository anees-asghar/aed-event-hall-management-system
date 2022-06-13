import datetime
import tkinter as tk
from tkinter import ttk


class AdminPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, width=1100, height=800)
        self.app = app

        # put admin page in the app window
        self.grid(row=0, column=1)
        self.grid_propagate(False)

        # page title
        self.title_label = tk.Label(self, text="Admin Page", font=("Arial", 30))
        self.title_label.place(x=200, y=100)

        # page sub title
        self.sales_by_label = tk.Label(self, text="Sales by:", font=("Arial", 20)) 
        self.sales_by_label.place(x=200, y=200)


        # --- OPTION SELECT AREA (sales by day, month or year) ---
        self.radio_btn_val = tk.IntVar() # stores the value of the selected radio button

        # day radio button
        self.day_radio = tk.Radiobutton(self, variable=self.radio_btn_val, value=0, text="Day", 
            command=self.day_radio_selected)
        self.day_radio.place(x=200, y=300)

        # month radio button
        self.month_radio = tk.Radiobutton(self, variable=self.radio_btn_val, value=1, text="Month", 
            command=self.month_radio_selected)
        self.month_radio.place(x=400, y=300)
        
        # year radio button
        self.radio_year_btn = tk.Radiobutton(self, variable=self.radio_btn_val, value=2, text="Year", 
            command=self.year_radio_selected)
        self.radio_year_btn.place(x=600, y=300)


        # --- DATE PICKING AREA ---
        days = [i for i in range(1, 31+1)]
        self.months = [
            "January", "February", "March", "April", "May", "June", "July", 
            "August", "September", "October", "November", "December"
        ]
        years = ["2022","2023"]

        # combo box for day
        self.day_combo = ttk.Combobox(self, value=days, state="readonly")
        self.day_combo.current(0)
        self.day_combo.place(x=200, y=350)

        # combo box for month
        self.month_combo = ttk.Combobox(self, value=self.months, state="readonly")
        self.month_combo.current(0)
        self.month_combo.place(x=400, y=350)
        
        # combo box for year
        self.year_combo = ttk.Combobox(self, value=years, state="readonly")
        self.year_combo.current(0)
        self.year_combo.place(x=600, y=350)
        
        # select date button
        self.select_date_btn = tk.Button(self, text="Select Date", command=self.display_stats)
        self.select_date_btn.place(x=800, y=340)

        # error label
        self.error_label = tk.Label(self, text="", fg="red", font=("Arial"))
        self.error_label.place(x=200, y=400) 


        # --- DISPLAY STATS AREA ---
        self.date_label = tk.Label(self, font=("Arial", 12), text="")
        self.date_label.place(x=200, y=450)

        self.total_tickets_sold_label = tk.Label(self, font=("Arial", 12), text="")
        self.total_tickets_sold_label.place(x=200, y=500)

        self.vip_tickets_sold_label = tk.Label(self, font=("Arial", 12), text="")
        self.vip_tickets_sold_label.place(x=200, y=550)

        self.total_tickets_value_label = tk.Label(self, font=("Arial", 12), text="")
        self.total_tickets_value_label.place(x=200, y=600)
       

        self.display_stats() # display stats for the default date
  

    def day_radio_selected(self):
        self.day_combo.configure(state="readonly")
        self.month_combo.configure(state="readonly")
        self.year_combo.configure(state="readonly")


    def month_radio_selected(self):
        self.day_combo.configure(state="disabled")
        self.month_combo.configure(state="readonly")
        self.year_combo.configure(state="readonly")


    def year_radio_selected(self):
        self.day_combo.configure(state="disabled")
        self.month_combo.configure(state="disabled")
        self.year_combo.configure(state="readonly")


    def generate_stats(self, reservations):
        total_tickets_sold = len(reservations)
        vip_tickets_sold = len(list(filter(lambda r: r[1]=="VIP", reservations)))
        total_tickets_value = sum([r[2] for r in reservations])
        return total_tickets_sold, vip_tickets_sold, total_tickets_value


    def display_stats(self):
        option_selected = self.radio_btn_val.get() # check which radio button was selected

        day = self.day_combo.get()    # get the selected day
        month = self.month_combo.get() # get the selected month
        year = self.year_combo.get()   # get the selected year

        # create db representation for day, month and year; for example day=09, month=05, year=22
        day_db = day if int(day) >= 10 else '0'+day
        month_num = self.months.index(month) + 1 # get month number; for example February = 2
        month_db = str(month_num) if month_num >= 10 else f"0{month_num}"
        year_db = year[-2:]

        if option_selected == 0: # user requested stats by date
            # check if the date is valid; 29 Feb 2022 is not a valid date
            try:
                datetime.datetime(int(year), month_num, int(day))
            except:
                self.error_label.configure(text="Not a valid date.")
                return
            
            reservations = self.app.db.select_reservations_by_day(day_db, month_db, year_db)
            self.date_label.configure(text=f"Date: {day} {month} {year}")

        elif option_selected == 1: # user requested data by month
            reservations = self.app.db.select_reservations_by_month(month_db, year_db)
            self.date_label.configure(text=f"Date: {month} {year}")
            
        elif option_selected == 2: # user requested data by year
            reservations = self.app.db.select_reservations_by_year(year_db)
            self.date_label.configure(text=f"Date: {year}")
        
        total_tickets_sold, vip_tickets_sold, total_tickets_value = self.generate_stats(reservations)

        self.total_tickets_sold_label.configure(text=f"Total Tickets Sold: {total_tickets_sold}")
        self.vip_tickets_sold_label.configure(text=f"VIP Tickets Sold: {vip_tickets_sold}")
        self.total_tickets_value_label.configure(text=f"Total Tickets Value: {total_tickets_value}$")

        self.error_label.configure(text="") # clear error label
 

    def show(self):
        self.display_stats()
        self.tkraise()
