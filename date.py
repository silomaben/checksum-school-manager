# import sqlite3
# from datetime import date
#
# # Connect to the database
# conn = sqlite3.connect('example.db')
#
# # Create a cursor
# c = conn.cursor()
#
# # Create a table
# c.execute('''CREATE TABLE IF NOT EXISTS my_table
#              (id INTEGER PRIMARY KEY, date_col DATE)''')
#
# # Insert a row with a date value
# today = date.today().strftime('%Y-%m-%d')
# print(today)
# c.execute("INSERT INTO my_table (id, date_col) VALUES (?, ?)", (1, today))
#
# # Commit the changes and close the connection
# conn.commit()
# conn.close()

import tkinter as tk
from tkinter import ttk

class TreeViewFilter:
    def __init__(self, parent):
        self.parent = parent
        self.treeview = ttk.Treeview(parent, columns=("Name", "Age"))
        self.treeview.heading("#0", text="ID")
        self.treeview.heading("Name", text="Name")
        self.treeview.heading("Age", text="Age")
        self.treeview.pack()
        self.populate_treeview()
        self.filter_var = tk.StringVar()
        self.filter_var.trace("w", self.filter_callback)
        self.filter_entry = tk.Entry(parent, textvariable=self.filter_var)
        self.filter_entry.pack()

    def populate_treeview(self):
        data = [("1", "John", "30"), ("2", "Jane", "25"), ("3", "Mike", "40"), ("4", "Mary", "35")]
        for row in data:
            self.treeview.insert("", "end", text=row[0], values=(row[1], row[2]))

    def filter_callback(self, *args):
        filter_str = self.filter_var.get()
        if filter_str:
            children = self.treeview.get_children()
            for child in children:
                values = self.treeview.item(child)["values"]
                if values and filter_str.lower() not in values[0].lower():
                    self.treeview.detach(child)
        else:
            self.populate_treeview()

if __name__ == "__main__":
    root = tk.Tk()
    treeview_filter = TreeViewFilter(root)
    root.mainloop()

