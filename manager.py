import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import bcrypt
import sqlite3
from PIL import Image, ImageTk
import os
import datetime
import pandas as pd

from my_db_functions import *


class TreeViewFilter:
    def __init__(self, parent):
        self.tree = ttk.Treeview(parent)
        self.tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 9)))
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("#1", width=50, minwidth=50, stretch=tk.YES)
        self.tree.column("#2", width=100, stretch=tk.NO)
        self.tree.column("#3", width=100, stretch=tk.NO)
        self.tree.column("#4", width=110, stretch=tk.NO)
        self.tree.column("#5", width=50, minwidth=50, stretch=tk.NO)
        self.tree.column("#6", width=40, minwidth=40, stretch=tk.NO)
        self.tree.column("#7", width=80, minwidth=80, stretch=tk.NO)
        self.tree.column("#8", width=150, stretch=tk.NO)
        self.tree.heading('#0', text="",command= lambda col='#0' : self.sort(col))
        self.tree.heading('#1', text="sid",command= lambda col='studentID' : self.sort(col))
        self.tree.heading('#2', text="Last Name",command= lambda col='Lastname' : self.sort(col))
        self.tree.heading('#3', text="First Name",command= lambda col='Firstname' : self.sort(col))
        self.tree.heading('#4', text="Middle Name",command= lambda col='Middlename' : self.sort(col))
        self.tree.heading('#5', text="Gender",command= lambda col='Gender' : self.sort(col))
        self.tree.heading('#6', text="Age",command= lambda col='Age' : self.sort(col))
        self.tree.heading('#7', text="Class",command= lambda col='Table' : self.sort(col))
        self.tree.heading('#8', text="Guardian Name",command= lambda col='Guardian' : self.sort(col))
        self.tree['height'] = 16
        self.tree.place(x=20, y=70)

        self.count_label = tk.Label(parent, text="Total: 0")
        self.count_label.place(x=640, y=35)

        self.age_entry = tk.Entry(parent, width=7)
        self.age_entry.place(x=380, y=35)
        self.age_entry.bind("<Return>", self.filter_callback)

        self.hitEnter = tk.Label(parent,text="hit enter to sort!")

        self.populate_treeview()

        self.class_selected = StringVar()
        self.class_selected.trace("w", self.filter_callback)
        self.class_values = ['', 'final', 'one', 'two', 'three', 'four', 'five',
                             'six']  ########################use the classes db to populate
        self.class_combobox = AutocompleteCombobox(parent, width=7, textvariable=self.class_selected)
        self.class_combobox.set_completion_list(self.class_values)
        self.class_combobox.place(x=80, y=35)

        self.gender_selected = StringVar()
        self.gender_selected.trace("w", self.filter_callback)
        self.gender_values = ['', 'Male', 'Female']  ########################use the gender db to populate
        self.gender_combobox = AutocompleteCombobox(parent, width=7, textvariable=self.gender_selected)
        self.gender_combobox.set_completion_list(self.gender_values)
        self.gender_combobox.place(x=230, y=35)

        clear_filter = tk.Button(parent, text='clear filter', command=lambda: self.clear())
        clear_filter.place(x=460, y=20)



        self.update_count_label()


        self.order = True



    def populate_treeview(self):
        conn = sqlite3.connect('db/students.db')
        cursor = conn.cursor()

        data = []
        for table_name in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            for row in cursor.execute(
                    f"SELECT studentID, Lastname, Firstname, Middlename, Gender, Age, GuardianFirstName,GuardianLastName FROM {table_name[0]}"):
                parent_name = (row[6] + " " + row[7])
                # calculate the DOB
                dob = datetime.datetime.strptime(row[5], "%d-%B-%Y").date()
                age = datetime.datetime.now().year - dob.year

                values = (row[0], row[1], row[2], row[3], row[4], age, table_name[0], parent_name)
                data.append(values)

        cursor.close()
        conn.close()

        self.df = pd.DataFrame(data, columns=['studentID', 'Lastname', 'Firstname', 'Middlename', 'Gender', 'Age', 'Table',
                                         'Guardian'])

        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=row.tolist())

        self.update_count_label()

    def filter_callback(self, *args):
        class_filter_str = self.class_selected.get()
        gender_filter_str = self.gender_selected.get()
        age_filter_str = self.age_entry.get()

        if class_filter_str or gender_filter_str or age_filter_str:
            children = self.tree.get_children()
            for child in children:
                values = self.tree.item(child)["values"]
                if values:
                    class_match = class_filter_str.lower() in values[6].lower() if class_filter_str else True
                    gender_match = gender_filter_str.lower() in values[4].lower() if gender_filter_str else True
                    age_match = age_filter_str == str(values[5]) if age_filter_str else True

                    if not (class_match and gender_match and age_match):
                        self.tree.detach(child)
                    self.update_count_label()
        else:
            self.tree.delete(*self.tree.get_children())
            self.populate_treeview()
            self.update_count_label()

    def update_count_label(self):
        # get the number of items present in the treeview
        count = len(self.tree.get_children())


        # update the count label
        self.count_label.config(text=f"Total: {count}")

    def  sort(self,col):
        global df

        if self.order:
            self.order=False
        else:
            self.order = True

        self.df=self.df.sort_values(by=[col],ascending=self.order)

        self.update_treeview()

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for index, row in self.df.iterrows():
            self.tree.insert("", "end", values=row.tolist())

    def clear(self):
        self.age_entry.delete(0, 'end')
        self.class_selected.set('')
        self.gender_selected.set('')

        print("is it working?")





class User:
    username = ''
    privilege = ''
    gate = ''

def enter_pressed():
    print('enter pressed')

class AutocompleteCombobox(ttk.Combobox):

    def set_completion_list(self, completion_list):
        """Use our completion list as our drop down selection menu, arrows move through menu."""
        self._completion_list = sorted(completion_list, key=str.lower)  # Work with a sorted list
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list  # Setup our popup menu

    def autocomplete(self, delta=0):
        """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
        if delta:  # need to delete selection otherwise we would fix the current position
            self.delete(self.position, tk.END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):  # Match case insensitively
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, tk.END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, tk.END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(tk.INSERT), tk.END)
            self.position = self.index(tk.END)
        if event.keysym == "Left":
            if self.position < self.index(tk.END):  # delete the selection
                self.delete(self.position, tk.END)
            else:
                self.position = self.position - 1  # delete one character
                self.delete(self.position, tk.END)
        if event.keysym == "Right":
            self.position = self.index(tk.END)  # go to end (no selection)
        if event.keysym == "Return":
            enter_pressed()

        if len(event.keysym) == 1:
            self.autocomplete()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def checksum():

            username=username_box.get()
            input_password = passwd_box.get()

            fetched_info = get_password(username)

            hashed_password=fetched_info[0]
            priviledge=fetched_info[1]
            User.username=username
            User.privilege=priviledge
            # print(User.privilege)

            if len(username )==0:
                messagebox.showerror('Error',
                                     'Please enter your username!')
                return

            if len(input_password)==0:
                messagebox.showerror('Error',
                                     'Please enter your password!')
                return

            if is_valid_password(input_password, hashed_password):
                if User.privilege=="coordinator":
                    controller.show_frame(Library)
                if User.privilege=="manager":
                    controller.show_frame(MainPage)
                if User.privilege=="admin":
                    controller.show_frame(Lobby)
                print('Password is valid')
                passwd_box.delete(0, tk.END)
                tell.config(text="")   #the label for wrong message
            else:
                tell.config(text="wrong username or password!")   #like this :)

                print('Password is not valid')




        def is_valid_password(password, hashed_password):
            # Check if the password matches the hashed password
            return bcrypt.checkpw(password.encode(), hashed_password)



        def get_password(username):
            conn = sqlite3.connect('users.db')      #create the users db on create account in another function for this to work
            c = conn.cursor()
            c.execute('SELECT password,user_privilege FROM users WHERE username=?', (username,))
            row = c.fetchall()
            if row:
                conn.close()
                return row[0]
            else:
                return None

        def toggle_show_password():
            if passwd_box['show'] == '*':
                passwd_box.configure(show='')
                show_password.configure(image=eyeOpen)
            else:
                passwd_box.configure(show='*')
                show_password.configure(image=eyeClose)





        mainframe = tk.Frame(self, bg="#cdcfdc")
        mainframe.pack(fill=BOTH, expand=True)

        main_bg = ImageTk.PhotoImage(Image.open('final_event/images/bg_checksum_login.png').resize((1080, 620)))
        login_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/login.png'))

        eyeOpen = ImageTk.PhotoImage(Image.open('final_event/images/buttons/eye open.png').resize((23, 16)))
        eyeClose = ImageTk.PhotoImage(Image.open('final_event/images/buttons/eye close.png').resize((23, 16)))

        main_bg_label = tk.Label(mainframe, image=main_bg, bg="#7b8c9a", borderwidth=0)
        main_bg_label.image = main_bg
        main_bg_label.place(x=0, y=0)

        login_btn=tk.Button(mainframe,image=login_icon,bg="#7b8c9a",borderwidth=0,command=checksum)
        login_btn.image=login_icon
        login_btn.place(x=125,y=440)

        username_box=tk.Entry(mainframe,width=29,borderwidth=0)
        username_box.place(x=128,y=275)
        username_box.focus_set()

        line=tk.Label(mainframe,width=24,bg='grey')
        line.place(x=130,y=292,height=1)

        line1 = tk.Label(mainframe, width=24, bg='grey')
        line1.place(x=130, y=384, height=1)

        passwd_box = tk.Entry(mainframe, width=29,borderwidth=0,show="*")
        passwd_box.place(x=128, y=367)

        show_password=tk.Button(mainframe,image=eyeClose,borderwidth=0 ,bg="white",command= lambda: toggle_show_password())
        show_password.place(x=300,y=370)

        tell = tk.Label(mainframe, text="", bg="#7b8c9a")
        tell.place(x=135, y=418)

        username_box.bind('<Return>', lambda event: passwd_box.focus())
        passwd_box.bind('<Return>', lambda event: checksum())

class Lobby(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def access_create_event(page):
            if User.privilege == "admin":
                controller.show_frame(page)

            else:
                messagebox.showerror("Access Denied!", "You dont have required permission to access this page")

        def on_enter(e):
            home_btn["image"] = gohomeBtnHover

        def on_leave(e):
            home_btn["image"] = gohomeicon

        def on_enter1(e):
            manage_btn["image"] = examinationBtnHover

        def on_leave1(e):
            manage_btn["image"] = examinationicon

        def on_enter2(e):
            library_btn["image"] = libraryBtnHover

        def on_leave2(e):
            library_btn["image"] = libraryicon

        mainframe = tk.Frame(self, bg="#cdcfdc")
        mainframe.pack(fill=BOTH, expand=True)

        main_bg = ImageTk.PhotoImage(Image.open('final_event/images/checksum_school_bg.png').resize((1080, 620)))
        gohomeicon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/home_school.png'))
        examinationicon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/examination.png'))
        libraryicon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/library.png'))

        gohomeBtnHover = ImageTk.PhotoImage(Image.open('final_event/images/buttons/home_school_hover.png'))
        examinationBtnHover = ImageTk.PhotoImage(Image.open('final_event/images/buttons/examination_hover.png'))
        libraryBtnHover = ImageTk.PhotoImage(Image.open('final_event/images/buttons/library_hover.png'))

        goback = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button.png').resize((40, 40)))
        gobackhover = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/back button hover.png').resize((40, 40)))

        main_bg_label = tk.Label(mainframe, image=main_bg, bg="#7b8c9a", borderwidth=0)
        main_bg_label.image = main_bg
        main_bg_label.place(x=0, y=0)

        home_btn = tk.Button(mainframe, image=gohomeicon, bg="#7b8c9a", borderwidth=0,
                             command=lambda: access_create_event(MainPage))
        home_btn.image = gohomeicon
        home_btn.place(x=170, y=190)

        manage_btn = tk.Button(mainframe, image=examinationicon, bg="#7b8c9a", borderwidth=0,
                               command=lambda: controller.show_frame(Library))
        manage_btn.image = examinationicon
        manage_btn.place(x=170, y=290)

        library_btn = tk.Button(mainframe, image=libraryicon, bg="#7b8c9a", borderwidth=0,
                                command=lambda: access_create_event(Lobby))
        library_btn.image = libraryicon
        library_btn.place(x=170, y=390)

        back_Button = tk.Button(mainframe, image=goback, bg="#7c8d9a", borderwidth=0,
                                command=lambda: controller.show_frame(LoginPage))
        back_Button.image = goback
        back_Button.place(x=5, y=5)

        home_btn.bind("<Enter>", on_enter)
        home_btn.bind("<Leave>", on_leave)

        manage_btn.bind("<Enter>", on_enter1)
        manage_btn.bind("<Leave>", on_leave1)

        library_btn.bind("<Enter>", on_enter2)
        library_btn.bind("<Leave>", on_leave2)



class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.studentpage = ''

        def toggle_button(self):
            if self.studentpage == 'view':
                indicate(self.toggle_option, self.view_students, new_student)
                # print(f'should go to {self.studentpage} student')
                self.studentpage = 'add'
                # print(self.studentpage)
                return
            if self.studentpage == 'add':
                indicate(self.toggle_option, self.add_student, students)
                # print(f'should go to {self.studentpage} student')
                self.studentpage = 'view'
                # print(self.studentpage)
                return

            # print(self.studentpage)



        def back_button():

            controller.show_frame(Lobby)
            for frame in contentframe.winfo_children():
                frame.destroy()



        def home_window(self, contentframe):
            user_bg = tk.Label(pageframe, image=user_bg_box, bg='#e0e0e0')
            user_bg.image = user_bg_box
            user_bg.place(x=560, y=20)

            user_settings = tk.Button(pageframe, image=user_settings_icon, bg="white", borderwidth=0)
            user_settings.image = user_settings_icon
            user_settings.place(x=660, y=24)

            page_label = tk.Label(pageframe, text='Home', bg="#e0e0e0", font=('Times New Roman', 15, "bold"))
            page_label.place(x=250, y=30)

        def students(self, contentframe):

            self.studentpage = 'view'

            user_bg = tk.Label(pageframe, image=user_bg_box, bg='#e0e0e0')
            user_bg.image=user_bg_box
            user_bg.place(x=560,y=20)

            user_settings = tk.Button(pageframe, image=user_settings_icon, bg="white", borderwidth=0)
            user_settings.image = user_settings_icon
            user_settings.place(x=660, y=24)

            page_label = tk.Label(pageframe, text='Students', bg="#e0e0e0", font=('Times New Roman', 15, "bold"))
            page_label.place(x=250, y=30)
#######################################################################################################################


            class_box_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/class box.png').resize((75, 60)))
            gender_box_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/gender box.png').resize((75, 60)))
            age_box_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/age box.png').resize((75, 60)))
            population_box_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/population box.png').resize((75, 60)))

            self.toggle_option = tk.Button(pageframe, image=self.add_student, bg="#e0e0e0", borderwidth=0, command=lambda:toggle_button(self))
            self.toggle_option.image = self.add_student
            self.toggle_option.place(x=10,y=60)

            class_box = tk.Button(contentframe, image=class_box_icon, borderwidth=0)
            class_box.image=class_box_icon
            class_box.place(x=10, y=10)

            class_label = tk.Label(contentframe, text='Select Class', borderwidth=0)
            class_label.place(x=80, y=17)





            gender_box = tk.Button(contentframe, image=gender_box_icon, borderwidth=0)
            gender_box.image= gender_box_icon
            gender_box.place(x=160, y=10)

            gender_label = tk.Label(contentframe, text='Gender', borderwidth=0)
            gender_label.place(x=230, y=17)




            age_box = tk.Button(contentframe, image=age_box_icon, borderwidth=0)
            age_box.image = age_box_icon
            age_box.place(x=310, y=10)

            age_label = tk.Label(contentframe, text='Age', borderwidth=0)
            age_label.place(x=380, y=17)

            population_box = tk.Button(contentframe, image=population_box_icon, borderwidth=0)
            population_box.image = population_box_icon
            population_box.place(x=550, y=10)

            population_label = tk.Label(contentframe, text='Population', borderwidth=0)
            population_label.place(x=620, y=17)



            treeview_filter = TreeViewFilter(contentframe)


            # create_treeview()
            # update_treeview()

        def new_student(self, contentframe):


            user_bg = tk.Label(pageframe, image=user_bg_box, bg='#e0e0e0')
            user_bg.image = user_bg_box
            user_bg.place(x=560, y=20)

            user_settings = tk.Button(pageframe, image=user_settings_icon, bg="white", borderwidth=0)
            user_settings.image = user_settings_icon
            user_settings.place(x=660, y=24)

            page_label = tk.Label(pageframe, text='Students Registration Form', bg="#e0e0e0", font=('Times New Roman', 15, "bold"))
            page_label.place(x=240, y=30)

            self.toggle_option = tk.Button(pageframe, image=self.view_students, bg="#e0e0e0", borderwidth=0,
                                           command=lambda: toggle_button(self))
            self.toggle_option.image = self.view_students
            self.toggle_option.place(x=10, y=60)
            ######################################################################################################
            def on_entry_click(event, entry, entrybox_content, label, text):
                if entry.get() == entrybox_content:
                    entry.delete(0, "end")
                    entry.insert(0, '')
                    entry.config(fg='black')
                    label.config(text=text)

            def on_focusout(event, entry, entrybox_content, label, text):
                if entry.get() == '':
                    entry.insert(0, entrybox_content)
                    entry.config(fg='grey')
                    label.config(text='')
                else:
                    label.config(text=text)

            #######################################################################################################
            reg_form_bg = ImageTk.PhotoImage(Image.open('final_event/images/student reg form.png'))

            form_bg = tk.Label(contentframe,image=reg_form_bg,bg='#e0e0e0')
            form_bg.image = reg_form_bg
            form_bg.place(x=0,y=0)

            firstName = tk.Entry(contentframe,borderwidth=0,width=25,fg='grey')
            middleName = tk.Entry(contentframe,borderwidth=0,width=25,fg='grey')
            lastName = tk.Entry(contentframe,borderwidth=0,width=25,fg='grey')
            guardianFName = tk.Entry(contentframe, borderwidth=0, width=25,fg='grey')
            guardianLName = tk.Entry(contentframe, borderwidth=0, width=25,fg='grey')
            guardianPhone = tk.Entry(contentframe, borderwidth=0, width=25,fg='grey')
            currentClass = tk.Entry(contentframe, borderwidth=0, width=25,fg='grey')
            enrollmentDate = tk.Entry(contentframe, borderwidth=0, width=25,fg='grey')

            firstName.insert(0, "Enter first name here")
            middleName.insert(0, "Enter middle name here")
            lastName.insert(0, "Enter last name here")
            guardianFName.insert(0, "Guardian first name here")
            guardianLName.insert(0, "Guardian last name here")
            guardianPhone.insert(0, "Guardian phone number here")
            currentClass.insert(0, "Current class here")



            firstName.place(x=49,y=62)
            middleName.place(x=284, y=62)
            lastName.place(x=520, y=62)
            guardianFName.place(x=49, y=250)
            guardianLName.place(x=284, y=250)
            guardianPhone.place(x=520, y=250)
            currentClass.place(x=49, y=346)
            enrollmentDate.place(x=284, y=346)

            gender = StringVar()

            male_rad = tk.Radiobutton(contentframe, text="Male", padx=5, bg='#eeeeee',variable=gender, value="Male")
            female_rad = tk.Radiobutton(contentframe, text="Female", padx=20,bg='#eeeeee', variable=gender, value="Female")

            year = tk.StringVar()
            month = tk.StringVar()
            date = tk.StringVar()

            spinbox_year = tk.Spinbox(contentframe, from_=2000, to=2033, textvariable=year, width=6,
                                      borderwidth=0)
            spinbox_year.place(x=625, y=157)

            month=StringVar()
            search_values = ['January', 'February','March','April','June']  ##########################use the classes db to populate
            class_combobox = AutocompleteCombobox(contentframe, width=9,textvariable=month)
            class_combobox.set_completion_list(search_values)
            class_combobox.place(x=497, y=155)


            spinbox_date = tk.Spinbox(contentframe, from_=1, to=31, textvariable=date, width=6,
                                      borderwidth=0)
            spinbox_date.place(x=393, y=157)



            male_rad.place(x=72, y=160)
            female_rad.place(x=170, y=160)

            fNameLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            mNameLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            lNameLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            guardianFNameLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            guardianLNameLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            guardianPhoneLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            currentClassLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            enrolmentDateLabel = tk.Label(contentframe, text='~enrollment_date~', bg="#eeeeee", fg='#6a6a6a')
            dateLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            monthLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            yearLabel = tk.Label(contentframe, text='', bg="#eeeeee", fg='#6a6a6a')
            genderLabel = tk.Label(contentframe, text='Gender', bg='#eeeeee',fg='#6a6a6a').place(x=127, y=130)

            fNameLabel.place(x=49, y=30)
            mNameLabel.place(x=284, y=30)
            lNameLabel.place(x=520, y=30)
            guardianFNameLabel.place(x=49, y=218)
            guardianLNameLabel.place(x=284, y=218)
            guardianPhoneLabel.place(x=520, y=218)
            currentClassLabel.place(x=49, y=314)
            enrolmentDateLabel.place(x=284, y=314)
            dateLabel.place(x=393, y=130)
            monthLabel.place(x=497, y=130)
            yearLabel.place(x=625, y=130)

            age = date.get() + "-" + month.get() + "-" + year.get()



            submit= tk.Button(contentframe,text='submit',command=lambda:add_student(firstName.get(),middleName.get(),lastName.get(),guardianFName.get(),guardianLName.get(),guardianPhone.get(),currentClass.get(),enrollmentDate.get(),gender.get(),age))
            submit.place(x=550, y=346)



            firstName.bind('<FocusIn>',lambda event: on_entry_click(event, firstName, "Enter first name here", fNameLabel,"~first_name~"))
            firstName.bind('<FocusOut>',lambda event: on_focusout(event,firstName, "Enter first name here", fNameLabel,"~first_name~"))
            middleName.bind('<FocusIn>',lambda event: on_entry_click(event, middleName, "Enter middle name here", mNameLabel,"~middle_name~"))
            middleName.bind('<FocusOut>',lambda event: on_focusout(event, middleName, "Enter middle name here", mNameLabel,"~middle_name~"))
            lastName.bind('<FocusIn>',lambda event: on_entry_click(event, lastName, "Enter last name here", lNameLabel,"~last_name~"))
            lastName.bind('<FocusOut>',lambda event: on_focusout(event, lastName, "Enter last name here", lNameLabel,"~last_name~"))
            guardianFName.bind('<FocusIn>',lambda event: on_entry_click(event, guardianFName, "Guardian first name here", guardianFNameLabel,"~guardian_first_name~"))
            guardianFName.bind('<FocusOut>',lambda event: on_focusout(event, guardianFName, "Guardian first name here", guardianFNameLabel,"~guardian_first_name~"))
            guardianLName.bind('<FocusIn>',lambda event: on_entry_click(event, guardianLName, "Guardian last name here",guardianLNameLabel,"~guardian_last_name~"))
            guardianLName.bind('<FocusOut>',lambda event: on_focusout(event, guardianLName, "Guardian last name here", guardianLNameLabel,"~guardian_last_name~"))
            guardianPhone.bind('<FocusIn>',lambda event: on_entry_click(event, guardianPhone, "Guardian phone number here", guardianPhoneLabel,"~guardian_phone_number~"))
            guardianPhone.bind('<FocusOut>',lambda event: on_focusout(event, guardianPhone, "Guardian phone number here",guardianPhoneLabel,"~guardian_phone_number~"))
            currentClass.bind('<FocusIn>',lambda event: on_entry_click(event, currentClass, "Current class here", currentClassLabel,"~current_class~"))
            currentClass.bind('<FocusOut>',lambda event: on_focusout(event, currentClass, "Current class here", currentClassLabel,"~current_class~~"))














        def teachers(self, contentframe):
            pass

        def classes(self, contentframe):
            pass


        def hide_indicators():
            students_button["image"] = students_icon
            classes_button["image"] = classes_icon
            home_button["image"] = home_icon
            teachers_button['image'] = teachers_icon

        def delete_page(button):
            button=str(button)

            for frame in contentframe.winfo_children():
                frame.destroy()
            for frame in pageframe.winfo_children():
                frame.destroy()





        def indicate(button_pressed, button, page):
            # print(button_pressed)
            # maintains students button selection
            if str(button_pressed) != '.!frame.!mainpage.!frame2.!button3' and str(button_pressed) != '.!frame.!mainpage.!frame2.!button5':
                hide_indicators()
            button_pressed["image"] = button
            delete_page(button_pressed)
            page(self, contentframe)

##########################################################################################################################################

        mainframe = tk.Frame(self, bg="#9eadb9")
        mainframe.pack(fill=BOTH, expand=True)

        pageframe = tk.Frame(self, height=100, width=725, bg="#e0e0e0")
        pageframe.place(x=282, y=50)

        contentframe = tk.Frame(self, height=420, width=725)
        contentframe.place(x=282, y=140)

        manage_BG = ImageTk.PhotoImage(Image.open('final_event/images/manage dashboard.png'))

        manageBG = tk.Label(mainframe, image=manage_BG, bg='#9eadb9')
        manageBG.image = manage_BG
        manageBG.place(x=0, y=0)

        goback = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button.png').resize((40, 40)))
        gobackhover = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/back button hover.png').resize((40, 40)))

        home_icon = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/home.png').resize((148, 35)))
        students_icon = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/students.png').resize((148, 35)))
        teachers_icon = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/teacher.png').resize((148, 35)))
        classes_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/classes.png').resize((148, 35)))

        user_settings_icon = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/user settings.png').resize((36, 36)))

        home_icon_select = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/home select.png').resize((148, 35)))
        students_icon_select = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/students hover.png').resize((148, 35)))
        teachers_icon_select = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/teacher hover.png').resize((148, 35)))
        classes_icon_select = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/classes hover.png').resize((148, 35)))

        user_bg_box = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/user_bg_box.png').resize((150, 40)))
        self.user_settings_icon = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/user settings.png').resize((34, 34)))

        self.add_student = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/add student.png').resize((102, 25)))
        self.view_students = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/view student.png').resize((102, 25)))



        back_Button = tk.Button(mainframe, image=goback, bg="#7b8c9a", borderwidth=0,
                                command=back_button)
        back_Button.image = goback
        back_Button.place(x=70, y=55)

        buttonsframe = tk.Frame(mainframe, height=380, width=160, bg="#7b8c9a")
        buttonsframe.place(x=78, y=180)



        home_button = tk.Button(buttonsframe, image=home_icon, bg="#7b8c9a", borderwidth=0,
                                command=lambda: indicate(home_button, home_icon_select,
                                                         home_window))
        home_button.image = home_icon
        home_button.pack(pady=10)

        students_button = tk.Button(buttonsframe, image=students_icon, bg="#7b8c9a", borderwidth=0,
                                    command=lambda: indicate(students_button, students_icon_select,
                                                             students))
        students_button.image = students_icon
        students_button.pack(pady=10)

        teachers_button = tk.Button(buttonsframe, image=teachers_icon, bg="#7b8c9a", borderwidth=0,
                                    command=lambda: indicate(teachers_button, teachers_icon_select, teachers))
        teachers_button.image = teachers_icon
        teachers_button.pack(pady=10)

        classes_button = tk.Button(buttonsframe, image=classes_icon, bg="#7b8c9a", borderwidth=0, command=lambda: indicate(classes_button, classes_icon_select, classes))
        classes_button.image = classes_icon
        classes_button.pack(pady=10)

        currentuser = tk.Label(mainframe, text=User.username, bg="#f7ffff")
        currentuser.place(x=860, y=80)

        user_settings = tk.Button(mainframe, image=user_settings_icon, bg="#f7ffff", borderwidth=0)
        user_settings.image = user_settings_icon
        user_settings.place(x=935, y=70)

        logouticon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/logout.png').resize((80, 22)))

        logout = tk.Button(mainframe, image=logouticon, borderwidth=0, bg="#9eadb9",
                           command=lambda: controller.show_frame(LoginPage))
        logout.image = logouticon
        logout.place(x=65, y=5)

        indicate(home_button, home_icon_select,
                 home_window)


class Examination(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

class Library(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)




        # creating a window
        window = tk.Frame(self)

        window.pack()

        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()


        window.grid_rowconfigure(0, minsize=height)
        window.grid_columnconfigure(0, minsize=width)

        self.frames = {}
        for F in (LoginPage, Lobby, MainPage, Examination, Library):
            frame = F(window, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        frame = self.frames[page.__name__]
        frame.tkraise()
        self.title("Application")


# width = self.window.winfo_screenwidth()
# height = self.window.winfo_screenheight()


app = Application()
app.maxsize(1080, 620)
app.resizable(None,None)
app.mainloop()
