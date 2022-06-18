import datetime
import tkinter as tk
from tkinter import ttk


class AdminPage(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg="#F1EEE9")
        self.app = app

        # put admin page in the app window
        self.place(relx=0.2, rely=0, relheight=1, relwidth=0.8)

        # page title
        self.title_label = tk.Label(self, text="Admin Page", bg="#F1EEE9", font=("Helvetica", 30))
        self.title_label.place(relx=0, rely=0, relwidth=1, relheight=0.25)


        # --- SELECT OPTION AREA (sales by day, month or year) ---

        self.radio_btn_val = tk.IntVar() # stores the value of the selected radio button

        # select option frame
        select_option_frame = tk.Frame(self, bg="#F1EEE9")
        select_option_frame.place(relx=0, rely=0.25, relwidth=1, relheight=0.15)

        # select option label
        self.select_option_label = tk.Label(select_option_frame, text="Sales data by:", 
            bg="#F1EEE9", font=("Helvetica")) 
        self.select_option_label.place(relx=0.2, rely=0.5, relwidth=0.15, anchor="w")

        # day option radio button
        self.day_radio = tk.Radiobutton(select_option_frame, variable=self.radio_btn_val, value=0, text="Day", 
            font=("Helvetica"), bg="#F1EEE9", command=self.day_radio_selected)
        self.day_radio.place(relx=0.35, rely=0.5, relwidth=0.15, anchor="w")

        # month option radio button
        self.month_radio = tk.Radiobutton(select_option_frame, variable=self.radio_btn_val, value=1, text="Month", 
            font=("Helvetica"), bg="#F1EEE9", command=self.month_radio_selected)
        self.month_radio.place(relx=0.5, rely=0.5, relwidth=0.15, anchor="w")
        
        # year option radio button
        self.radio_year_btn = tk.Radiobutton(select_option_frame, variable=self.radio_btn_val, value=2, text="Year", 
            font=("Helvetica"), bg="#F1EEE9", command=self.year_radio_selected)
        self.radio_year_btn.place(relx=0.65, rely=0.5, relwidth=0.15, anchor="w")


        # --- SELECT DATE AREA ---

        days = [i for i in range(1, 31+1)]
        self.months = [
            "January", "February", "March", "April", "May", "June", "July", 
            "August", "September", "October", "November", "December"
        ]
        years = ["2022","2023"]

        # select date frame
        select_date_frame = tk.Frame(self, bg="#F1EEE9")
        select_date_frame.place(relx=0, rely=0.40, relwidth=1, relheight=0.1)

        # combo box for day
        self.day_combo = ttk.Combobox(select_date_frame, font=("Helvetica", 10), value=days, state="readonly")
        self.day_combo.current(0)
        self.day_combo.place(relx=0.1, rely=0, relheight=0.5, relwidth=0.2)

        # combo box for month
        self.month_combo = ttk.Combobox(select_date_frame, font=("Helvetica", 10), value=self.months, state="readonly")
        self.month_combo.current(0)
        self.month_combo.place(relx=0.3, rely=0, relheight=0.5, relwidth=0.2)
        
        # combo box for year
        self.year_combo = ttk.Combobox(select_date_frame, font=("Helvetica", 10), value=years, state="readonly")
        self.year_combo.current(0)
        self.year_combo.place(relx=0.5, rely=0, relheight=0.5, relwidth=0.2)
        
        # select date button
        self.select_date_btn = tk.Button(select_date_frame, text="Select Date", relief="flat", 
            bg="#15133C", fg="white", command=self.display_stats)
        self.select_date_btn.place(relx=0.7, rely=0, relheight=0.5, relwidth=0.2)

        # error label
        self.error_label = tk.Label(select_date_frame, text="", bg="#F1EEE9", fg="red", font=("Helvetica"))
        self.error_label.place(relx=0.1, rely=0.5) 


        # --- DISPLAY STATS AREA ---

        # display stats frame
        display_stats_frame = tk.Frame(self, bg="#F1EEE9")
        display_stats_frame.place(relx=0, rely=0.5, relwidth=1, relheight=0.4)

        # statistics label 
        self.stats_label = tk.Label(display_stats_frame, bg="#F1EEE9", font=("Helvetica", 20), text="")
        self.stats_label.place(relx=0.2, rely=0, relheight=0.4)
        
        # total tickets sold label
        self.total_tickets_sold_label = tk.Label(display_stats_frame, bg="#F1EEE9", font=("Helvetica"), text="")
        self.total_tickets_sold_label.place(relx=0.2, rely=0.4, relheight=0.2)

        # vip tickets sold label
        self.vip_tickets_sold_label = tk.Label(display_stats_frame, bg="#F1EEE9", font=("Helvetica"), text="")
        self.vip_tickets_sold_label.place(relx=0.2, rely=0.6, relheight=0.2)

        # total tickets value label
        self.total_tickets_value_label = tk.Label(display_stats_frame, bg="#F1EEE9", font=("Helvetica"), text="")
        self.total_tickets_value_label.place(relx=0.2, rely=0.8, relheight=0.2)


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
            self.stats_label.configure(text=f"Statistics | {day} {month} {year}")

        elif option_selected == 1: # user requested data by month
            reservations = self.app.db.select_reservations_by_month(month_db, year_db)
            self.stats_label.configure(text=f"Statistics | {month} {year}")
            
        elif option_selected == 2: # user requested data by year
            reservations = self.app.db.select_reservations_by_year(year_db)
            self.stats_label.configure(text=f"Statistics | {year}")
        
        total_tickets_sold, vip_tickets_sold, total_tickets_value = self.generate_stats(reservations)

        self.total_tickets_sold_label.configure(text=f"Total Tickets Sold: {total_tickets_sold}")
        self.vip_tickets_sold_label.configure(text=f"VIP Tickets Sold: {vip_tickets_sold}")
        self.total_tickets_value_label.configure(text=f"Total Tickets Value: {total_tickets_value}$")

        self.error_label.configure(text="") # clear error label
 

    def show(self):
        self.display_stats()
        self.tkraise()
