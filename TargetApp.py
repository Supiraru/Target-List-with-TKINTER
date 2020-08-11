import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar, DateEntry
from database import database

Database = database('Target.db')

def populate():
    targetList.delete(0, tk.END)
    for row in Database.fetch():
        targetList.insert(tk.END, row)

def addTarget():
    if targetText.get() == '' or dateText == '' or conditionText.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    Database.insert(targetText.get(), dateText, conditionText.get())
    targetList.delete(0, tk.END)
    targetList.insert(tk.END, targetText.get(), dateText, conditionText.get())
    clear()
    populate()

def select_item(event):
    try:
        global Select
        index = targetList.curselection()[0]
        Select = targetList.get(index)

        targetEntry.delete(0, tk.END)
        targetEntry.insert(tk.END, Select[1])
        dateLabel.config(text=Select[2])
        conditionEntry.delete(0, tk.END)
        conditionEntry.insert(tk.END, Select[3])
        
    except IndexError:
        pass


def removeTarget():
    Database.remove(Select[0])
    clear()
    populate()

def update():
    Database.update(Select[0], targetText.get(), dateText,
              conditionText.get())
    populate()

def clear():
    targetEntry.delete(0, tk.END)
    dateLabel.config(text='Pick Date')
    conditionEntry.delete(0, tk.END)

#Calendar
def ShowCalender():
    top = tk.Toplevel(root)
    global cal
    cal = Calendar(top, selectmode = "day", year = 2020, month = 5, day= 22)
    cal.pack(pady=10)
    my_button = tk.Button(top, text = "Get Date", command=grab_date)
    my_button.pack(pady=20)

def grab_date():
    dateLabel.config(text=cal.get_date())
    global dateText
    dateText = cal.get_date()


#Create Object
root = tk.Tk()

#Target
targetLabel = tk.Label(root, text='Target :', font=('bold', 14), pady=20, padx=20)
targetLabel.grid(row = 0, column = 0, stick = tk.W)
targetText = tk.StringVar()
targetEntry = tk.Entry(root, textvariable = targetText)
targetEntry.grid(row = 0, column = 1)

#Date
dateLabel = tk.Label(root, text='Pick Date', font=('bold', 14), padx=20)
dateLabel.grid(row=0, column=3, stick = tk.W)
dateButton = tk.Button(root, text = "show calendar", command=ShowCalender)
dateButton.grid(row=0, column=4)

#condition
conditionLabel = tk.Label(root, text='Condition :', font=('bold', 14), padx=20)
conditionLabel.grid(row=1, column=0, stick = tk.W)
conditionText = tk.StringVar()
conditionEntry = tk.Entry(root, textvariable=conditionText)
conditionEntry.grid(row=1, column=1, padx=5,pady=10)

#Target List
targetListLabel = tk.Label(root, text='List', font=('bold',14), padx=20)
targetListLabel.grid(row=3, column=0, stick=tk.W)
targetList = tk.Listbox(root, height=15, width=80)
targetList.grid(row=4, column=0, columnspan=5, rowspan=12, pady=20, padx=20)

#scrollbar
scrollbar = tk.Scrollbar(root)
scrollbar.grid(row=4, column=5)
targetList.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=targetList.yview)

#Buttons
addButton = tk.Button(root, text='Add Target', width=12, command=addTarget) 
addButton.grid(row=2,column=0,pady=20)
removeButton = tk.Button(root, text='Remove', width=12, command=removeTarget)
removeButton.grid(row=2,column=1)
UpdateButton = tk.Button(root, text='Update', width=12, command=update)
UpdateButton.grid(row=2,column=2)
clearButton = tk.Button(root, text='Clear Input', width=12, command=clear)
clearButton.grid(row=2,column=3)

#bind select
targetList.bind('<<ListboxSelect>>', select_item)


root.title('Target List Application')
root.geometry('700x500')

# Start Apps
populate()
root.mainloop()