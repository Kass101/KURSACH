from tkinter import ttk, Toplevel, Label, Entry, Button, StringVar, messagebox
from tkcalendar import DateEntry
from Interface.db_connection import connect_to_db
import re


def is_shifr_unique(shifr, editing=False, original_shifr=None):
    """Проверяет, уникален ли шифр группы"""
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT shifr FROM "Group" WHERE shifr = %s', (shifr,))
        result = cursor.fetchone()
        conn.close()
        if editing and shifr == original_shifr:
            return True  # не меняли шифр — ок
        return result is None
    return False


def get_courses():
    """Получает список курсов из БД"""
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_course, name FROM "Course"')
        courses = cursor.fetchall()
        conn.close()
        return courses
    return []


def save_group(shifr, course_id, begin_date, end_date, window, refresh_callback, editing=False, original_shifr=None):
    if not re.match(r'^[А-Я]{2}-\d{2}$', shifr):
        messagebox.showerror("Ошибка", "Шифр должен быть в формате XX-00 (две заглавные русские буквы, тире и две цифры)")
        return

    if not is_shifr_unique(shifr, editing, original_shifr):
        messagebox.showerror("Ошибка", "Группа с таким шифром уже существует")
        return

    if begin_date >= end_date:
        messagebox.showerror("Ошибка", "Дата окончания должна быть позже даты начала")
        return

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        if editing:
            cursor.execute('''
                UPDATE "Group"
                SET shifr = %s, id_course = %s, begin_date = %s, end_date = %s
                WHERE shifr = %s
            ''', (shifr, course_id, begin_date, end_date, original_shifr))
        else:
            cursor.execute('''
                INSERT INTO "Group" (shifr, id_course, begin_date, end_date)
                VALUES (%s, %s, %s, %s)
            ''', (shifr, course_id, begin_date, end_date))
        conn.commit()
        conn.close()
        window.destroy()
        refresh_callback()


def open_group_form(refresh_callback, existing_data=None):
    """Открывает окно для добавления/редактирования группы"""
    window = Toplevel()
    window.title("Добавить группу" if not existing_data else "Редактировать группу")
    window.geometry("400x300")
    window.resizable(False, False)

    Label(window, text="Шифр группы:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
    shifr_var = StringVar()
    if existing_data:
        shifr_entry = Entry(window, textvariable=shifr_var, width=30, state='readonly')
    else:
        shifr_entry = Entry(window, textvariable=shifr_var, width=30)
    shifr_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(window, text="Курс:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
    courses = get_courses()
    course_names = [f"{c[0]} - {c[1]}" for c in courses]
    course_var = StringVar()
    course_dropdown = ttk.Combobox(window, textvariable=course_var, values=course_names, state="readonly", width=27)
    course_dropdown.grid(row=1, column=1, padx=10, pady=5)

    Label(window, text="Дата начала:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
    begin_date_picker = DateEntry(window, date_pattern='yyyy-mm-dd', width=28)
    begin_date_picker.grid(row=2, column=1, padx=10, pady=5)

    Label(window, text="Дата окончания:").grid(row=3, column=0, sticky='w', padx=10, pady=5)
    end_date_picker = DateEntry(window, date_pattern='yyyy-mm-dd', width=28)
    end_date_picker.grid(row=3, column=1, padx=10, pady=5)

    def on_submit():
        selected_course = course_var.get()
        if not selected_course:
            messagebox.showerror("Ошибка", "Выберите курс")
            return
        course_id = int(selected_course.split(" - ")[0])
        save_group(
            shifr_var.get().strip(),
            course_id,
            begin_date_picker.get_date(),
            end_date_picker.get_date(),
            window,
            refresh_callback,
            editing=existing_data is not None,
            original_shifr=existing_data[1] if existing_data else None
        )

    Button(window, text="Сохранить", command=on_submit).grid(row=4, column=0, columnspan=2, pady=15)

    if existing_data:
        # existing_data = (index, shifr, id_course, course_name, begin_date, end_date)
        shifr_var.set(existing_data[1])
        course_dropdown.set(f"{existing_data[2]} - {existing_data[3]}")
        begin_date_picker.set_date(existing_data[4])
        end_date_picker.set_date(existing_data[5])
