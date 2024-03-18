from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    group_id = Column('group_id', ForeignKey(Group.id, ondelete='CASCADE'))
    group = relationship('Group', backref='students')


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey(Teacher.id, ondelete='CASCADE'))
    teacher = relationship('Teacher', backref='subjects')


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    grade_date = Column('grade_date', Date, nullable=True)
    student_id = Column('student_id', ForeignKey(Student.id, ondelete='CASCADE'))
    subject_id = Column('subject_id', ForeignKey(Subject.id, ondelete='CASCADE'))
    student = relationship('Student', backref='grade')
    subject = relationship('Subject', backref='grade')
