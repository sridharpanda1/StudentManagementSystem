import time
import ttkthemes
import pymysql
import pandas
from tkinter import *
from tkinter import ttk, messagebox, filedialog

# functionality part
count = 0
text = ''
def slider():
    global text, count
    if count == len(head):
        count = 0
        text = ''

    text = text + head[count]  # S ... after keep on updating
    sliderLabel.config(text=text)
    count = count + 1
    if count == len(head):
        # If the full line is printed, wait for 5 milliseconds before continuing
        sliderLabel.after(1500, slider)
    else:
        # If the full line is not printed yet, wait for 300 milliseconds before updating
        sliderLabel.after(300, slider)


def clock():
    global date
    global currentTime
    date = time.strftime('%d/%m/%Y')
    currentTime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currentTime}')
    datetimeLabel.after(1000, clock)


def connect_DB():
    def connect():
        global myCursor
        global con
        try:
            con = pymysql.connect(host=hostentry.get(), user=usernameentry.get(), password=passwordentry.get())
            #con = pymysql.connect(host='localhost', user='root', password='admin')
            myCursor = con.cursor()

        except:
            messagebox.showerror('Error', 'Please Check Your Credentials CAREFULLY', parent=connectDBWindow)
            return
        # try:
        #     query = 'create database student_management_system'
        #     myCursor.execute(query)
        #     query = 'use student_management_system'
        #     myCursor.execute(query)
        #     query = 'create table student(id int not null primary key, ' \
        #             'name varchar(30), mobile varchar(10),' \
        #             'email varchar(30), address varchar(100)' \
        #             'gender varchar(30), dob varchar(20)' \
        #             'date varchar(50), time varchar(30) )'
        #     myCursor.execute(query)
        # except:
        #     query = 'use student_management_system'
        #     myCursor.execute(query)
        query = 'use studentdata'
        myCursor.execute(query)
        messagebox.showinfo('Success', 'DB Connection is Successful', parent=connectDBWindow)
        connectDBWindow.destroy()
        addStudentButton.config(state=NORMAL)
        searchStudentButton.config(state=NORMAL)
        updateStudentButton.config(state=NORMAL)
        showStudentsButton.config(state=NORMAL)
        deleteStudentButton.config(state=NORMAL)
        exportDataButton.config(state=NORMAL)

    connectDBWindow = Toplevel()
    connectDBWindow.geometry('470x280+1000+230')
    connectDBWindow.title('DB Connection Window')
    connectDBWindow.resizable(0, 0)

    hostnameLabel = Label(connectDBWindow, text='Hostname', font=('sans-serif', 18, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=10, pady=20)
    hostentry = Entry(connectDBWindow, font=('sans-serif', 15, 'bold'), bd=5)
    hostentry.grid(row=0, column=1, padx=40, pady=20)

    usernameLabel = Label(connectDBWindow, text='Username', font=('sans-serif', 18, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=10, pady=20)
    usernameentry = Entry(connectDBWindow, font=('sans-serif', 15, 'bold'), bd=5)
    usernameentry.grid(row=1, column=1, padx=40, pady=20)

    passwordLabel = Label(connectDBWindow, text='Password', font=('sans-serif', 18, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=10, pady=20)
    passwordentry = Entry(connectDBWindow, font=('sans-serif', 15, 'bold'), bd=5)
    passwordentry.grid(row=2, column=1, padx=40, pady=20)

    connectButtonDB = ttk.Button(connectDBWindow, text='Connect', command=connect)
    connectButtonDB.grid(row=3, columnspan=2)


def add_student():
    def add_data():
        if idEntry.get() == '' or nameEntry.get() == '' or mobEntry.get() == '' or emailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or dobEntry.get() == '':
            messagebox.showerror('Error', 'All fields are REQUIRED.', parent=add_window)
        else:
            current_date = time.strftime('%d/%m/%Y')
            current_time = time.strftime('%H:%M:%S')
            try:
                query = 'insert into  student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                myCursor.execute(query, (idEntry.get(), nameEntry.get(), mobEntry.get(), emailEntry.get(),
                                         addressEntry.get(), genderEntry.get(), dobEntry.get(), current_date,
                                         current_time))
                con.commit()
                res = messagebox.askyesno('Confirmation', 'Data ADDED successfully. Do you want to clean the form???',
                                          parent=add_window)
                # print(res)
                if res:
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    mobEntry.delete(0, END)
                    emailEntry.delete(0, END)
                    addressEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    dobEntry.delete(0, END)
                else:
                    pass
            except:
                messagebox.showerror('Error', 'ID can not be REPEATED', parent=add_window)
                return

            query = 'select * from student'
            myCursor.execute(query)
            fetch_data = myCursor.fetchall()
            studentTable.delete(*studentTable.get_children())
            # print(fetch_data)
            for data in fetch_data:
                datalist = list(data)
                studentTable.insert('', END, values=datalist)

    add_window = Toplevel()
    add_window.grab_set()
    add_window.title('Add Student Window')
    add_window.geometry('550x550+300+20')
    add_window.resizable(0, 0)

    idLabel = Label(add_window, text='ID', font=('sans-serif', 20, 'bold'))
    idLabel.grid(padx=30, pady=15, sticky=W)
    idEntry = Entry(add_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    idEntry.grid(row=0, column=1, padx=15, pady=15)

    nameLabel = Label(add_window, text='Name', font=('sans-serif', 20, 'bold'))
    nameLabel.grid(padx=30, pady=15, sticky=W)
    nameEntry = Entry(add_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    nameEntry.grid(row=1, column=1, padx=15, pady=15)

    mobLabel = Label(add_window, text='Contact No.', font=('sans-serif', 20, 'bold'))
    mobLabel.grid(padx=30, pady=15, sticky=W)
    mobEntry = Entry(add_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    mobEntry.grid(row=2, column=1, padx=15, pady=15)

    emailLabel = Label(add_window, text='Email', font=('sans-serif', 20, 'bold'))
    emailLabel.grid(padx=30, pady=15, sticky=W)
    emailEntry = Entry(add_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    emailEntry.grid(row=3, column=1, padx=15, pady=15)

    addressLabel = Label(add_window, text='Address', font=('sans-serif', 20, 'bold'))
    addressLabel.grid(padx=30, pady=15, sticky=W)
    addressEntry = Entry(add_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    addressEntry.grid(row=4, column=1, padx=15, pady=15)

    genderLabel = Label(add_window, text='Gender', font=('sans-serif', 20, 'bold'))
    genderLabel.grid(padx=30, pady=15, sticky=W)
    genderEntry = Entry(add_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    genderEntry.grid(row=5, column=1, padx=15, pady=15)

    dobLabel = Label(add_window, text='D.O.B.', font=('sans-serif', 20, 'bold'))
    dobLabel.grid(padx=30, pady=15, sticky=W)
    dobEntry = Entry(add_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    dobEntry.grid(row=6, column=1, padx=15, pady=15)

    addStudentButton = ttk.Button(add_window, text='Add', command=add_data)
    addStudentButton.grid(row=9, columnspan=2, padx=15, pady=15)


def search_student():
    def search_data():
        query = 'select *from student where id = %s or name = %s or mobile = %s or email = %s or address = %s or gender = %s or dob = %s'
        myCursor.execute(query, (
        idEntry.get(), nameEntry.get(), mobEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(),
        dobEntry.get()))

        studentTable.delete(*studentTable.get_children())
        fetched_data = myCursor.fetchall()

        # check if the fetched_data list is empty, which indicates no record was found
        if not fetched_data:
            messagebox.showwarning("Record Not Found",
                                   "No record was found with the entered details. Please try again.",
                                   parent=search_window)
        else:
            # display the fetched data in the studentTable widget
            for data in fetched_data:
                studentTable.insert('', END, values=data)

    search_window = Toplevel()
    search_window.grab_set()
    search_window.title('Search Student Window')
    search_window.geometry('550x550+300+20')
    search_window.resizable(0, 0)

    idLabel = Label(search_window, text='ID', font=('sans-serif', 20, 'bold'))
    idLabel.grid(padx=30, pady=15, sticky=W)
    idEntry = Entry(search_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    idEntry.grid(row=0, column=1, padx=15, pady=15)

    nameLabel = Label(search_window, text='Name', font=('sans-serif', 20, 'bold'))
    nameLabel.grid(padx=30, pady=15, sticky=W)
    nameEntry = Entry(search_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    nameEntry.grid(row=1, column=1, padx=15, pady=15)

    mobLabel = Label(search_window, text='Contact No.', font=('sans-serif', 20, 'bold'))
    mobLabel.grid(padx=30, pady=15, sticky=W)
    mobEntry = Entry(search_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    mobEntry.grid(row=2, column=1, padx=15, pady=15)

    emailLabel = Label(search_window, text='Email', font=('sans-serif', 20, 'bold'))
    emailLabel.grid(padx=30, pady=15, sticky=W)
    emailEntry = Entry(search_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    emailEntry.grid(row=3, column=1, padx=15, pady=15)

    addressLabel = Label(search_window, text='Address', font=('sans-serif', 20, 'bold'))
    addressLabel.grid(padx=30, pady=15, sticky=W)
    addressEntry = Entry(search_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    addressEntry.grid(row=4, column=1, padx=15, pady=15)

    genderLabel = Label(search_window, text='Gender', font=('sans-serif', 20, 'bold'))
    genderLabel.grid(padx=30, pady=15, sticky=W)
    genderEntry = Entry(search_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    genderEntry.grid(row=5, column=1, padx=15, pady=15)

    dobLabel = Label(search_window, text='D.O.B.', font=('sans-serif', 20, 'bold'))
    dobLabel.grid(padx=30, pady=15, sticky=W)
    dobEntry = Entry(search_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    dobEntry.grid(row=6, column=1, padx=15, pady=15)

    searchStudentButton = ttk.Button(search_window, text='Search', command=search_data)
    searchStudentButton.grid(row=9, columnspan=2, padx=15, pady=15)


def show_students():
    query = 'select * from student'
    myCursor.execute(query)
    fetched_data = myCursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def update_student():
    def update_data():
        query = 'update student set name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s, date=%s, time=%s where id=%s'
        myCursor.execute(query, (nameEntry.get(), mobEntry.get(), emailEntry.get(), addressEntry.get(),
                                 genderEntry.get(), dobEntry.get(), date, currentTime, idEntry.get()))
        con.commit()
        messagebox.showinfo('Success', f'ID {idEntry.get()} is MODIFIED successfully.')
        update_window.destroy()
        query = 'select * from student'
        show_students()

    update_window = Toplevel()
    update_window.grab_set()
    update_window.title('Update Student Window')
    update_window.geometry('550x550+300+20')
    update_window.resizable(0, 0)

    idLabel = Label(update_window, text='ID', font=('sans-serif', 20, 'bold'))
    idLabel.grid(padx=30, pady=15, sticky=W)
    idEntry = Entry(update_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    idEntry.grid(row=0, column=1, padx=15, pady=15)

    nameLabel = Label(update_window, text='Name', font=('sans-serif', 20, 'bold'))
    nameLabel.grid(padx=30, pady=15, sticky=W)
    nameEntry = Entry(update_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    nameEntry.grid(row=1, column=1, padx=15, pady=15)

    mobLabel = Label(update_window, text='Contact No.', font=('sans-serif', 20, 'bold'))
    mobLabel.grid(padx=30, pady=15, sticky=W)
    mobEntry = Entry(update_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    mobEntry.grid(row=2, column=1, padx=15, pady=15)

    emailLabel = Label(update_window, text='Email', font=('sans-serif', 20, 'bold'))
    emailLabel.grid(padx=30, pady=15, sticky=W)
    emailEntry = Entry(update_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    emailEntry.grid(row=3, column=1, padx=15, pady=15)

    addressLabel = Label(update_window, text='Address', font=('sans-serif', 20, 'bold'))
    addressLabel.grid(padx=30, pady=15, sticky=W)
    addressEntry = Entry(update_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    addressEntry.grid(row=4, column=1, padx=15, pady=15)

    genderLabel = Label(update_window, text='Gender', font=('sans-serif', 20, 'bold'))
    genderLabel.grid(padx=30, pady=15, sticky=W)
    genderEntry = Entry(update_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    genderEntry.grid(row=5, column=1, padx=15, pady=15)

    dobLabel = Label(update_window, text='D.O.B.', font=('sans-serif', 20, 'bold'))
    dobLabel.grid(padx=30, pady=15, sticky=W)
    dobEntry = Entry(update_window, font=('sans-serif', 15, 'bold'), width=24, bd=5)
    dobEntry.grid(row=6, column=1, padx=15, pady=15)

    updateStudentButton = ttk.Button(update_window, text='Update', command=update_data)
    updateStudentButton.grid(row=9, columnspan=2, padx=15, pady=15)

    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    listData = content['values']
    idEntry.insert(0, listData[0])
    nameEntry.insert(0, listData[1])
    mobEntry.insert(0, listData[2])
    emailEntry.insert(0, listData[3])
    addressEntry.insert(0, listData[4])
    genderEntry.insert(0, listData[5])
    dobEntry.insert(0, listData[6])


def delete_student():
    indexing = studentTable.focus()
    # print(indexing)
    content = studentTable.item(indexing)
    # print(content)
    contentID = content['values'][0]
    query = 'delete from student where id=%s'
    myCursor.execute(query, contentID)
    con.commit()
    messagebox.showinfo('Deleted', f'The ID {contentID} is DELETED successfully.')
    query = 'select * from student'
    myCursor.execute(query)
    fetched_data = myCursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def export_data():
    url = filedialog.asksaveasfile(defaultextension=' .csv')
    indexing = studentTable.get_children()
    new_list = []
    for index in indexing:
        content = studentTable.item(index)
        data_list = content['values']
        new_list.append(data_list)

    table = pandas.DataFrame(new_list, columns=['ID', 'Name', 'Contact No.', 'E-Mail', 'Address',
                                                'Gender', 'D.O.B.', 'Created Date', 'Created Time'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data EXPORTED to CSV successfully.')

def exit_sys():
    res = messagebox.askyesno('Confirmation', 'Do you want to Exit?')
    if res:
        root.destroy()
    else:
        pass

# GUI part
root = ttkthemes.ThemedTk()

root.get_themes()

root.set_theme('breeze')

root.geometry('1500x750+10+20')
root.resizable(0, 0)
root.title('Welcome to Student Management System')

datetimeLabel = Label(root, font=('sans-serif', 18, 'bold'))
datetimeLabel.place(x=5, y=5)
clock()

head = 'Welcome to Student Management System'
sliderLabel = Label(root, font=('arial', 28, 'bold', 'underline'), width=50)
sliderLabel.place(x=200, y=5)
slider()

connectButton = ttk.Button(root, text='Connect to DB', command=connect_DB)
connectButton.place(x=1200, y=0)

leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=600)

logo_img = PhotoImage(file='audience.png')
logo_Label = Label(leftFrame, image=logo_img)
logo_Label.grid(row=0, column=0)

addStudentButton = ttk.Button(leftFrame, text='Add Student', width=20, state=DISABLED, command=add_student)
addStudentButton.grid(row=1, column=0, pady=20)

searchStudentButton = ttk.Button(leftFrame, text='Search Student', width=20, state=DISABLED, command=search_student)
searchStudentButton.grid(row=2, column=0, pady=20)

showStudentsButton = ttk.Button(leftFrame, text='Show Students', width=20, state=DISABLED, command=show_students)
showStudentsButton.grid(row=3, column=0, pady=20)

updateStudentButton = ttk.Button(leftFrame, text='Update Student', width=20, state=DISABLED, command=update_student)
updateStudentButton.grid(row=4, column=0, pady=20)

deleteStudentButton = ttk.Button(leftFrame, text='Delete Student', width=20, state=DISABLED, command=delete_student)
deleteStudentButton.grid(row=5, column=0, pady=20)

exportDataButton = ttk.Button(leftFrame, text='Export Data', width=20, state=DISABLED, command=export_data)
exportDataButton.grid(row=6, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text='Exit', width=20, command=exit_sys)
exitButton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=1100, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('ID', 'Name', 'Contact No.', 'E-Mail', 'Address', 'Gender'
                                                 , 'D.O.B.', 'Created Date', 'Created Time'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH, expand=1)

studentTable.heading('ID', text='ID')
studentTable.heading('Name', text='Name')
studentTable.heading('Contact No.', text='Contact No.')
studentTable.heading('E-Mail', text='E-Mail')
studentTable.heading('Address', text='Address')
studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B.', text='D.O.B.')
studentTable.heading('Created Date', text='Created Date')
studentTable.heading('Created Time', text='Created Time')

studentTable.column('ID', width=50, anchor=CENTER)
studentTable.column('Name', width=150, anchor=CENTER)
studentTable.column('Contact No.', width=100, anchor=CENTER)
studentTable.column('E-Mail', width=200, anchor=CENTER)
studentTable.column('Address', width=200, anchor=CENTER)
studentTable.column('Gender', width=80, anchor=CENTER)
studentTable.column('D.O.B.', width=90, anchor=CENTER)
studentTable.column('Created Date', width=100, anchor=CENTER)
studentTable.column('Created Time', width=100, anchor=CENTER)

styleTree = ttk.Style()
styleTree.configure('Treeview', rowhight=30, font=('arial', 12), foreground='red4')

studentTable.config(show='headings')

root.mainloop()
