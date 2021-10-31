import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sys import exit

class GUI(tk.Canvas):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        sub = """Do you ever wonder who passed away on the day you were born? Or yesterday? Or any other day?
        Simply enter the date (yyyy-mm-dd format to be ISO compliant!) and see what comes up!
        """
        self._title = tk.Label(master=root, text='Who Died On This Day?', font='Arial 18')
        self._date_frame = tk.Frame(master=root)
        self._date_label = tk.Label(master=root, text=sub)
        self._year_label = tk.Label(master=self._date_frame, text='Year')
        self._month_label = tk.Label(master=self._date_frame, text='Month')
        self._day_label = tk.Label(master=self._date_frame, text='Day')
        self._year_entry = tk.Entry(master=self._date_frame, width=25)
        self._month_entry = tk.Entry(master=self._date_frame, width=10)
        self._day_entry = tk.Entry(master=self._date_frame, width=10)
        self._submit = tk.Button(master=self._date_frame, text='Search', command=get_deaths)

        label_kwargs = {
            'sticky': 'w',
            'ipadx': 10,
            'row': 0
            }
        entry_kwargs = {
            'ipadx': 10,
            'row': 1,
            'padx': 5
            }
        self._title.pack()
        self._date_label.pack()
        self._date_frame.pack(expand=False, anchor='n')
        self._date_frame.columnconfigure([0,1,2], weight=1, minsize=50)
        self._date_frame.rowconfigure([0,1,2], weight=1)
        self._year_label.grid(column=0, **label_kwargs)
        self._month_label.grid(column=1, **label_kwargs)
        self._day_label.grid(column=2, **label_kwargs)
        self._year_entry.grid(column=0, **entry_kwargs)
        self._month_entry.grid(column=1, **entry_kwargs)
        self._day_entry.grid(column=2, **entry_kwargs)
        self._submit.grid(column=2, row=2, sticky='e', pady=10, padx=10)
        self.setup_people_frame()

    def setup_people_frame(self):
        self._people = tk.Frame(master=root)
        self._people.pack(fill=tk.X)
        self._scroll = tk.Scrollbar(self)
        self._scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._people.yscrollcommand = self._scroll.set
        self._scroll.config(command=self.yview)

    def delete(self):
        self._people.destroy()
        self._people = tk.Frame(master=root)
        self._people.pack()

    def add_person(self, text):
        label = tk.Label(master=self._people, text=text)
        label.pack()

    @property
    def year(self):
        return self._year_entry.get()

    @property
    def month(self):
        return self._month_entry.get()

    @property
    def day(self):
        return self._day_entry.get()

    @classmethod
    def error_message(self):
        messagebox.showwarning('Invalid Date', 'Are you sure that\'s a date?')

    @classmethod
    def today_message(self):
        messagebox.showwarning('Invalid Date', 'Have patience, we\'re not there yet!')

root_url = 'https://en.wikipedia.org/wiki/Deaths_in_'

def get_deaths():
    yr = window.year
    mth = window.month
    dy = window.day
    dt = verify_date(yr, mth, dy)
    now = datetime.now().date()

    if dt != None and dt != now:
        month_name = datetime(year=2000, month=int(mth), day=1).strftime('%B')
        url = f'{root_url}{month_name}_{str(yr)}'
        body = BeautifulSoup(requests.get(url).text, 'html.parser').body
        list = body.find(id=dy).find_next('ul')



        for item in list:
            try:
                window.add_person(item.text)
            except:
                pass

    elif dt >= now:
        window.today_message()

def verify_date(y, m, d):
    try:
        year = int(y)
        month = int(m)
        day = int(d)
        val = datetime(year=year, month=month, day=day).date()
    except Exception as e:
        val = None
        window.error_message()
    finally:
        return val


root = tk.Tk()
window = GUI(root, bg='black', width=600, height=750)
root.mainloop()
