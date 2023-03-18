import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
import os
import sqlite3
import csv
# import cv2
import bcrypt
import re                       #Regular Strings--for validating password

#my library imports
from ticket_creator import *
from save_events_2database import *
from checkin_algorithm import *
from camera_ticket_validator import check_ticket_if_valid_fr

class User:
    username = ''
    privilege = ''
    gate = ''


User.gate="mainGate"










class CreateUser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        def hash_password(password):
            # Hash the password using bcrypt
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode(), salt)
            return hashed_password


        def add_user(username, password,privilege):
            password = hash_password(password)
            # create connection to SQLite database
            conn = sqlite3.connect('users.db')
            c = conn.cursor()

            # create table to store user account information
            conn.execute(
                '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, user_privilege TEXT NOT NULL,password TEXT NOT NULL)''')

            # insert user into SQLite database
            c.execute("INSERT INTO users (username, password, user_privilege) VALUES (?, ?, ?)",
                      (username, password, privilege))

            conn.commit()
            conn.close()

        def validate_input(username, password):
            # validate username
            if not re.match(r'^\w{3,}$', username):
                messagebox.showerror('Error',
                                     'Username must be at least 3 characters and can only contain letters, numbers, and underscore')
                return False

            # validate password
            if not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{8,}$', password):
                messagebox.showerror('Error',
                                     'Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter, one number, and one special character (@#$%^&+=)')
                return False

            return True

        def create_user():
            username = username_box.get()
            password = passwd_box.get()
            priviledge=priviledge_box.get()

            # validate input
            if not validate_input(username, password):
                return

            # add user to database
            add_user(username, password,priviledge)
            messagebox.showinfo('Success', 'User added!')


        mainframe = tk.Frame(self, bg="#cdcfdc")
        mainframe.pack(fill=BOTH, expand=True)

        main_bg = ImageTk.PhotoImage(Image.open('final_event/images/bg_checksum_create_user.png').resize((1080, 620)))
        createUser_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/create user.png'))

        goback = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button.png').resize((40, 40)))
        gobackhover = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/back button hover.png').resize((40, 40)))



        main_bg_label = tk.Label(mainframe, image=main_bg, bg="#7b8c9a", borderwidth=0)
        main_bg_label.image = main_bg
        main_bg_label.place(x=0, y=0)

        createUser_btn=tk.Button(mainframe,image=createUser_icon,bg="#7b8c9a",borderwidth=0,command=create_user)
        createUser_btn.image=createUser_icon
        createUser_btn.place(x=100,y=490)

        username_box=tk.Entry(mainframe,width=29,borderwidth=0)
        username_box.place(x=128,y=275)

        line=tk.Label(mainframe,width=24,bg='grey')
        line.place(x=130,y=292,height=1)

        line1 = tk.Label(mainframe, width=24, bg='grey')
        line1.place(x=130, y=384, height=1)

        passwd_box = tk.Entry(mainframe, width=29,borderwidth=0,show="*")
        passwd_box.place(x=128, y=367)

        self.priviledge=tk.StringVar()

        priviledge_box = ttk.Combobox(mainframe, textvariable=self.priviledge)
        priviledge_box['values'] =  ['admin','manager','coordinator']
        priviledge_box.current(0)
        priviledge_box.place(x=150, y=420)



        tell = tk.Label(mainframe, text="", bg="#7b8c9a")
        tell.place(x=135, y=418)

        back_Button = tk.Button(mainframe, image=goback, bg="#7c8d9a", borderwidth=0,
                                command=lambda: controller.show_frame(MainPage))
        back_Button.image = goback
        back_Button.place(x=5, y=5)


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
                    controller.show_frame(SecondPage)
                if User.privilege=="manager":
                    controller.show_frame(MainPage)
                if User.privilege=="admin":
                    controller.show_frame(MainPage)
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

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def access_create_event(page):
            if User.privilege=="admin":
                controller.show_frame(page)
            else:
                messagebox.showerror("Access Denied!", "You dont have required permission to access this page")


        def on_enter(e):
            create_btn["image"] = createBtnHover

        def on_leave(e):
            create_btn["image"] = createBtn

        def on_enter1(e):
            manage_btn["image"] = manageBtnHover

        def on_leave1(e):
            manage_btn["image"] = manageBtn

        def on_enter2(e):
            create_user_btn["image"] = createUserBtnHover

        def on_leave2(e):
            create_user_btn["image"] = createUserBtn

        mainframe = tk.Frame(self, bg="#cdcfdc")
        mainframe.pack(fill=BOTH, expand=True)

        main_bg = ImageTk.PhotoImage(Image.open('final_event/images/checksum_event_bg.png').resize((1080, 620)))
        createBtn = ImageTk.PhotoImage(Image.open('final_event/images/buttons/create event.png'))
        manageBtn = ImageTk.PhotoImage(Image.open('final_event/images/buttons/manage event.png'))
        createUserBtn = ImageTk.PhotoImage(Image.open('final_event/images/buttons/create user.png'))

        createBtnHover = ImageTk.PhotoImage(Image.open('final_event/images/buttons/create event hover.png'))
        manageBtnHover = ImageTk.PhotoImage(Image.open('final_event/images/buttons/manage event hover.png'))
        createUserBtnHover = ImageTk.PhotoImage(Image.open('final_event/images/buttons/create user hover.png'))

        goback = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button.png').resize((40, 40)))
        gobackhover = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/back button hover.png').resize((40, 40)))




        main_bg_label=tk.Label(mainframe,image=main_bg,bg="#7b8c9a",borderwidth=0)
        main_bg_label.image=main_bg
        main_bg_label.place(x=0,y=0)

        create_btn = tk.Button(mainframe,image=createBtn,bg="#7b8c9a",borderwidth=0,command=lambda: access_create_event(FirstPage))
        create_btn.image=createBtn
        create_btn.place(x=170,y=190)

        manage_btn = tk.Button(mainframe, image=manageBtn, bg="#7b8c9a", borderwidth=0,command=lambda: controller.show_frame(SecondPage))
        manage_btn.image = manageBtn
        manage_btn.place(x=170, y=290)

        create_user_btn = tk.Button(mainframe, image=createUserBtn, bg="#7b8c9a", borderwidth=0,
                               command=lambda: access_create_event(CreateUser))
        create_user_btn.image = createUserBtn
        create_user_btn.place(x=170, y=390)

        back_Button = tk.Button(mainframe, image=goback, bg="#7c8d9a", borderwidth=0,
                                command=lambda: controller.show_frame(LoginPage))
        back_Button.image = goback
        back_Button.place(x=5, y=5)

        create_btn.bind("<Enter>", on_enter)
        create_btn.bind("<Leave>", on_leave)

        manage_btn.bind("<Enter>", on_enter1)
        manage_btn.bind("<Leave>", on_leave1)

        create_user_btn.bind("<Enter>", on_enter2)
        create_user_btn.bind("<Leave>", on_leave2)


class FirstPage(tk.Frame): #create events page
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def on_enter(e):
            back_Button["image"] = gobackhover

        def on_leave(e):
            back_Button["image"] = goback

        def save_event():
            from save_events_2database import save_event

            event_name = eventname.get()
            event_date = str(spinbox_date.get()) + str(spinbox_month.get()) + str(spinbox_year.get())
            event_location = eventlocation.get()
            event_venue = eventvenue.get()
            event_niche = eventniche.get()

            message=save_event(event_name,event_date,event_location,event_venue,event_niche,"N/A","N/A")
            confirmation.config(text=message)

            if message!="Saved":
                confirmation.place(x=740,y=390)




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





        label_colour_bg = "#e0e0e0"
        label_colour_fg = "black"
        entrybox_colour_bg = "#f7fefe"

        mainframe = tk.Frame(self, bg="#9eadb9")
        mainframe.pack(fill=BOTH, expand=True)

        create_BG = ImageTk.PhotoImage(Image.open('final_event/images/create event.png'))
        goback = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button.png').resize((40, 40)))
        gobackhover = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button hover.png').resize((40, 40)))
        saveicon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/save.png'))

        createBG=tk.Label(mainframe,image=create_BG,bg='#9eadb9')
        createBG.image=create_BG
        createBG.place(x=0,y=0)

        back_Button = tk.Button(mainframe, image=goback,bg="#7c8d9a",borderwidth=0, command=lambda: controller.show_frame(MainPage))
        back_Button.image=goback
        back_Button.place(x=70, y=55)

        save_Button = tk.Button(mainframe, image=saveicon, bg=label_colour_bg, borderwidth=0,command=save_event)
        save_Button.image = saveicon
        save_Button.place(x=800, y=340)

        eventname=tk.Entry(mainframe,bg=entrybox_colour_bg,width=40,borderwidth=0,fg='grey')
        eventname.insert(0, "Enter event name here")
        eventname.place(x=437,y=158)

        eventvenue = tk.Entry(mainframe, bg=entrybox_colour_bg, width=40, borderwidth=0,fg='grey')
        eventvenue.insert(0, "Enter event venue here")
        eventvenue.place(x=437, y=253)

        eventniche = tk.Entry(mainframe, bg=entrybox_colour_bg, width=40, borderwidth=0, fg='grey')
        eventniche.insert(0, "Enter event niche here")
        eventniche.place(x=437, y=348)

        eventlocation = tk.Entry(mainframe, bg=entrybox_colour_bg, width=40, borderwidth=0, fg='grey')
        eventlocation.insert(0, "Enter event location here")
        eventlocation.place(x=745, y=253)

        event_name_label = tk.Label(mainframe, text='',bg=label_colour_bg,fg=label_colour_fg)
        event_name_label.place(x=444,y=120)

        event_venue_label = tk.Label(mainframe, text='',bg=label_colour_bg,fg=label_colour_fg)
        event_venue_label.place(x=444, y=215)

        event_niche_label = tk.Label(mainframe, text='', bg=label_colour_bg, fg=label_colour_fg)
        event_niche_label.place(x=444, y=310)

        event_location_label = tk.Label(mainframe, text='', bg=label_colour_bg, fg=label_colour_fg)
        event_location_label.place(x=750, y=215)

        event_date = tk.Label(mainframe, text='set_date', bg=label_colour_bg, fg=label_colour_fg)
        event_date.place(x=843, y=118)

        year = tk.StringVar()
        month = tk.StringVar()
        date = tk.StringVar()

        spinbox_year = tk.Spinbox(mainframe, from_=2023, to=2033, textvariable=year,bg=entrybox_colour_bg, width=6,borderwidth=0)
        spinbox_year.place(x=755,y=157)

        spinbox_month = tk.Spinbox(mainframe, from_=1, to=12, textvariable=month, bg=entrybox_colour_bg, width=6, borderwidth=0)
        spinbox_month.place(x=847, y=157)


        spinbox_date = tk.Spinbox(mainframe, from_=1, to=31, textvariable=date, bg=entrybox_colour_bg, width=6, borderwidth=0)
        spinbox_date.place(x=930, y=157)

        confirmation=tk.Label(mainframe,text="", bg=label_colour_bg, fg=label_colour_fg)
        confirmation.place(x=860,y=390)









        eventname.bind('<FocusIn>', lambda event: on_entry_click(event, eventname,"Enter event name here",event_name_label,"-event_name-"))
        eventname.bind('<FocusOut>', lambda event: on_focusout(event, eventname,"Enter event name here",event_name_label,"-event_name-"))

        eventvenue.bind('<FocusIn>', lambda event: on_entry_click(event, eventvenue,"Enter event venue here",event_venue_label,"-event_venue-"))
        eventvenue.bind('<FocusOut>', lambda event: on_focusout(event, eventvenue,"Enter event venue here",event_venue_label,"-event_venue-"))

        eventniche.bind('<FocusIn>', lambda event: on_entry_click(event, eventniche, "Enter event niche here", event_niche_label,"-event_niche-"))
        eventniche.bind('<FocusOut>',
                        lambda event: on_focusout(event, eventniche ,"Enter event niche here", event_niche_label,
                                                  "-event_niche-"))
        eventlocation.bind('<FocusIn>',
                        lambda event: on_entry_click(event, eventlocation, "Enter event location here", event_location_label,
                                                     "-event_location-"))
        eventlocation.bind('<FocusOut>',
                        lambda event: on_focusout(event, eventlocation, "Enter event location here", event_location_label,
                                                  "-event_location-"))




        back_Button.bind("<Enter>", on_enter)
        back_Button.bind("<Leave>", on_leave)






class SecondPage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        from save_events_2database import return_event_names


        def refresh_combobox():
            self.values = [tup[0] for tup in return_event_names()]
            self.combo['values'] = self.values



        def proceed(self,button):
            selected=self.combo.get()
            index = self.values.index(selected)
            element_to_move = self.values.pop(index)
            self.values.insert(0, element_to_move)
            # print(self.values)

            if button=="manage":
                if User.privilege=="coordinator":
                    messagebox.showerror("Access Denied!","You dont have required permission to access this page")
                else:
                    controller.show_frame(ManagePage)

            elif button=="run":
                controller.show_frame(RunPage)

        def back_button():
            if User.privilege=="coordinator":
                messagebox.showerror("Access Denied!", "You dont have required permission to access this page")
            else:
                controller.show_frame(MainPage)



        def on_enter(e):
            back_Button["image"] = gobackhover

        def on_leave(e):
            back_Button["image"] = goback

        refreshIcon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/refresh button.png').resize((20, 20)))
        goback = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button.png').resize((40, 40)))
        gobackhover = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button hover.png').resize((40, 40)))






        mainframe = tk.Frame(self, bg="#9eadb9")
        mainframe.pack(fill=BOTH, expand=True)

        manage_BG = ImageTk.PhotoImage(Image.open('final_event/images/manage event.png'))

        manageBG = tk.Label(mainframe, image=manage_BG, bg='#9eadb9')
        manageBG.image = manage_BG
        manageBG.place(x=0, y=0)

        self.combo_value=tk.StringVar()

        self.values=[tup[0] for tup in return_event_names()]



        self.combo = ttk.Combobox(mainframe, textvariable=self.combo_value,width=60)
        self.combo['values'] = self.values
        self.combo.current(0)
        self.combo.place(x=520,y=267)






        back_Button = tk.Button(mainframe, image=goback, bg="#7b8c9a", borderwidth=0,
                                command=lambda: back_button())
        back_Button.image = goback
        back_Button.place(x=70, y=55)

        refresh_Button = tk.Button(mainframe, image=refreshIcon, borderwidth=0,
                                command=refresh_combobox)
        refresh_Button.image = refreshIcon
        refresh_Button.place(x=910, y=265)

        manageicon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/manage.png'))
        runicon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/run.png'))
        logouticon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/logout.png').resize((80, 22)))

        # refresh=tk.Button(mainframe,text="refresh",command=refresh_combobox)
        # refresh.place(x=200,y=100)

        manage_Button = tk.Button(mainframe, image=manageicon, bg="#e0e0e0", borderwidth=0, command=lambda:proceed(self,"manage") )
        manage_Button.image = manageicon
        manage_Button.place(x=530, y=350)

        run_Button = tk.Button(mainframe, image=runicon, bg="#e0e0e0", borderwidth=0,command=lambda:proceed(self,"run"))
        run_Button.image = runicon
        run_Button.place(x=730, y=350)

        refresh_combobox()

        logout=tk.Button(mainframe,image=logouticon,borderwidth=0,bg="#9eadb9",command=lambda:controller.show_frame(LoginPage))
        logout.image=logouticon
        logout.place(x=65,y=5)


        back_Button.bind("<Enter>", on_enter)
        back_Button.bind("<Leave>", on_leave)

class ManagePage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        def back_button():
            theeventname.config(text="")
            controller.show_frame(SecondPage)
            for frame in contentframe.winfo_children():
                frame.destroy()



        def run():
            from event_class import load_event

            print(second_page.combo_value.get())
            theeventname.config(text=second_page.combo_value.get())
            currentuser.config(text=User.privilege)
            loaded_event = load_event(second_page.combo_value.get())
            return loaded_event






        def home_window(self,contentframe):
            pass

        def registration_window(self,contentframe):

            def submit_registration(current_event):
                # # Directory name to check for
                dir_name = "db/specifics"
                # Check if the directory exists
                if not os.path.exists(dir_name):
                    # If it doesn't exist, create it
                    os.makedirs(dir_name)

                db_path=dir_name+f"/{current_event.name}.db"


                getFirstName = firstNameEntry.get()
                getSecondName = secondNameEntry.get()
                getAge = ageEntry.get()
                getSex = var.get()
                getPhone = yourPhoneEntry.get()
                getEmergency = emailEntry.get()
                getIdNumber = idNumberEntry.get()

                emptyfield=None

                if not getFirstName:
                    emptyfield="this"
                if not getSecondName:
                    emptyfield="this"
                if not getAge:
                    emptyfield="this"
                if not getSex:
                    emptyfield="this"
                if not getPhone:
                    emptyfield="this"
                if not getEmergency:
                    emptyfield="this"
                if not getIdNumber:
                    emptyfield="this"
                if emptyfield!=None:
                    messagebox.showwarning("Empty Field", "Fill all the fields")
                    return

                conn = sqlite3.connect(db_path)
                with conn:
                    cursor = conn.cursor()
                cursor.execute(
                    'CREATE TABLE IF NOT EXISTS attendingGuests (idNumber TEXT,Firstname TEXT,Secondname TEXT,Age INT,Gender TEXT,Phonenumber TEXT,Emergencynumber TEXT)')
                cursor.execute(
                    'INSERT INTO attendingGuests (idNumber,Firstname,Secondname ,Age,Gender,Phonenumber,Emergencynumber) VALUES(?,?,?,?,?,?,?)',
                    (getIdNumber, getFirstName, getSecondName, getAge, getSex, getPhone, getEmergency,))
                conn.commit()
                cursor.close()
                status.config(text="Submitted Successfully")
#######################################################################################################################
            ######    add a label to show saved successfully ----not yet done  ##############

            current_event = run()


            reg_girl_img = ImageTk.PhotoImage(Image.open('final_event/images/registration girl.png'))

            reg_girl_label= tk.Label(contentframe,image=reg_girl_img)
            reg_girl_label.image=reg_girl_img
            reg_girl_label.place(x=0,y=0)


            # registration window
            firstName = tk.Label(contentframe, text="First Name")
            secondName = tk.Label(contentframe, text="Second Name")
            gender = tk.Label(contentframe, text="Gender")
            idNumber = tk.Label(contentframe, text="Id Number")
            age = tk.Label(contentframe, text="Age")
            yourPhone = tk.Label(contentframe, text="Your Phone Number")
            email = tk.Label(contentframe, text="Email Address")

            firstName.place(x=370, y=20)
            secondName.place(x=550, y=20)
            gender.place(x=500, y=80)
            idNumber.place(x=370, y=160)
            age.place(x=570, y=160)
            yourPhone.place(x=370, y=220)
            email.place(x=370, y=280)

            # entry
            # global firstNameEntry, secondNameEntry, ageEntry, sexEntry, yourPhoneEntry, emergencyPhoneEntry
            firstNameEntry = tk.Entry(contentframe, highlightthickness=0, relief=FLAT)
            secondNameEntry = tk.Entry(contentframe, highlightthickness=0, relief=FLAT)
            idNumberEntry = tk.Entry(contentframe, highlightthickness=0, relief=FLAT, width=12)
            ageEntry = tk.Entry(contentframe, width=5, highlightthickness=0)
            yourPhoneEntry = tk.Entry(contentframe, highlightthickness=0, width=30)
            emailEntry = tk.Entry(contentframe, highlightthickness=0, width=35)
            # radio button for gender
            var = StringVar()
            male_rad = tk.Radiobutton(contentframe, text="Male", padx=5, variable=var, value="male")
            female_rad = tk.Radiobutton(contentframe, text="Female", padx=20, variable=var, value="female")

            male_rad.place(x=460, y=100)
            female_rad.place(x=520, y=100)

            # placing entries
            firstNameEntry.place(x=370, y=40)
            secondNameEntry.place(x=550, y=40)
            idNumberEntry.place(x=450, y=160)
            ageEntry.place(x=620, y=160)
            yourPhoneEntry.place(x=490, y=220)
            emailEntry.place(x=462, y=280)

            # submit button
            submitbtn = tk.Button(contentframe, text="Submit Form", width=30,command=lambda:submit_registration(current_event),height=2)
            submitbtn.place(x=400, y=320)

            # initialize camera button
            takepicturebtn = tk.Button(contentframe, text="Take Picture", width=30, height=2)
            takepicturebtn.place(x=400, y=380)

            status=tk.Label(contentframe,text='',font=('Times New Roman', 8))
            status.place(x=450,y=361)




        def checklist_window(self,contentframe):
            current_event = run()
            from custom_checklist import create_widget

            widget_list = []

            # Open the CSV file and read the data
            with open('widget_data.csv') as f:
                reader = csv.reader(f)
                # Skip the header row
                next(reader)
                # Loop over the rows and create the widgets
                for row in reader:
                    widget_type, message, checked = row
                    print(widget_type + checked)
                    checked = str(checked)
                    if widget_type == 'text':
                        create_widget(contentframe, 'text', message, checked)

                    elif widget_type == 'checkbox':
                        widget = create_widget(contentframe, 'checkbox', message, checked)
                        widget_list.append(widget)

        def generate_tickets(self, contentframe):
            current_event = run()

            def validate_entry(text):       ###function ensures entrybox can only receive numeric key presses
                if text.isdigit():
                    return True
                elif text == "":
                    return True
                else:
                    return False



            def start_engine():             ### function for my generate button that generates event tickets
                if totalTicketsEntry.get()=="":
                    messagebox.showwarning("Empty Field", "Fill the Total Tickets field")
                    return
                if totalTicketsEntry.get().isdigit():
                    last_ticket=int(len(firstTicketEntry.get())*("9"))
                    difference=(last_ticket-int(firstTicketEntry.get()))

                    print(difference)



                    if int(totalTicketsEntry.get()) > difference:
                        messagebox.showwarning(f"Input Error", f"Total tickets available are {difference} tickets!\nIncrease the size of your starting ticket.")
                        return

                    else:
                        confirmation_postupdates=post_updates(current_event.name, totalTicketsEntry.get(), firstTicketEntry.get())
                        print(confirmation_postupdates+" saving event details")
                        ticket_tracking(current_event.name,totalTicketsEntry.get(),firstTicketEntry.get())
                        encrypt_ticket_number(generate_ticketNumber(current_event.name, current_event.date, totalTicketsEntry.get(),firstTicketEntry.get()), current_event.name)

                        return
                messagebox.showwarning("Input Error", "Only use whole numbers for Total Tickets")


            ticketing_boy_img = ImageTk.PhotoImage(Image.open('final_event/images/ticketing boy.png'))
            generate_tickets_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/generate tickets.png').resize((185,45)))

            reg_girl_label = tk.Label(contentframe, image=ticketing_boy_img)
            reg_girl_label.image = ticketing_boy_img
            reg_girl_label.place(x=0, y=0)

            eventName = tk.Label(contentframe, text="Event Name")
            firstTicket = tk.Label(contentframe, text="First Ticket Number")
            matickets = tk.Label(contentframe, text="Total Tickets")

            vcmd = (contentframe.register(validate_entry), '%P')


            eventNameEntry = tk.Entry(contentframe, highlightthickness=0, relief=FLAT,disabledbackground="white")
            eventNameEntry.insert(0,str(current_event.name))
            eventNameEntry.config(state="disabled")
            firstTicketEntry = tk.Entry(contentframe, highlightthickness=0, relief=FLAT, validate="key", validatecommand=vcmd)
            totalTicketsEntry = tk.Entry(contentframe, highlightthickness=0, relief=FLAT, width=12, validate="key", validatecommand=vcmd)


            eventName.place(x=370, y=60)
            firstTicket.place(x=550, y=60)
            matickets.place(x=490, y=120)

            eventNameEntry.place(x=370, y=80)
            firstTicketEntry.place(x=550, y=80)
            totalTicketsEntry.place(x=490, y=150)


            generate=tk.Button(contentframe,image=generate_tickets_icon,borderwidth=0,command=start_engine)
            generate.image=generate_tickets_icon
            generate.place(x=430,y=200)


        def hide_indicators():
            register_guests_button["image"] = register_guests_icon
            checklist_button["image"] = checklists_icon
            home_button["image"] = home_icon
            tickets_button['image']=ticketing_icon



        def delete_page():
            for frame in contentframe.winfo_children():
                frame.destroy()

        def indicate(button_pressed, button, page):
            hide_indicators()
            button_pressed["image"] = button
            delete_page()
            page(self,contentframe)




        mainframe = tk.Frame(self, bg="#9eadb9")
        mainframe.pack(fill=BOTH, expand=True)

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
        register_guests_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/register guests.png').resize((148, 35)))
        ticketing_icon = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/ticketing.png').resize((148, 35)))
        checklists_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/checklist.png').resize((148, 35)))

        user_settings_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/user settings.png').resize((36,36)))

        home_icon_select = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/home select.png').resize((148, 35)))
        register_guests_icon_select = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/register guests select.png').resize((148, 35)))
        ticketing_icon_select = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/ticketing select.png').resize((148, 35)))
        checklists_icon_select = ImageTk.PhotoImage(Image.open('final_event/images/buttons/checklist select.png').resize((148, 35)))

        user_settings_icon = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/user settings.png').resize((36, 36)))


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

        register_guests_button = tk.Button(buttonsframe, image= register_guests_icon, bg="#7b8c9a", borderwidth=0,command=lambda: indicate(register_guests_button,register_guests_icon_select,registration_window))
        register_guests_button.image = register_guests_icon
        register_guests_button.pack(pady=10)

        tickets_button = tk.Button(buttonsframe, image=ticketing_icon,bg="#7b8c9a", borderwidth=0,command=lambda: indicate(tickets_button, ticketing_icon_select, generate_tickets))
        tickets_button.image = ticketing_icon
        tickets_button.pack(pady=10)

        checklist_button = tk.Button(buttonsframe, image=checklists_icon, bg="#7b8c9a", borderwidth=0,command=lambda: indicate(checklist_button,checklists_icon_select,checklist_window))
        checklist_button.image = checklists_icon
        checklist_button.pack(pady=10)



        currentuser = tk.Label(mainframe, text=User.username,bg="#f7ffff")
        currentuser.place(x=860, y=80)



        user_settings=tk.Button(mainframe,image=user_settings_icon,bg="#f7ffff",borderwidth=0)
        user_settings.image=user_settings_icon
        user_settings.place(x=935,y=70)

        second_page = controller.frames.get("Library")
        print(second_page.combo_value.get())
        theeventname = tk.Label(self, text=second_page.combo_value.get(),bg="#e0e0e0")
        theeventname.place(x=365, y=93)
        theeventname.config(text="")


        but = tk.Button(self, text='Load Current Event', command=run)
        but.place(x=550, y=70)

        logouticon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/logout.png').resize((80, 22)))
        logout = tk.Button(mainframe, image=logouticon, borderwidth=0, bg="#9eadb9",
                           command=lambda: controller.show_frame(LoginPage))
        logout.image = logouticon
        logout.place(x=65, y=5)
















class RunPage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):  # try ", *args, **kwargs"
        tk.Frame.__init__(self, parent, *args, **kwargs)



        """               functions                     """

        def back_button():
            theeventname.config(text="")
            controller.show_frame(SecondPage)
            for frame in contentframe.winfo_children():
                frame.destroy()



        def run():
            from event_class import load_event

            print(second_page.combo_value.get())
            theeventname.config(text=second_page.combo_value.get())
            currentuser.config(text=User.privilege)
            loaded_event = load_event(second_page.combo_value.get())
            return loaded_event

        def face_checkin(self,contentframe):
            current_event = run()

            start_checkin_img = ImageTk.PhotoImage(Image.open('final_event/images/start checkin.png'))
            start_checkin_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/start checkin.png').resize((100,100)))

            start_checkin=tk.Label(contentframe,image=start_checkin_img,borderwidth=0)
            start_checkin.image=start_checkin_img
            start_checkin.place(x=30,y=120)

            start_btn=tk.Button(contentframe,image=start_checkin_icon,borderwidth=0,command=lambda:checkin(current_event.name,User.username,User.gate))
            start_btn.image=start_checkin_icon
            start_btn.place(x=290,y=20)

            startlabel=tk.Label(contentframe,text="start check-in")
            startlabel.place(x=300,y=122)


        def ticketing(self,contentframe):
            current_event = run()

            start_ticket_img = ImageTk.PhotoImage(Image.open('final_event/images/ticket validation page.png'))
            start_checkin_icon = ImageTk.PhotoImage(
                Image.open('final_event/images/buttons/start checkin.png').resize((100, 100)))
            datetocheck = current_event.date[:-4]


            start_btn = tk.Button(contentframe, image=start_checkin_icon, borderwidth=0,
                                  command=lambda:check_ticket_if_valid_fr(current_event.name, datetocheck,User.username,User.gate))
            start_btn.image = start_checkin_icon
            start_btn.place(x=290, y=20)


            bg_img=tk.Label(contentframe,image=start_ticket_img,borderwidth=0)
            bg_img.image=start_ticket_img
            bg_img.place(x=130, y=140)

            startlabel = tk.Label(contentframe, text="start ticket validation")
            startlabel.place(x=300, y=122)



            pass
        def splitguests(self,contentframe):
            current_event = run()
            pass
        def lostitems(self,contentframe):
            current_event = run()
            pass
        def eventstats(self,contentframe):
            current_event = run()
            pass

        def hide_indicators():
            facerecog_button["image"] = facerecog_icon
            ticketing_button["image"] = ticketing_icon
            split_button["image"] = split_icon
            lostitems_button["image"] = lostitems_icon
            eventstats_button["image"] = eventstats_icon




        def delete_page():
            for frame in contentframe.winfo_children():
                frame.destroy()

        def indicate(button_pressed, button, page):
            hide_indicators()
            button_pressed["image"] = button
            delete_page()
            page(self,contentframe)

        def on_entry_click(event, entry,entrybox_content,label,text):
            if entry.get() == entrybox_content:
                entry.delete(0, "end")
                entry.insert(0, '')
                entry.config(fg='black')
                label.config(text=text)


        def on_focusout(event, entry,entrybox_content,label,text):
            if entry.get() == '':
                entry.insert(0, entrybox_content)
                entry.config(fg='grey')
                label.config(text='')
            else:
                label.config(text=text)



                     #####    variables  ########
        label_colour_bg = "#e0e0e0"
        label_colour_fg = "black"
        entrybox_colour_bg = "#f7fefe"


                     #####    import pics  ########
        manage_BG = ImageTk.PhotoImage(Image.open('final_event/images/run dashboard.png'))
        ticketing_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/ticketing.png').resize((148, 35)))
        split_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/split.png').resize((148, 35)))
        facerecog_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/face recog.png').resize((148, 35)))
        lostitems_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/lost items.png').resize((148, 35)))
        eventstats_icon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/stats.png').resize((148, 35)))

        #select icon display
        ticketing_icon_select = ImageTk.PhotoImage(Image.open('final_event/images/buttons/ticketing select.png').resize((148, 35)))
        split_icon_select = ImageTk.PhotoImage(Image.open('final_event/images/buttons/split select.png').resize((148, 35)))
        facerecog_icon_select = ImageTk.PhotoImage(Image.open('final_event/images/buttons/face recog select.png').resize((148, 35)))
        lostitems_icon_select = ImageTk.PhotoImage(Image.open('final_event/images/buttons/lost items select.png').resize((148, 35)))
        eventstats_icon_select = ImageTk.PhotoImage(Image.open('final_event/images/buttons/stats select.png').resize((148, 35)))

        user_settings_icon = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/user settings.png').resize((36, 36)))

        """             #####    widgets  ########                   """
        mainframe = tk.Frame(self, bg="#9eadb9")
        mainframe.pack(fill=BOTH, expand=True)



        manageBG = tk.Label(mainframe, image=manage_BG, bg='#9eadb9')
        manageBG.image = manage_BG
        manageBG.place(x=0, y=0)

        goback = ImageTk.PhotoImage(Image.open('final_event/images/buttons/back button.png').resize((40, 40)))
        gobackhover = ImageTk.PhotoImage(
            Image.open('final_event/images/buttons/back button hover.png').resize((40, 40)))

        back_Button = tk.Button(mainframe, image=goback, bg="#7b8c9a", borderwidth=0,
                                command=back_button)
        back_Button.image = goback
        back_Button.place(x=70, y=55)

        buttonsframe =tk.Frame(mainframe,height=380,width=160,bg="#7b8c9a")
        buttonsframe.place(x=78,y=180)

        facerecog_button = tk.Button(buttonsframe, image=facerecog_icon, bg="#7b8c9a", borderwidth=0,command=lambda: indicate(facerecog_button,facerecog_icon_select,face_checkin))
        facerecog_button.image = facerecog_icon
        facerecog_button.pack(pady=10)

        ticketing_button = tk.Button(buttonsframe, image=ticketing_icon, bg="#7b8c9a", borderwidth=0,command=lambda: indicate(ticketing_button,ticketing_icon_select,ticketing))
        ticketing_button.image = ticketing_icon
        ticketing_button.pack(pady=10)

        split_button = tk.Button(buttonsframe, image=split_icon, bg="#7b8c9a", borderwidth=0,command=lambda: indicate(split_button,split_icon_select,splitguests))
        split_button.image = split_icon
        split_button.pack(pady=10)

        lostitems_button = tk.Button(buttonsframe, image=lostitems_icon, bg="#7b8c9a", borderwidth=0,command=lambda: indicate(lostitems_button,lostitems_icon_select,lostitems))
        lostitems_button.image = lostitems_icon
        lostitems_button.pack(pady=10)

        eventstats_button = tk.Button(buttonsframe, image=eventstats_icon, bg="#7b8c9a", borderwidth=0,command=lambda: indicate(eventstats_button,eventstats_icon_select,eventstats))
        eventstats_button.image = eventstats_icon
        eventstats_button.pack(pady=10)

        contentframe = tk.Frame(mainframe, height=420, width=725)
        contentframe.place(x=282, y=140)


        currentuser = tk.Label(mainframe, text=User.username, bg="#f7ffff")
        currentuser.place(x=860, y=80)

        user_settings = tk.Button(mainframe, image=user_settings_icon, bg="#f7ffff", borderwidth=0, command=lambda: controller.show_frame(CreateUser))
        user_settings.image = user_settings_icon
        user_settings.place(x=935, y=70)

        second_page = controller.frames.get("Library")
        theeventname = tk.Label(self, text=second_page.combo_value.get(), bg="#e0e0e0")
        theeventname.place(x=365, y=93)
        theeventname.config(text="")

        but = tk.Button(self, text='Load Current Event', command=run)
        but.place(x=550, y=70)

        logouticon = ImageTk.PhotoImage(Image.open('final_event/images/buttons/logout.png').resize((80, 22)))
        logout = tk.Button(mainframe, image=logouticon, borderwidth=0, bg="#9eadb9",
                           command=lambda: controller.show_frame(LoginPage))
        logout.image = logouticon
        logout.place(x=65, y=5)

        current_event = run()










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
        for F in (CreateUser,LoginPage,MainPage,FirstPage, SecondPage, ManagePage ,RunPage):
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
