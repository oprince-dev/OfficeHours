from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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

class StudentSearchForm(FlaskForm):
    search = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')

# class AddStudentForm(FlaskForm):
#     first =
