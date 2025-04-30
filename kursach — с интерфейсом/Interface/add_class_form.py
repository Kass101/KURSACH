import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from Interface.db_connection import connect_to_db

def get_courses_and_groups():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('SELECT g.shifr, g.id_course, c.name FROM "Group" g JOIN "Course" c ON g.id_course = c.id_course')
    groups = cursor.fetchall()
    conn.close()
    return groups

def get_professors():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id_professor, fio FROM "Professor"')
    profs = cursor.fetchall()
    conn.close()
    return profs

def validate_class_inputs(group, date, time, type_, professor_id, class_number, id_class=None):
    errors = []

    if not all([group, date, time, type_, professor_id, class_number]):
        errors.append("Пожалуйста, заполните все поля.")
        return "\n".join([f"• {err}" for err in errors])  # Остальные проверки не имеют смысла

    try:
        dt = datetime.strptime(f"{date} {time}", "%d-%m-%Y %H:%M")
    except ValueError:
        errors.append("Неверный формат даты или времени.")
        return "\n".join([f"• {err}" for err in errors])  # Остальные проверки тоже не имеют смысла

    conn = connect_to_db()
    cursor = conn.cursor()

    # Проверка конфликта по преподавателю
    cursor.execute('''
        SELECT 1 FROM "Class"
        WHERE date_time = %s AND id_professor = %s AND (%s IS NULL OR id_class != %s)
    ''', (dt, professor_id, id_class, id_class))
    if cursor.fetchone():
        errors.append("Преподаватель уже ведет занятие в это время.")

    # Проверка конфликта по группе
    cursor.execute('''
        SELECT 1 FROM "Class"
        WHERE date_time = %s AND shifr = %s AND (%s IS NULL OR id_class != %s)
    ''', (dt, group, id_class, id_class))
    if cursor.fetchone():
        errors.append("Группа уже занята в это время.")

    # Проверка конфликта по аудитории
    cursor.execute('''
        SELECT 1 FROM "Class"
        WHERE date_time = %s AND class_number = %s AND (%s IS NULL OR id_class != %s)
    ''', (dt, class_number, id_class, id_class))
    if cursor.fetchone():
        errors.append("Аудитория уже занята в это время.")

    conn.close()
    return "\n".join([f"• {err}" for err in errors]) if errors else None

def open_add_class_form(tree, update_callback):
    open_class_form(tree, update_callback, mode="add")

def open_edit_class_form(tree, update_callback, class_data):
    open_class_form(tree, update_callback, mode="edit", class_data=class_data)

def open_class_form(tree, update_callback, mode="add", class_data=None):
    win = tk.Toplevel()
    win.title("Редактировать занятие" if mode == "edit" else "Добавить занятие")
    win.geometry("400x350")
    win.resizable(False, False)

    groups = get_courses_and_groups()
    group_shifrs = [g[0] for g in groups]
    group_names = [f"{g[0]} ({g[2]})" for g in groups]

    professors = get_professors()
    prof_names = [f"{p[0]} - {p[1]}" for p in professors]

    ttk.Label(win, text="Группа:", anchor="e").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    group_cb = ttk.Combobox(win, values=group_names, state="readonly", width=30)
    group_cb.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(win, text="Дата:", anchor="e").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    date_entry = DateEntry(win, date_pattern="dd-mm-yyyy", width=30)
    date_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(win, text="Время (чч:мм):", anchor="e").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    time_entry = ttk.Entry(win, width=30)
    time_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(win, text="Тип занятия:", anchor="e").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    type_cb = ttk.Combobox(win, values=["лекция", "практика"], state="readonly", width=30)
    type_cb.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(win, text="Преподаватель:", anchor="e").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    professor_cb = ttk.Combobox(win, values=prof_names, state="readonly", width=30)
    professor_cb.grid(row=4, column=1, padx=10, pady=5)

    ttk.Label(win, text="Аудитория:", anchor="e").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    class_number_entry = ttk.Entry(win, width=30)
    class_number_entry.grid(row=5, column=1, padx=10, pady=5)

    if mode == "edit" and class_data:
        group_index = group_shifrs.index(class_data["shifr"])
        group_cb.current(group_index)

        # Обработка date_time
        date_obj = None
        try:
            if isinstance(class_data["date_time"], datetime):
                date_obj = class_data["date_time"]
            else:
                try:
                    date_obj = datetime.strptime(class_data["date_time"], "%d-%m-%Y %H:%M")
                except ValueError:
                    date_obj = datetime.strptime(class_data["date_time"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            messagebox.showerror("Ошибка", "Невозможно распознать дату.")
            return

        date_entry.set_date(date_obj.date())
        time_entry.insert(0, date_obj.strftime("%H:%M"))
        type_cb.set(class_data["type"])
        prof_index = next((i for i, p in enumerate(professors) if p[0] == class_data["id_professor"]), 0)
        professor_cb.current(prof_index)
        class_number_entry.insert(0, class_data["class_number"])

    def submit():
        group_index = group_cb.current()
        prof_index = professor_cb.current()

        if group_index == -1 or prof_index == -1:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите группу и преподавателя.")
            return

        shifr = group_shifrs[group_index]
        date = date_entry.get()
        time = time_entry.get()
        type_ = type_cb.get()
        professor_id = professors[prof_index][0]
        class_number = class_number_entry.get()

        err = validate_class_inputs(shifr, date, time, type_, professor_id, class_number,
                                    id_class=class_data["id_class"] if mode == "edit" else None)
        if err:
            messagebox.showerror("Ошибка", err)
            return

        dt = datetime.strptime(f"{date} {time}", "%d-%m-%Y %H:%M")
        conn = connect_to_db()
        cursor = conn.cursor()

        if mode == "add":
            cursor.execute(''' 
                INSERT INTO "Class"(date_time, type, shifr, id_professor, class_number)
                VALUES (%s, %s, %s, %s, %s)
            ''', (dt, type_, shifr, professor_id, class_number))
        else:
            cursor.execute(''' 
                UPDATE "Class"
                SET date_time = %s, type = %s, shifr = %s, id_professor = %s, class_number = %s
                WHERE id_class = %s
            ''', (dt, type_, shifr, professor_id, class_number, class_data["id_class"]))

        conn.commit()
        conn.close()

        messagebox.showinfo("Успех", "Занятие успешно сохранено!")
        update_callback(tree)
        win.destroy()

    ttk.Button(win, text="Сохранить", command=submit).grid(row=6, column=0, columnspan=2, pady=10)
