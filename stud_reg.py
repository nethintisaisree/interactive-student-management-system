import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")
FILE = "students.txt"
COURSES = ["MCA", "MBA", "MSc", "MTech"]
shown = []

class Person:
    def __init__(self, name):
        self.name = name
    def details(self):
        return self.name

class Student(Person): # inheritance
    def __init__(self, roll_no, name, course):
        super().__init__(name)
        self.roll_no = roll_no
        self.course = course
    def details(self): # polymorphism
        return f"{self.roll_no} - {self.name} - {self.course}"

def load_students():
    students = []
    try:
        with open(FILE) as file:
            for line in file:
                roll_no, name, course = line.strip().split(",")
                students.append(Student(roll_no, name, course))
    except FileNotFoundError:
        pass
    return students

def save_students(students):
    with open(FILE, "w") as file:
        for s in students:
            file.write(f"{s.roll_no},{s.name},{s.course}\n")
            
def show_students(students):
    global shown
    shown = students
    listbox.delete(0, tk.END)
    for s in students:
        listbox.insert(tk.END, s.details())

def get_input():
    roll_no = roll_entry.get().strip()
    name = name_entry.get().strip()
    if roll_no == "" or name == "":
        raise ValueError("All fields are required.")
    if not roll_no.isdigit():
        raise ValueError("Roll No must contain only numbers.")
    if not name.replace(" ", "").isalpha():
        raise ValueError("Name must contain only letters.")
    course = course_box.get()
    if course == "Select Course":
        raise ValueError("Please select a course.")
    return roll_no, name, course

def process(action):
    try:
        if action == "delete":
            roll_no = roll_entry.get().strip()
        else:
            roll_no, name, course = get_input()
        students = load_students()
        found = None
        for s in students:
            if s.roll_no == roll_no:
                found = s
        if action == "add":
            if found:
                raise ValueError("Roll No already exists.")
            students.append(Student(roll_no, name, course))
        elif found is None:
            raise ValueError("Roll No not found.")
        elif action == "update":
            found.name = name
            found.course = course
        else:
            students.remove(found)
        save_students(students)
        show_students(students)
        for entry in (roll_entry, name_entry):
            entry.delete(0, tk.END)
        course_box.set("Select Course")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

def add_student():
    process("add")
def update_student():
    process("update")
def delete_student():
    process("delete")
def search_student():
    text = search_entry.get().strip().lower()
    results = []
    for s in load_students():
        if text in s.roll_no.lower() or text in s.name.lower():
            results.append(s)
    show_students(results)
    if len(results) == 0:
        messagebox.showinfo("Search", "No records found.")

def show_all():
    show_students(load_students())
def select_student(event):
    selection = listbox.curselection()
    if selection:
        s = shown[selection[0]]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, s.name)
        roll_entry.delete(0, tk.END)
        roll_entry.insert(0, s.roll_no)
        course_box.set(s.course)

app = ctk.CTk()
app.title("Student Management System")
app.geometry("650x520")

form = ctk.CTkFrame(app)
form.pack(pady=10)
ctk.CTkLabel(form, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = ctk.CTkEntry(form, width=250)
name_entry.grid(row=0, column=1, padx=10, pady=5)
ctk.CTkLabel(form, text="Roll No").grid(row=1, column=0, padx=10, pady=5, sticky="w")
roll_entry = ctk.CTkEntry(form, width=250)
roll_entry.grid(row=1, column=1, padx=10, pady=5)
ctk.CTkLabel(form, text="Course").grid(row=2, column=0, padx=10, pady=5, sticky="w")
course_box = ctk.CTkComboBox(form, values=COURSES, width=250, state="readonly")
course_box.set("Select Course")
course_box.grid(row=2, column=1, padx=10, pady=5)

buttons = ctk.CTkFrame(app)
buttons.pack(pady=5)
ctk.CTkButton(buttons, text="Add", width=90, command=add_student).pack(side="left", padx=5, pady=5)
ctk.CTkButton(buttons, text="Update", width=90, command=update_student).pack(side="left", padx=5, pady=5)
ctk.CTkButton(buttons, text="Delete", width=90, command=delete_student).pack(side="left", padx=5, pady=5)

find = ctk.CTkFrame(app)
find.pack(pady=5)
search_entry = ctk.CTkEntry(find, width=200)
search_entry.pack(side="left", padx=5, pady=5)
ctk.CTkButton(find, text="Search", width=90, command=search_student).pack(side="left", padx=5, pady=5)
ctk.CTkButton(find, text="Show All", width=90, command=show_all).pack(side="left", padx=5, pady=5)

listbox = tk.Listbox(app, width=60, height=10, font=("Arial", 12), bg="#2b2b2b", fg="white", selectbackground="#2b2b2b", selectforeground="white", activestyle="none", exportselection=False)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", select_student)

show_all()
app.mainloop()