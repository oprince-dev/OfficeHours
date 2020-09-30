from app import db, login_manager
from flask_login import UserMixin

"""
    Models
"""

@login_manager.user_loader
def load_user(user_id):
    return Teacher.query.get(user_id)

student_block = db.Table('student_block',
        db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
        db.Column('block_id', db.Integer, db.ForeignKey('block.id'))
        )

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Student('{self.id}', '{self.first_name}, {self.last_name}')"

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    blocks = db.relationship('Block', backref=db.backref('subject'))

    def __repr__(self):
        return f"Subject('{self.id}', '{self.title}')"

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    title = db.Column(db.String(1))
    students = db.relationship('Student',
            secondary=student_block,
            backref=db.backref('classes', lazy='dynamic')
            )

    def __repr__(self):
        return f"Block('{self.id}', '{self.subject_id}', '{self.teacher_id}', '{self.title}')"


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(4), nullable=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    blocks = db.relationship('Block', backref=db.backref('teacher'))

    def __repr__(self):
        return f"Teacher('{self.id}', '{self.first_name} {self.last_name}')"
