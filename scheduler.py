import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox

datafilename = ""
schedulefilename = ""

def dataChoose():
    global datafilename
    tk.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    if tk.filename != '':
        datafilelbl.config(text=tk.filename)
        datafilename = tk.filename

def scheduleChoose():
    global schedulefilename
    tk.filename = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
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

        times.pop(0)
        times.pop(0)

        print(times)

        for i in range(1, len(data)):
            for j in range(len(data[i])):
                try: int(data[i][j])
                except:
                    if data[i][j] not in students and data[i][j] != '':
                        students.append(data[i][j])

        students = np.unique(np.array(students))

        sch_array = []

        for i in range(len(events)):
            pass

        skills = []
        for student in students: skills.append([])
        for i in range(len(skills)):
            for j in range(len(events) + 1): skills[i].append(0)

        print(len(data[0]))
        print(len(skills[0]))

        for s in range(len(students)):
            for i in range(len(data)):
                for j in range(len(data[i])):
                    #print(len(data[i]))
                    if data[i][j] == students[s]:
                        skills[s][j - 1] = i

        print(students)
        print(skills)

    except:
        fileError()

def fileError():
    messagebox.showerror("File Error", "File error! Ensure that the correct files have been entered and the files have the correct formats!")
    errorlbl.config(text="File Error!", fg="red")

tk = Tk()

tk.resizable(False, False)

Label(tk, text="Student Depth Chart: ").grid(row=1, column=0)
datafilelbl = Label(tk, text="no file selected")
datafilelbl.grid(row=1, column=1)
Button(tk, text="Choose File...", command=dataChoose).grid(row=1, column=2)

Label(tk, text="Schedule File: ").grid(row=2, column=0)
schedulefilelbl = Label(tk, text="no file selected")
schedulefilelbl.grid(row=2, column=1)
Button(tk, text="Choose File...", command=scheduleChoose).grid(row=2, column=2)

Button(tk, text="Schedule!", command=schedule).grid(row=3, column=1)

errorlbl = Label(tk, text="", fg="white")
errorlbl.grid(row=4, column=1)

tk.mainloop()
