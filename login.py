import ttkthemes
from tkinter import ttk, messagebox, filedialog
from tkinter import *
from tkinter import messagebox

# def login(usernameEntry, passwordEntry):
#     if usernameEntry.get() == '' or passwordEntry.get() == '':
#         messagebox.showerror('Error', 'Fields can not be empty.')
#     elif usernameEntry.get() == 'admin1' or passwordEntry.get() == 'admin1':
#         messagebox.showinfo('Success', 'Welcome to Student Management System.')
#         import sms
#         #window.destroy()
#     else:
#         messagebox.showerror('Error', 'Please Check USERNAME or PASSWORD')

def login():
    if not usernameEntry.get() and not passwordEntry.get():
        messagebox.showerror("Error", "USERNAME and PASSWORD are REQUIRED.")
    elif not usernameEntry.get() or not passwordEntry.get():
        messagebox.showerror("Error", "Please enter both USERNAME and PASSWORD.")
    elif usernameEntry.get() != "admin" or passwordEntry.get() != "adminpass":
        messagebox.showerror("Error", "Please Check USERNAME or PASSWORD.")
    else:
        messagebox.showinfo("Success", "Login successful!")
        window.destroy()
        import sms

window = ttkthemes.ThemedTk()
window.get_themes()
window.set_theme('breeze')
# To Fix the Window size
window.geometry('1500x750+10+20')
window.title('Login System of Student Management System')

window.resizable(False, False)  # To Disable Maximize Button
bgLabel = Label(window, bg='white')

loginFrame = Frame(window, bg='white')
loginFrame.place(x=480, y=180)
loginImage = PhotoImage(file='administrator.png')
loginLabel = Label(loginFrame, image=loginImage)
loginLabel.grid(row=0, column=0, columnspan=2, pady=10, padx=5)

usernameImage = PhotoImage(file='username.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                      font=('sans-serif', 20, 'bold'), bd=5)
usernameLabel.grid(row=1, column=0, pady=10, padx=5)
usernameEntry = Entry(loginFrame, font=('sans-serif', 15), width=30, bd=5)
usernameEntry.grid(row=1, column=1, pady=10, padx=5)

passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT,
                      font=('sans-serif', 20, 'bold'), bd=5)
passwordLabel.grid(row=2, column=0, pady=10, padx=5)
passwordEntry = Entry(loginFrame, font=('sans-serif', 15), width=30, bd=5)
passwordEntry.grid(row=2, column=1, pady=10, padx=5)

loginButton = Button(loginFrame, text='Login', font=('sans-serif', 15, 'bold'), width=15, bg='SteelBlue1',
                     activebackground='SteelBlue2', activeforeground='white', cursor='hand2', command=login)
loginButton.grid(row=3, column=1)

# To run the window in loop to show it contineously
window.mainloop()
