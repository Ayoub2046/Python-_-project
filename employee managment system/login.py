from customtkinter import *
from PIL import Image
from tkinter import messagebox

# Global variables to store the username and password
current_username = 'admin'
current_password = '1221'


def login():
    if UsernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required')
    elif UsernameEntry.get() == current_username and passwordEntry.get() == current_password:
        messagebox.showinfo('Success', 'Login is successful')
        root.destroy()
        import ems  # Replace with your actual import
    else:
        messagebox.showerror('Error', 'Wrong credentials')


def reset():
    new_window = CTkToplevel()
    new_window.title('Create New User')
    new_window.geometry('400x200')
    new_window.resizable(0, 0)

    new_username_label = CTkLabel(new_window, text='New Username')
    new_username_label.place(x=50, y=50)
    new_username_entry = CTkEntry(new_window, width=200)
    new_username_entry.place(x=150, y=50)

    new_password_label = CTkLabel(new_window, text='New Password')
    new_password_label.place(x=50, y=100)
    new_password_entry = CTkEntry(new_window, width=200, show='*')
    new_password_entry.place(x=150, y=100)

    def create_user():
        global current_username, current_password
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()

        if new_username == '' or new_password == '':
            messagebox.showerror('Error', 'All fields are required')
        elif new_username == current_username and new_password == current_password:
            messagebox.showerror('Error', 'New username and password must be different from old ones')
        elif new_username == current_username:
            messagebox.showerror('Error', 'New username must be different from the old one')
        elif new_password == current_password:
            messagebox.showerror('Error', 'New password must be different from the old one')
        else:
            # Update the global username and password
            current_username = new_username
            current_password = new_password
            messagebox.showinfo('Success', 'New user created successfully')
            new_window.destroy()  # Close the new user window
            reset_login_window()  # Return to the login window

    create_button = CTkButton(new_window, text='Create', command=create_user)
    create_button.place(x=150, y=150)


def reset_login_window():
    # Clear the entries in the login window
    UsernameEntry.delete(0, 'end')
    passwordEntry.delete(0, 'end')
    root.deiconify()  # Show the login window again


def enter_key(event):
    login()


root = CTk()
root.geometry('930x478')
root.resizable(0, 0)
root.title('Login Page')

image = CTkImage(Image.open('5561830_21207.jpg'), size=(930, 478))
imagelabel = CTkLabel(root, image=image)
imagelabel.place(x=0, y=0)

headinlabel = CTkLabel(root, text='Employee Management System', bg_color='#FAFAF7', text_color='dark blue',
                       font=('Goudy Old Style', 29, 'bold'))
headinlabel.place(x=20, y=100)

# Section for Username
UsernameEntry = CTkEntry(root, placeholder_text='Enter your name', width=180)
UsernameEntry.place(x=50, y=150)

# Section for Password
passwordEntry = CTkEntry(root, placeholder_text='Enter your password', width=180, show='*')
passwordEntry.place(x=50, y=200)

# Login Button
loginButton = CTkButton(root, text='Login', cursor='hand2', command=login)
loginButton.place(x=70, y=250)

# Reset Button
resetButton = CTkButton(root, text='Create New User', cursor='hand2', command=lambda: [root.withdraw(), reset()])
resetButton.place(x=70, y=300)

root.bind('<Return>', enter_key)

root.mainloop()