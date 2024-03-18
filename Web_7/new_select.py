from sqlalchemy import func, desc, select, and_
from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
            .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


# Знайти студента із найвищим середнім балом з певного предмета.
def select_2():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
            .select_from(Grade).join(Student).filter(Grade.subject_id == 1) \
            .group_by(Student.id).order_by(desc('average_grade')).limit(1).all()
    return result


# Знайти середній бал у групах з певного предмета.
def select_3():
    result = session.query(Student.group_id, func.round(func.avg(Grade.grade), 2)) \
            .select_from(Grade).join(Student).filter(Grade.subject_id == 1) \
            .group_by(Student.group_id).order_by(Student.group_id).all()
    return result


# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')) \
            .select_from(Grade).order_by(desc('average_grade')).limit(1).all()
    return result


# Знайти які курси читає певний викладач.
def select_5():
    result = session.query(Teacher.id, Teacher.fullname, Subject.name) \
            .select_from(Subject).join(Teacher).filter(Subject.teacher_id == 2).all()
    return result


# Знайти список студентів у певній групі.
def select_6():
    result = session.query(Student.id, Student.fullname) \
            .select_from(Student).filter(Student.group_id == 1).all()
    return result


# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7():
    result = session.query(Student.fullname, Grade.grade) \
            .select_from(Student).join(Grade).filter(and_(Student.group_id == 1, Grade.subject_id == 1)).all()
    return result


# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8():
    result = session.query(Teacher.fullname, Subject.name, func.round(func.avg(Grade.grade), 2)) \
            .select_from(Teacher).join(Subject).join(Grade).filter(Teacher.id == 2) \
            .group_by(Teacher.fullname, Subject.name).all()
    return result


# Знайти список курсів, які відвідує студент.
def select_9():
    result = session.query(Subject.name)\
            .select_from(Grade).join(Subject).filter(Grade.student_id == 5)\
            .group_by(Subject.id).all()
    return result


# Список курсів, які певному студенту читає певний викладач.
def select_10():
    result = session.query(Subject.name)\
            .select_from(Grade).join(Subject)\
            .filter(and_(Grade.student_id == 1, Subject.teacher_id == 2))\
            .group_by(Subject.id).all()
    return result


# Середній бал, який певний викладач ставить певному студентові.
def select_11():
    result = session.query(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2))\
            .select_from(Grade).join(Student).join(Subject).join(Teacher)\
            .filter(and_(Grade.student_id == 1, Teacher.id == 1))\
            .group_by(Student.fullname, Teacher.fullname).all()
    return result


# Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12():
    subquery = (select(func.max(Grade.grade_date)).join(Student)\
                .filter(and_(Grade.subject_id == 1, Student.group_id == 1)))\
                .scalar_subquery()

    result = session.query(Student.id, Student.fullname, Grade.grade, Grade.grade_date)\
            .select_from(Grade) \
            .join(Student) \
            .filter(and_(Grade.subject_id == 1, Student.group_id == 1, Grade.grade_date == subquery)).all()

    return result


sel_list = [select_1(), select_2(), select_3(), select_4(),
            select_5(), select_6(), select_7(), select_8(),
            select_9(), select_10(), select_11(), select_12()
            ]


if __name__ == '__main__':
    for i in range(0, 12):
        print(f'select_{i+1} --->', sel_list[i])
