from app import app, db
from app.models import  Student, Subject, Block, Teacher, student_block
from app.forms import TeacherRegisterForm, StudentRegisterForm, AddStudentForm
from flask import render_template, url_for, redirect, flash, jsonify, request
from sqlalchemy import or_


"""
    Routes
"""
@app.route("/")
def index():
    return render_template('home.html')

@app.route("/register/teacher", methods=['GET', 'POST'])
def register_teacher():
    teacherForm = TeacherRegisterForm()

    if teacherForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                teacherForm.password.data).decode('utf-8')
        teacher = Teacher(first_name=teacherForm.last_name.data,
                          last_name=teacherForm.last_name.data,
                          email=teacherForm.email.data,
                          password=hashed_password)
        db.session.add(teacher)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', form=teacherForm, title='Teacher')

@app.route("/register/student", methods=['GET', 'POST'])
def register_student():
    studentForm = StudentRegisterForm()

    if studentForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                studentForm.password.data).decode('utf-8')
        student = Student(first_name=studentForm.last_name.data,
                          last_name=studentForm.last_name.data,
                          email=studentForm.email.data,
                          password=hashed_password)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('register_student'))

    return render_template('register.html', form=studentForm, title='Student')


@app.route("/students", methods=['GET'])
def students():
    if request.args:
        args = request.args

        if "subject" in args and args["subject"] != "0":
            subject_id = args["subject"]
            if "block" in args:
                block_title = args["block"]
                block = Block.query.filter_by(subject_id=subject_id, title=block_title).first()
                students = block.students
                active = subject_id
            else:
                block = Block.query.filter_by(subject_id=subject_id).all()
                students = Student.query.all()
                active = subject_id

        elif "search" in args:
            name_query = args["search"]
            block = Block.query.all()
            students = Student.query.filter(or_(
                    Student.first_name.like(name_query),
                    Student.last_name.like(name_query)
                    )).all()
            active = 0

        else:
            block = Block.query.all()
            students = Student.query.all()
            active = 0
    else:
        block = Block.query.all()
        students = Student.query.all()
        active = 0

    subjects = Subject.query.all()

    return render_template('students.html',
                           subjects=subjects,
                           block=block,
                           students=students,
                           active=active)

@app.route("/append/student", methods=['GET', 'POST'])
def append_student():
    subjects = Subject.query.all()
    students = Student.query.all()
    addStudentform = AddStudentForm()
    addStudentform.class_subject.choices = [(subject.id, subject.title) for subject in subjects]

    if addStudentform.validate_on_submit():
        subject_id = addStudentform.class_subject.data
        subject = Subject.query.filter_by(id=subject_id).first()
        block_title = addStudentform.class_block.data
        block = Block.query.filter_by(subject_id=subject_id, title=block_title).first()
        student = Student.query.filter_by(id=addStudentform.student_id.data).first()
        block.students.append(student)
        db.session.add(block)
        db.session.commit()

    return render_template('append_student.html', students=students, form=addStudentform)

@app.route("/edit", methods=['GET', 'POST'])
def edit_student():
    if request.args:
        args = request.args
        student_id = args["s"]
        if "d" in args:
            block_id = args["d"]
            block = Block.query.filter_by(id=block_id).first()
            student = Student.query.filter_by(id=student_id).first()
            block.students.remove(student)
            db.session.commit()

        student = Student.query.filter_by(id=student_id).first()
    return render_template('edit_student.html', student=student)

@app.route("/assignments")
def assignments():
    return render_template('assignments.html')
