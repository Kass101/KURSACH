from tkinter import Toplevel, Label, Entry, Button, StringVar, ttk, messagebox
from tkcalendar import DateEntry
from Interface.db_connection import connect_to_db
from datetime import datetime

def open_add_class_form(tree, refresh_callback):
    form = Toplevel()
    form.title("Добавить занятие")
    form.geometry("500x400")

    # Объявляем переменные
    time_var = StringVar()
    type_var = StringVar()
    group_var = StringVar()
    professor_var = StringVar()
    course_name_var = StringVar()  # Переменная для имени курса
    class_number_var = StringVar()

    # Используем grid для лейблов и полей
    Label(form, text="Дата:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    date_entry = DateEntry(form, width=18)
    date_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(form, text="Время (чч:мм):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    time_entry = Entry(form, textvariable=time_var)
    time_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(form, text="Тип занятия:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    type_combo = ttk.Combobox(form, textvariable=type_var, values=["лекция", "практика"])
    type_combo.grid(row=2, column=1, padx=5, pady=5)

    Label(form, text="Группа:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    group_combo = ttk.Combobox(form, textvariable=group_var)
    group_combo.grid(row=3, column=1, padx=5, pady=5)

    Label(form, text="Преподаватель:").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    professor_combo = ttk.Combobox(form, textvariable=professor_var)
    professor_combo.grid(row=4, column=1, padx=5, pady=5)

    Label(form, text="Название курса:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
    course_name_entry = Entry(form, textvariable=course_name_var, state="readonly")
    course_name_entry.grid(row=5, column=1, padx=5, pady=5)

    Label(form, text="Аудитория:").grid(row=6, column=0, padx=5, pady=5, sticky='e')
    class_number_entry = Entry(form, textvariable=class_number_var)
    class_number_entry.grid(row=6, column=1, padx=5, pady=5)

    # Заполняем списки групп и преподавателей
    professor_map = {}

    conn = connect_to_db()
    if conn:
        cur = conn.cursor()

        # Загружаем группы
        cur.execute('SELECT shifr FROM "Group"')
        groups = [r[0] for r in cur.fetchall()]
        group_combo["values"] = groups

        # Загружаем преподавателей
        cur.execute('SELECT id_professor, fio FROM "Professor"')
        professors = cur.fetchall()
        professor_map = {f"{i} - {f}": i for i, f in professors}
        professor_combo["values"] = list(professor_map.keys())

        conn.close()

    # Обновление названия курса при выборе группы
    def update_course_info(*args):
        shifr = group_var.get()
        conn = connect_to_db()
        if conn:
            cur = conn.cursor()

            # Получаем название курса через шифр группы
            cur.execute(''' 
                SELECT c.name 
                FROM "Group" g 
                JOIN "Course" c ON g.id_course = c.id_course 
                WHERE g.shifr = %s
            ''', (shifr,))
            res = cur.fetchone()
            if res:
                course_name_var.set(res[0])  # Обновляем название курса
            else:
                course_name_var.set("")  # Если курс не найден, очищаем

            conn.close()

    group_var.trace_add("write", update_course_info)

    def save_class():
        errors = []

        try:
            date = date_entry.get_date()
            time = time_var.get()
            full_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            errors.append("• Некорректная дата или время")

        if not type_var.get():
            errors.append("• Не выбран тип занятия")

        if not group_var.get():
            errors.append("• Не выбрана группа")

        professor_str = professor_var.get()
        professor_id = professor_map.get(professor_str)
        if not professor_id:
            errors.append("• Не выбран преподаватель")

        if not class_number_var.get():
            errors.append("• Не указана аудитория")

        # Проверка длины аудитории
        if len(class_number_var.get()) > 10:
            errors.append("• Аудитория не может превышать 10 символов")

        course_name = course_name_var.get()
        if not course_name:
            errors.append("• Не найден соответствующий курс")

        # Если есть ошибки, выводим их и прерываем выполнение
        if errors:
            messagebox.showerror("Ошибка", "\n".join(errors))
            return

        # Проверка на занятость группы, преподавателя и аудитории в указанное время
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()

            # Проверка на занятие с той же группой в это время
            cursor.execute(''' 
                SELECT 1 FROM "Class" 
                WHERE shifr = %s AND date_time = %s
            ''', (group_var.get(), full_datetime))
            if cursor.fetchone():
                errors.append("• В это время уже есть занятие для этой группы")

            # Проверка на занятие с тем же преподавателем в это время
            cursor.execute(''' 
                SELECT 1 FROM "Class" 
                WHERE id_professor = %s AND date_time = %s
            ''', (professor_id, full_datetime))
            if cursor.fetchone():
                errors.append("• В это время этот преподаватель уже занят")

            # Проверка на занятие в той же аудитории в это время
            cursor.execute(''' 
                SELECT 1 FROM "Class" 
                WHERE class_number = %s AND date_time = %s
            ''', (class_number_var.get(), full_datetime))
            if cursor.fetchone():
                errors.append("• В это время эта аудитория уже занята")

            if errors:
                messagebox.showerror("Ошибка", "\n".join(errors))
                conn.close()
                return

            # Если ошибок нет, сохраняем новое занятие
            cursor.execute(''' 
                INSERT INTO "Class" (date_time, type, shifr, id_professor, class_number)
                VALUES (%s, %s, %s, %s, %s)
            ''', (full_datetime, type_var.get(), group_var.get(), professor_id, class_number_var.get()))
            conn.commit()
            conn.close()

            # Обновляем таблицу и закрываем форму
            refresh_callback(tree)
            form.destroy()

            # Показываем сообщение об успешном добавлении
            messagebox.showinfo("Успех", "Занятие успешно добавлено")

    Button(form, text="Сохранить", command=save_class).grid(row=7, column=0, columnspan=2, pady=10)
