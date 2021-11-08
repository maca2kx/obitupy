import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from sys import exit
import webbrowser

class GUI(tk.Canvas):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        sub = """Do you ever wonder who passed away on the day you were born? Or yesterday? Or any other day (at least until 1994 when Wikipedia changes their page formatting)?
        Simply enter the date (yyyy-mm-dd format to be ISO compliant!) and see what comes up!
        """
        self.title = tk.Label(master=root, text='Who Died On This Day?', font='Arial 18')
        self.sub_label = tk.Label(master=root, text=sub)

        self.date_entry = tk.Entry(master=root, width=35)
        self.submit = tk.Button(master=root, text='Search', command=get_deaths)

        self.title.pack()
        self.sub_label.pack()
        self.date_entry.pack()
        self.submit.pack(pady=5)

        self.date_entry.bind('<Return>', get_deaths)

        self.list_links = []

        self.add_list()
        self.date_entry.focus_set()
        self.winfo_toplevel().title('Obitupy')

    def add_list(self):
        self.people_frame = tk.Frame(master=root)
        self.pack_people_frame()
        self.scroll = tk.Scrollbar(master=self.people_frame)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.list = tk.Listbox(master=self.people_frame, bd=0, yscrollcommand=self.scroll.set)
        self.list.pack(fill=tk.X)
        self.list.bind('<<ListboxSelect>>', self.list_click)
        self.scroll.config(command=self.list.yview)
        self.people_frame.pack_forget()

    def list_click(self, event):
        link = self.list_links[self.list.curselection()[0]]
        webbrowser.open_new_tab(link)

    def pack_people_frame(self):
        self.people_frame.pack(fill=tk.X)

    def add_person(self, i, text, link):
        if link.startswith('https://en.wikipedia.org/') == False:
            link = f'https://en.wikipedia.org{link}'

        self.list_links.append(link)
        self.list.insert(i, text)

    def clear_list(self):
        self.list.delete(0, self.list.size()-1)

    @property
    def list_size(self):
        return self.list.size()

    @property
    def get_date(self):
        return self.date_entry.get()

    def error_message(self, type):
        if type == 1:
            messagebox.showwarning('Invalid Date', 'Are you sure that\'s a date?')
        elif type == 2:
            messagebox.showwarning('Invalid Date', 'Have patience, we\'re not there yet!')
        elif type == 3:
            messagebox.showwarning('Invalid Date', 'Unable to find any deaths for this date')


def get_deaths(event=None):
    ROOT_URL = 'https://en.wikipedia.org/wiki/Deaths_in_'
    possible_formats = ('%Y-%m-%d', '%Y%m%d', '%Y/%m/%d', '%Y.%m.%d')

    for i, format in enumerate(possible_formats):
        try:
            dt = datetime.strptime(window.get_date, format).date()
            break
        except:
            if i == len(possible_formats) - 1:
                window.error_message(1)
                dt = None
            else:
                pass

    now = datetime.now().date()
    if dt != None and dt < now:
        yr = dt.year
        mth = dt.month
        dy = dt.day
        month_name = datetime(year=2000, month=int(mth), day=1).strftime('%B')
        url = f'{ROOT_URL}{month_name}_{str(yr)}'
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
                            window.add_person(i, item.text.split('[')[0], item.a['href'])
                        except:
                            pass
            except:
                window.error_message(3)
        else:
            pass

    elif dt >= now:
        window.error_message(2)

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    window = GUI(root, bg='black', width=600, height=750)
    root.mainloop()
