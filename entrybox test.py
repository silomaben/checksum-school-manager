import tkinter as tk
from datetime import datetime

root = tk.Tk()

def validate_date(date):
    if len(date) != 10: # Check if the input has the correct length
        return False
    if not date[0:2].isdigit() or not date[3:5].isdigit() or not date[6:10].isdigit(): # Check if the digits are in the correct places
        return False
    if date[2] != '-' or date[5] != '-': # Check if the spaces are in the correct places
        return False
    return True

def on_submit():
    date = entry.get()
    if validate_date(date):
        # Date is valid, do something with it
        print(f"Valid date: {date}")
    else:
        # Date is not valid, show an error message
        print("Invalid date")

current_date = datetime.now().strftime('%d-%m-%Y')

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="Submit", command=on_submit)
entry.insert(0, current_date)

button.pack()

root.mainloop()
