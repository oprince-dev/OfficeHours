from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import Optional
from wtforms.validators import ValidationError

from app.models import Student
from app.models import Teacher

"""
    Forms
"""


class TeacherRegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
    )
    first = StringField(
        'First',
        validators=[DataRequired(), Length(min=1, max=20)],
    )
    last = StringField(
        'Last',
        validators=[DataRequired(), Length(min=1, max=30)],
    )
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField(
        'Comfirm Password',
        validators=[
            DataRequired(),
            EqualTo('password'),
        ],
    )
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_email = Teacher.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('Email already exists.')


class StudentRegisterForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
    )
    first = StringField(
        'First',
        validators=[DataRequired(), Length(min=1, max=20)],
    )
    last = StringField(
        'Last',
        validators=[DataRequired(), Length(min=1, max=30)],
    )
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField(
        'Comfirm Password',
        validators=[
            DataRequired(),
            EqualTo('password'),
        ],
    )
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_email = Student.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired('Email Required'), Email()],
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired('Password Required'),
            Length(min=3, max=20),
        ],
    )
    submit = SubmitField('Sign In')


class UploadStudentsFileForm(FlaskForm):
    file = FileField('File')


class SubmitStudentsForm(FlaskForm):
    select = BooleanField('Select')
    submit = SubmitField('Submit')


class AppendStudentForm(FlaskForm):
    select = BooleanField('Select')
    class_subject = SelectField('Subject', validators=[DataRequired()])
    class_block = SelectField(
        'Block', choices=['A', 'B', 'C'],
        validators=[DataRequired()],
    )
    submit = SubmitField('Add Student(s)')


class ManualBlockForm(FlaskForm):
    class_subject = StringField('Subject', validators=[DataRequired()])
    class_block = SelectField(
        'Block', choices=['A', 'B', 'C', 'D', 'E', 'F'],
        validators=[DataRequired()],
    )
    submit = SubmitField('Add Class')


class WeekForm(FlaskForm):
    block = SelectField('Block', validators=[DataRequired()])
    week_number = IntegerField('Week', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Add Week')


class AssignmentForm(FlaskForm):
    block = SelectField('Block', validators=[DataRequired()])
    week_number = IntegerField('Week', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[Optional()])
    end_of_week = BooleanField('End of Week', validators=[Optional()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Assignment')
