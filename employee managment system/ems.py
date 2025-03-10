from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import sqlite3

# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Create a table if it doesn't exist with AUTOINCREMENT for id
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    role TEXT,
                    gender TEXT,
                    salary REAL)''')
conn.commit()

# Functions
def treeview_data():
    tree.delete(*tree.get_children())  # Clear existing data
    cursor.execute('SELECT * FROM employees')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

def add_employee(event=None):
    if phoneEntry.get() == '' or nameEntry.get() == '' or salaryEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        name = nameEntry.get().title()  # Capitalize the first letter of each word
        employee = (name, phoneEntry.get(), roleBox.get(), genderbox.get(), salaryEntry.get())
        cursor.execute('INSERT INTO employees (name, phone, role, gender, salary) VALUES (?, ?, ?, ?, ?)', employee)
        conn.commit()
        treeview_data()  # Refresh data in Treeview
        new_employee()  # Clear the input fields

def search_employee():
    query = searchEntry.get()
    option = searchbox.get()
    if query == '' or option == 'search by':
        messagebox.showerror('Error', 'Please select search criteria and enter a query')
    else:
        tree.delete(*tree.get_children())
        cursor.execute(f'SELECT * FROM employees WHERE {option.lower()} LIKE ?', ('%' + query + '%',))
        for row in cursor.fetchall():
            tree.insert('', 'end', values=row)

def update_employee():
    selected = tree.focus()
    if not selected:
        messagebox.showerror('Error', 'Please select an employee to update')
        return
    values = tree.item(selected, 'values')
    id_index = int(values[0])

    name = nameEntry.get().title()  # Capitalize the first letter of each word
    updated_employee = (
        name,
        phoneEntry.get(),
        roleBox.get(),
        genderbox.get(),
        salaryEntry.get(),
        id_index
    )
    cursor.execute('UPDATE employees SET name=?, phone=?, role=?, gender=?, salary=? WHERE id=?', updated_employee)
    conn.commit()
    treeview_data()  # Refresh data in Treeview

def delete_employee():
    selected = tree.focus()
    if not selected:
        messagebox.showerror('Error', 'Please select an employee to delete')
        return
    values = tree.item(selected, 'values')
    cursor.execute('DELETE FROM employees WHERE id=?', (int(values[0]),))
    conn.commit()
    treeview_data()  # Refresh data in Treeview

def delete_all():
    cursor.execute('DELETE FROM employees')
    conn.commit()
    treeview_data()  # Refresh data in Treeview

def new_employee():
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    roleBox.set(role_option[0])
    genderbox.set(gender_option[0])
    salaryEntry.delete(0, END)

# Add this function to print all employees
def print_all_employees():
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Create the main window
window = CTk()
window.geometry('930x582+100+100')
window.resizable(False, False)
window.title('Employee Management System')

# Set the background color to light gray
window.configure(fg_color='#161c30')

logo = CTkImage(Image.open('img.png'), size=(930, 158))
logolabel = CTkLabel(window, image=logo, text='')
logolabel.grid(row=0, column=0, columnspan=2)

leftFrame = CTkFrame(window, fg_color='#161c30')
leftFrame.grid(row=1, column=0)

idlabel = CTkLabel(leftFrame, text='ID', font=('arial', 18, 'bold'))
idlabel.grid(row=0, column=0, padx=20, pady=15)

idEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=180, state='disabled')  # Disabled Entry
idEntry.grid(row=0, column=1)

namelabel = CTkLabel(leftFrame, text='Name', font=('arial', 18, 'bold'))
namelabel.grid(row=1, column=0, padx=20, pady=15, sticky='w')
nameEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=180)
nameEntry.grid(row=1, column=1)

phonelabel = CTkLabel(leftFrame, text='Phone', font=('arial', 18, 'bold'))
phonelabel.grid(row=2, column=0, padx=20, pady=15, sticky='w')

phoneEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=180)
phoneEntry.grid(row=2, column=1)

rolelabel = CTkLabel(leftFrame, text='Role', font=('arial', 18, 'bold'))
rolelabel.grid(row=3, column=0, padx=20, pady=15, sticky='w')
role_option = ['Web Developer', 'Python', 'Principle of Management', 'Accounting', 'JavaScript', 'IT in Business', 'Information Management System',
               'Agriculture','PA','BH','NURSIN','DATABASE','MATH','ARABIC','CRITICAL THINKING','ENGLISH','SOMALIA']
roleBox = CTkComboBox(leftFrame, values=role_option, width=180, font=('arial', 18, 'bold'), state='readonly')
roleBox.grid(row=3, column=1)
roleBox.set(role_option[0])

genderlabel = CTkLabel(leftFrame, text='Gender', font=('arial', 18, 'bold'))
genderlabel.grid(row=4, column=0, padx=20, pady=15, sticky='w')

gender_option = ['Male', 'Female']
genderbox = CTkComboBox(leftFrame, values=gender_option, width=180, font=('arial', 18, 'bold'), state='readonly')
genderbox.grid(row=4, column=1)
genderbox.set(gender_option[0])

salarylabel = CTkLabel(leftFrame, text='Salary', font=('arial', 18, 'bold'))
salarylabel.grid(row=5, column=0, padx=20, pady=15, sticky='w')

salaryEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=180)
salaryEntry.grid(row=5, column=1)

rightFrame = CTkFrame(window, fg_color='gray')
rightFrame.grid(row=1, column=1)

search_option = ['ID', 'Name', 'Phone', 'Role', 'Gender', 'Salary']
searchbox = CTkComboBox(rightFrame, values=search_option, state='readonly')
searchbox.grid(row=0, column=0)
searchbox.set('search by')

searchEntry = CTkEntry(rightFrame)
searchEntry.grid(row=0, column=1)

searchButton = CTkButton(rightFrame, text='Search', width=100, command=search_employee)
searchButton.grid(row=0, column=2)

showallButton = CTkButton(rightFrame, text='Show All', width=100, command=treeview_data)
showallButton.grid(row=0, column=3, pady=5)

tree = ttk.Treeview(rightFrame)
tree.grid(row=1, column=0, columnspan=4)

tree['columns'] = ('ID', 'Name', 'Phone', 'Role', 'Gender', 'Salary')
tree.heading('ID', text='ID', anchor='w')
tree.heading('Name', text='Name', anchor='w')
tree.heading('Phone', text='Phone', anchor='w')
tree.heading('Role', text='Role', anchor='w')
tree.heading('Gender', text='Gender', anchor='w')
tree.heading('Salary', text='Salary', anchor='w')

tree.config(show='headings')

tree.column('ID', width=100, anchor='w')
tree.column('Name', width=100, anchor='w')
tree.column('Phone', width=160, anchor='w')
tree.column('Role', width=200, anchor='w')
tree.column('Gender', width=100, anchor='w')
tree.column('Salary', width=140, anchor='w')

Style = ttk.Style()
Style.configure('Treeview.Heading', font=('arial', 10, 'bold'))
Style.configure('Treeview', font=('arial', 10, 'bold'), rowheight=30, background='white', forground='white')

scrollbar = ttk.Scrollbar(rightFrame, orient=VERTICAL)
scrollbar.grid(row=1, column=4, sticky='ns')
tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

buttonFrame = CTkFrame(window, fg_color='#161c30')
buttonFrame.grid(row=2, column=0, columnspan=2)

newButton = CTkButton(buttonFrame, text='New Employee', font=('arial', 16, 'bold'), width=160, corner_radius=15, command=new_employee)
newButton = CTkButton(buttonFrame, text='New Employee', font=('arial', 16, 'bold'), width=160, corner_radius=15, command=new_employee)
newButton.grid(row=0, column=0, pady=5)

addButton = CTkButton(buttonFrame, text='Add Employee', font=('arial', 16, 'bold'), width=160, corner_radius=15, command=add_employee)
addButton.grid(row=0, column=1, pady=5, padx=5)

UpdateButton = CTkButton(buttonFrame, text='Update Employee', font=('arial', 16, 'bold'), width=160, corner_radius=15, command=update_employee)
UpdateButton.grid(row=0, column=2, pady=5, padx=5)

DeleteButton = CTkButton(buttonFrame, text='Delete Employee', font=('arial', 16, 'bold'), width=160, corner_radius=15, command=delete_employee)
DeleteButton.grid(row=0, column=3, pady=5, padx=5)

DeleteAllButton = CTkButton(buttonFrame, text='Delete All', font=('arial', 16, 'bold'), width=160, corner_radius=15, command=delete_all)
DeleteAllButton.grid(row=0, column=4, pady=5, padx=5)

# Bind Enter key to add_employee function
window.bind('<Return>', add_employee)

# Call print_all_employees function to see stored data
print_all_employees()

# Ensure to close the database connection when your application exits
window.protocol("WM_DELETE_WINDOW", lambda: (conn.close(), window.destroy()))

# Start the Tkinter event loop
window.mainloop()

# Call treeview_data() to show all stored data in the Treeview part
treeview_data()
