from app import app, db
from app.models import Classroom, Student, Teacher, classroom_student_link
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

        if "sort" in args:
            classroom_id = args["class"]
            sort_term = args["sort"]
            acceptable_query = {"id": Student.student_id,
                                "first": Student.first_name,
                                "last": Student.last_name}
            order = acceptable_query[sort_term]
            if sort_term in acceptable_query:
                if classroom_id == '0':
                    cs = Classroom.query.all()
                    students = Student.query.order_by(order).all()
                    active = 0
                else:
                    cs = Classroom.query.filter_by(
                            classroom_id=classroom_id
                            ).first()
                    students = cs.students.order_by(order)
                    active = cs.classroom_id

        elif "class" in args and args["class"] != "all":
            classroom_id = args["class"]
            cs = Classroom.query.filter_by(classroom_id=classroom_id).first()
            students = cs.students
            active = cs.classroom_id

        elif "search" in args:
            name_query = args["search"]
            cs = Classroom.query.all()
            students = Student.query.filter(or_(
                    Student.first_name.like(name_query),
                    Student.last_name.like(name_query)
                    )).all()
            active = 0

        else:
            cs = Classroom.query.all()
            students = Student.query.all()
            active = 0
    else:
        cs = Classroom.query.all()
        students = Student.query.all()
        active = 0

    classes_tabs = Classroom.query.all()

    return render_template('students.html',
                           classes_tabs=classes_tabs,
                           cs=cs,
                           students=students,
                           active=active)

@app.route("/add/student", methods=['GET', 'POST'])
def add_student():
    students = Student.query.all()
    return render_template('add_student.html', students=students)

@app.route("/assignments")
def assignments():
    return render_template('assignments.html')
