from student_operations import add_Student
from group_operations import add_Group
from professor_operations import add_professor
from class_operations import add_Class
from course_operations import add_Course
from add_student_to_group import add_Student_to_Group, add_Multiple_Students_to_Group

if __name__ == "__main__":
    # добавление студента
    Student_data = {
        "id_student": "25-04-2025",
        "date": "2025-04-28",
        "fio": "Петров Петр Петрович",
        "series": "1234",
        "number": "654321",
        "issued_by": "МВД России по г. Москве",
        "date_of_issue": "2020-05-20",
        "phone_number": "89995554433",
        "email": "petrov@mail.ru",
        "organisation": "ООО Альфа",
        "position": "Инженер"
    }

    # добавление студента в группу
    # data = {
    #      "id_student": "22-06-0003",
    #      "shifr": "ПО-24"
    # }

    # добавление нескольких студентов в группу
    # students = ["22-06-0019", "22-06-0005", "22-06-0009"]
    # group_shifr = "ПО-22"

    # добавление курса
    # course_data = {
    #     "id_course": "123456789012",
    #     "name": "Программирование на Python",
    #     "hours": 72
    # }

    # добавление группы
    # data = {
    #      "shifr": "ПО-22",
    #      "id_course": 1,
    #      "begin_date": "2025-09-01",
    #      "end_date": "2026-06-30"
    #  }

    # добавление препода
    # professor_data = {
    #     "id_professor": "22-062",
    #     "fio": "Иванов Андрей Иванович",
    #     "phone_number": "89001234565",
    #     "email": "ivanovA@mail.ru"
    # }

    # добавление занятия
    # class_data = {
    #     "date_time": "2025-05-05 12:00:00",
    #     "type": "лекция",
    #     "shifr": "ПО-24",
    #     "id_professor": "22-062",
    #     "class_number": "102A"
    # }

    # add_Class(class_data)

    # add_professor(professor_data)
    # add_Student_to_Group(data)
    # add_Group(data)
    # add_Course(course_data)
    add_Student(Student_data)
    # add_Multiple_Students_to_Group(students, group_shifr)