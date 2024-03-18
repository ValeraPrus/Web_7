import logging
from faker import Faker
from random import randint, choice
from sqlalchemy.exc import SQLAlchemyError

from conf.db import session
from conf.models import Grade, Teacher, Student, Group, Subject


STUDENTS = 30
GROUPS = 3
SUBJECTS = 6
TEACHERS = 3

fake = Faker('uk-Ua')
subjects = ['Математика', 'Фізика', 'Хімія', 'Біологія',
            'Історія', 'Література', 'Англійська', 'Філософія'
            ]


def insert_groups():
    for _ in range(GROUPS):
        group = Group(
            name=fake.word()
        )
        session.add(group)


def insert_students():
    groups = session.query(Group).all()
    for _ in range(STUDENTS):
        student = Student(
            fullname=fake.name(),
            group_id=choice(groups).id
        )
        session.add(student)


def insert_teachers():
    for _ in range(TEACHERS):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)


def insert_subjects():
    for _ in range(SUBJECTS):
        teachers = session.query(Teacher).all()
        subject_name = choice(subjects)
        subject = Subject(
            name=subject_name,
            teacher_id=choice(teachers).id
        )
        subjects.remove(subject_name)
        session.add(subject)


def insert_grades():
    students = session.query(Student).all()
    subjects = session.query(Subject).all()
    for student in students:
        number_of_grades = randint(10, 20)
        for _ in range(number_of_grades):
            grade = Grade(
                grade=randint(0, 100),
                grade_date=fake.date_this_decade(),
                student_id=student.id,
                subject_id=choice(subjects).id
            )
            session.add(grade)


if __name__ == '__main__':
    try:
        insert_groups()
        insert_teachers()
        session.commit()
        insert_subjects()
        insert_students()
        session.commit()
        insert_grades()
        session.commit()
    except SQLAlchemyError as e:
        logging.error(e)
        session.rollback()
    finally:
        session.close()
