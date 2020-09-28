from app import db

"""
    Models
"""

classroom_student_link = db.Table('classroom_student_link',
        db.Column('student_id', db.Integer, db.ForeignKey('student.student_id')),
        db.Column('classroom_id', db.Integer, db.ForeignKey('classroom.classroom_id'))
        )

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    classes = db.relationship('Classroom',
            secondary=classroom_student_link,
            backref=db.backref('students', lazy='dynamic')
            )

    def __repr__(self):
        return f"Student('{self.student_id}', '{self.first_name} {self.last_name}')"

class Classroom(db.Model):
    classroom_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))

    def __repr__(self):
        return f"Classroom('{self.class_id}', '{self.title}', '{self.teacher_id}')"


class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(4), nullable=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    classes = db.relationship('Classroom', backref='teacher')

    def __repr__(self):
        return f"Teacher('{self.teacher_id}', '{self.first_name} {self.last_name}')"
