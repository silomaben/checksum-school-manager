import sqlite3
import os
from tkinter import messagebox



def add_student(first_name,middle_name,last_name,gNameFirst,gNameLast,guardian_phone,current_class,enrolmentDay,student_gender,age):
    if not all([first_name, middle_name, last_name, gNameFirst, gNameLast, guardian_phone, current_class, enrolmentDay,
                student_gender, age]):
        messagebox.showerror("Error", "Please fill in all the fields")
        return
    # # Directory name to check for
    dir_name = "db"
    # Check if the directory exists
    if not os.path.exists(dir_name):
        # If it doesn't exist, create it
        os.makedirs(dir_name)

    db_path = dir_name + f"/students.db"

    # first_name = firstName.get()
    # middle_name = middleName.get()
    # last_name = lastName.get()
    # gNameFirst = guardianFName.get()
    # gNameLast = guardianLName.get()
    # guardian_phone = guardianPhone.get()
    # current_class = currentClass.get()
    # enrolmentDay = enrollmentDate.get()
    # student_gender = gender.get()
    # age=age.get()

    conn = sqlite3.connect(db_path)
    with conn:
        cursor = conn.cursor()

    query=f'CREATE TABLE IF NOT EXISTS {current_class} (studentID TEXT,Firstname TEXT,Middlename TEXT,Lastname TEXT,Age INT,Gender Text,GuardianFirstName TEXT,GuardianLastName TEXT,GuardianPhone TEXT,EnrollmentDate DATE)'
    cursor.execute(query,)
    query2=f'INSERT INTO {current_class} (studentID,Firstname,Middlename ,Lastname ,Age ,Gender,GuardianFirstName,GuardianLastName,GuardianPhone,EnrollmentDate ) VALUES(?,?,?,?,?,?,?,?,?,?)'
    cursor.execute(query2,
        ('studentID', first_name, middle_name,last_name,age,student_gender, gNameFirst, gNameLast, guardian_phone,enrolmentDay))
    conn.commit()
    cursor.close()
    print('done')

# add_student('ben','siloma','masikonde','stephen','leposo','0720275809','final','13-03-2023','male',21)

