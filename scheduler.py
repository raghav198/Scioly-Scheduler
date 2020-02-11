from tkinter import *
from tkinter import filedialog, messagebox
import numpy as np
import kernel

datafilename = ""
schedulefilename = ""

NUM_TEAMS = 1


def datachoose():
    global datafilename, errorlbl
    tk.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                             filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if tk.filename != '':
        datafilelbl.config(text=tk.filename)
        datafilename = tk.filename


def schedulechoose():
    global schedulefilename, errorlbl
    tk.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                             filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if tk.filename != '':
        schedulefilelbl.config(text=tk.filename)
        schedulefilename = tk.filename


def schedule():
    try:
        datafile = open(datafilename, 'r')
        data = datafile.read().splitlines()
        schedulefile = open(schedulefilename, 'r')
        schedule = schedulefile.read().splitlines()

        for i in range(len(data)): data[i] = data[i].split(',')
        for i in range(len(schedule)): schedule[i] = schedule[i].split(',')

        students = []
        events = data[0]
        times = data[0]

        for i in range(1, len(events)):
            for j in range(3, len(schedule[i]) - 1):
                if schedule[i][j] != '': times[i] = j - 3

        del times[0:1]

        print(times)
        schedule = []

        for i in range(max(times)): schedule.append([])
        for i in range(len(schedule)):
            for j in range(len(events)):
                if times[j] == i:
                    schedule[i].append(1)
                else:
                    schedule[i].append(0)

        print(schedule)
        schedule = np.array(schedule)

        print(schedule)

        for i in range(1, len(data)):
            for j in range(len(data[i])):
                try:
                    int(data[i][j])
                except:
                    if data[i][j] not in students and data[i][j] != '':
                        students.append(data[i][j])

        students = np.unique(np.array(students))

        skills = []
        for student in students: skills.append([])
        for i in range(len(skills)):
            for j in range(len(events) + 1): skills[i].append(0)

        print(len(data[0]))
        print(len(skills[0]))

        for s in range(len(students)):
            for i in range(len(data)):
                for j in range(len(data[i])):
                    # print(len(data[i]))
                    if data[i][j] == students[s]:
                        skills[s][j - 1] = i

        print(students)
        print(skills)

    except FileNotFoundError:
        fileerror()


def fileerror():
    messagebox.showerror("File Error",
                         "Ensure that the correct files have been entered and the files have the correct formats...")


tk = Tk()
tk.title("SciOly Scheduler")
tk.resizable(False, False)

Label(tk, text="Student Depth Chart: ").grid(row=1, column=0)
datafilelbl = Label(tk, text="no file selected")
datafilelbl.grid(row=1, column=1)
Button(tk, text="Choose File...", command=datachoose).grid(row=1, column=2)

Label(tk, text="Schedule File: ").grid(row=2, column=0)
schedulefilelbl = Label(tk, text="no file selected")
schedulefilelbl.grid(row=2, column=1)
Button(tk, text="Choose File...", command=schedulechoose).grid(row=2, column=2)

Button(tk, text="Schedule!", command=schedule).grid(row=3, column=1)

tk.mainloop()
