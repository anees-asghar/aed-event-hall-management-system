import tkinter as tk
from tkinter import ttk

class AdminPage(tk.Frame):
    def __init__(self, container):
        super().__init__(container, width=1100, height=800)
        self.container = container
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

      
        self.days_clicked = ttk.Combobox(self, value = self.days_admin, state="readonly")
        self.days_clicked.current(0)
        self.days_clicked.place(x=200, y=350)

        self.month_clicked = ttk.Combobox(self, value = self.months_admin, state="readonly")
        self.month_clicked.current(0)
        self.month_clicked.place(x=400, y=350)
        
        self.year_clicked = ttk.Combobox(self, value = self.years_admin, state="readonly")
        self.year_clicked.current(0)
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

            reservations = self.container.db.select_reservations_by_date(date)

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

            reservations = self.container.db.select_reservations_by_month(month=month_num, year=year_abbr)

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

            reservations = self.container.db.select_reservations_by_year(year=year_abbr)

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

