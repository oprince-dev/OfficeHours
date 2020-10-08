from app import db, login_manager
from flask_login import UserMixin

"""
    Models
"""

@login_manager.user_loader
def load_user(user_id):
    return Teacher.query.get(int(user_id))

student_block = db.Table('student_block',
        db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
        db.Column('block_id', db.Integer, db.ForeignKey('block.id'))
        )

class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(4), nullable=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    blocks = db.relationship('Block', backref=db.backref('teacher'))

    def __repr__(self):
        return f"Teacher(id='{self.id}', name='{self.first_name} {self.last_name}')"

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Student(id='{self.id}', name='{self.first_name}, {self.last_name}')"

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    blocks = db.relationship('Block', backref=db.backref('subject'))

    def __repr__(self):
        return f"Subject(id='{self.id}', title='{self.title}')"

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    title = db.Column(db.String(1))
    weeks = db.relationship('Week', backref=db.backref('block'), lazy='dynamic')
    students = db.relationship('Student',
            secondary=student_block,
            backref=db.backref('classes', lazy='dynamic')
            )

    def __repr__(self):
        return f"Block(id='{self.id}', subject_id='{self.subject_id}', teacher_id='{self.teacher_id}', title='{self.title}')"

class Week(db.Model):
    __table_args__ = (db.UniqueConstraint('block_id', 'week_number', name='_block_week_uc'),)
    id = db.Column(db.Integer, primary_key=True)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'))
    week_number = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date(), nullable=False)
    assignments = db.relationship('Assignment', backref=db.backref('week'), lazy='dynamic')

    def __repr__(self):
        return f"Week(id='{self.id}', block_id='{self.block_id}')"

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'))
    title = db.Column(db.String(30))
    description = db.Column(db.String(300))
    due_date = db.Column(db.Date(), nullable=False)


    def __repr__(self):
        return f"Asssignment(id='{self.id}', week_id='{self.week_id}')"
