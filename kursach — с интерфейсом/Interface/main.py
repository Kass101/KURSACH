import tkinter as tk
from tkinter import ttk
from Interface.tab_student import create_student_tab
from Interface.tab_professor import create_professor_tab
from Interface.tab_class import create_class_tab
from Interface.tab_group import create_group_tab
from Interface.tab_course import create_course_tab
from Interface.tab_student_group import create_student_group_tab

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Отдел повышения квалификации")

    tab_control = ttk.Notebook(root)

    create_student_tab(tab_control)
    create_professor_tab(tab_control)
    create_class_tab(tab_control)
    create_group_tab(tab_control)
    create_course_tab(tab_control)
    create_student_group_tab(tab_control)

    tab_control.pack(expand=1, fill="both")

    root.mainloop()
