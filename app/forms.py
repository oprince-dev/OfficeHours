from app import app
from app.models import Teacher
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, TextAreaField, Form, FormField, FieldList
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from wtforms.validators import Email, EqualTo, Length

"""
    Forms
"""
class TeacherRegisterForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first = StringField('First',
                           validators=[DataRequired(), Length(min=1, max=20)])
    last = StringField('Last',
                           validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Comfirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_email = Teacher.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('Email already exists.')

class StudentRegisterForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first = StringField('First',
                           validators=[DataRequired(), Length(min=1, max=20)])
    last = StringField('Last',
                           validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Comfirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_email = Student.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('Email already exists.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired("Email Required"), Email()])
    password = PasswordField('Password', validators=[DataRequired("Password Required"), Length(min=3, max=20)])
    submit = SubmitField('Sign In')

class AppendStudentForm(FlaskForm):
    student_id = StringField('ID', validators=[DataRequired()])
    first = StringField('First', validators=[DataRequired()])
    last = StringField('Last', validators=[DataRequired()])
    class_subject = SelectField('Subject', validators=[DataRequired()])
    class_block = SelectField('Block', choices=['A', 'B', 'C'], validators=[DataRequired()])
    submit = SubmitField('Add Student')

class NewBlockForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    title = SelectField('Title', choices=["A", "B", "C", "D", "E", "F"], validators=[DataRequired()])
    submit = SubmitField('Add Class')

class NewWeekForm(FlaskForm):
    block = SelectField('Block', validators=[DataRequired()])
    week_number = IntegerField('Week', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Add Week')

class NewAssignmentForm(FlaskForm):
    block = SelectField('Block', validators=[DataRequired()])
    week_number = IntegerField('Week', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Assignment')
