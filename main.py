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

    def add_person(self, text):
        label = tk.Label(text=text)
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

root_url = 'https://en.wikipedia.org/wiki/Deaths_in_'

def get_deaths():
    year = window.year
    month = window.month
    day = window.day
    date = verify_date(year, month, day)

    if date != None:
        url = f'{root_url}{str(year)}'
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        body = soup.body
        lists = body.find_all('ul')

        for ul in lists:
            try:
                val = ul.previous_sibling.previous_sibling.string
            except:
                pass

            if val == str(int(day)):
                latest = ul.children
                break

        for item in latest:
            try:
                window.add_person(item.text)
            except:
                pass

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
