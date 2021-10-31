import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sys import exit

class GUI(tk.Canvas):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        sub = """Do you ever wonder who passed away on the day you were born? Or yesterday? Or any other day (within reason)?
        Simply enter the date (yyyy-mm-dd format to be ISO compliant!) and see what comes up!
        """
        self.title = tk.Label(master=root, text='Who Died On This Day?', font='Arial 18')
        self.date_frame = tk.Frame(master=root)
        self.date_label = tk.Label(master=root, text=sub)
        self.year_label = tk.Label(master=self.date_frame, text='Year')
        self.month_label = tk.Label(master=self.date_frame, text='Month')
        self.day_label = tk.Label(master=self.date_frame, text='Day')
        self.year_entry = tk.Entry(master=self.date_frame, width=25)
        self.month_entry = tk.Entry(master=self.date_frame, width=10)
        self.day_entry = tk.Entry(master=self.date_frame, width=10)
        self.submit = tk.Button(master=self.date_frame, text='Search', command=get_deaths)

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
        self.title.pack()
        self.date_label.pack()
        self.date_frame.pack(expand=False, anchor='n')
        self.date_frame.columnconfigure([0,1,2], weight=1, minsize=50)
        self.date_frame.rowconfigure([0,1,2], weight=1)

        self.year_label.grid(column=0, **label_kwargs)
        self.month_label.grid(column=1, **label_kwargs)
        self.day_label.grid(column=2, **label_kwargs)
        self.year_entry.grid(column=0, **entry_kwargs)
        self.month_entry.grid(column=1, **entry_kwargs)
        self.day_entry.grid(column=2, **entry_kwargs)
        self.submit.grid(column=2, row=2, sticky='e', pady=10, padx=10)

        self.add_list()
        self.year_entry.focus_set()
        self.set_listeners()

    def add_list(self):
        self.people_frame = tk.Frame(master=root)
        self.pack_people_frame()
        self.scroll = tk.Scrollbar(master=self.people_frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.list = tk.Listbox(master=self.people_frame, bd=0, highlightthickness=0,   yscrollcommand=self.scroll.set)
        self.list.pack(fill=tk.X)
        self.scroll.config(command=self.list.yview)
        self.people_frame.pack_forget()

    def pack_people_frame(self):
        self.people_frame.pack(fill=tk.X)

    def add_person(self, i, text):
        self.list.insert(i, text)

    def clear_list(self):
        self.list.delete(0, self.list.size()-1)

    @property
    def list_size(self):
        return self.list.size()

    @property
    def year(self):
        return self.year_entry.get()

    @property
    def month(self):
        return self.month_entry.get()

    @property
    def day(self):
        return self.day_entry.get()

    def set_listeners(self):
        self.year_entry.bind('<Key>', self.year_switch)
        self.month_entry.bind('<Key>', self.month_switch)
        self.day_entry.bind('<Key>', self.day_switch)

    def year_switch(self, event):
        if len(self.year_entry.get()) == 3:
            self.month_entry.focus_set()

    def month_switch(self, event):
        if len(self.month_entry.get()) == 1:
            self.day_entry.focus_set()

    def day_switch(self, event):
        if len(self.day_entry.get()) == 1:
            self.submit.focus_set()

    def error_message(self, type):
        if type == 1:
            messagebox.showwarning('Invalid Date', 'Are you sure that\'s a date?')
        elif type == 2:
            messagebox.showwarning('Invalid Date', 'Have patience, we\'re not there yet!')
        elif type == 3:
            messagebox.showwarning('Invalid Date', 'Unable to find any deaths for this date')

root_url = 'https://en.wikipedia.org/wiki/Deaths_in_'

def get_deaths():
    yr = window.year
    mth = window.month
    dy = window.day
    dt = verify_date(yr, mth, dy)
    now = datetime.now().date()

    if dt != None and dt < now:
        month_name = datetime(year=2000, month=int(mth), day=1).strftime('%B')
        url = f'{root_url}{month_name}_{str(yr)}'
        body = BeautifulSoup(requests.get(url).text, 'html.parser').body

        if body != None:
            try:
                list = body.find(id=dy).find_next('ul')

                if list != None:
                    if window.list_size > 0:
                        window.clear_list()

                    window.pack_people_frame()
                    for i, item in enumerate(list):
                        try:
                            window.add_person(i, item.text)
                        except:
                            pass
            except:
                window.error_message(3)
        else:
            pass

    elif dt >= now:
        window.error_message(2)

def verify_date(y, m, d):
    try:
        year = int(y)
        month = int(m)
        day = int(d)
        val = datetime(year=year, month=month, day=day).date()
    except:
        val = None
        window.error_message(1)
    finally:
        return val


root = tk.Tk()
window = GUI(root, bg='black', width=600, height=750)
root.mainloop()
