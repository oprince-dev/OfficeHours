import pandas as pd
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from sqlalchemy import exc
from sqlalchemy import or_

from app import app
from app import bcrypt
from app import db
from app.forms import AppendStudentForm
from app.forms import AssignmentForm
from app.forms import LoginForm
from app.forms import ManualBlockForm
from app.forms import StudentRegisterForm
from app.forms import SubmitStudentsForm
from app.forms import TeacherRegisterForm
from app.forms import UploadStudentsFileForm
from app.forms import WeekForm
from app.models import Assignment
from app.models import Block
from app.models import Student
from app.models import Subject
from app.models import Teacher
from app.models import Week


"""
    Home
"""


@app.route('/')
@login_required
def index():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    return render_template('home.html', blocks=blocks)


"""
    Auth
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Teacher.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data,
        ):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('index'),
            )
        else:
            flash('Email and/or Password did not match.', 'danger')

    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = TeacherRegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data,
        ).decode('utf-8')
        teacher = Teacher(
            first_name=form.first.data,
            last_name=form.last.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(teacher)
        db.session.commit()
        flash(
            f'Account created. Welcome, {form.first.data} {form.last.data}!',
            'success',
        )
        return redirect(url_for('index'))

    return render_template('auth/register.html', form=form, title='Teacher')


@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = StudentRegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data,
        ).decode('utf-8')
        student = Student(
            first_name=form.last_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(student)
        db.session.commit()
        flash(
            f'Account created. Welcome, {form.first.data} {form.last.data}!',
            'success',
        )
        return redirect(url_for('register_student'))

    return render_template('auth/register.html', form=form, title='Student')


"""
    Students
"""


@app.route('/students', methods=['GET'])
@login_required
def students():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    selected_block = None

    if request.args:
        args = request.args

        if 'b' in args:
            block_id = args['b']
            selected_block = Block.query.filter_by(id=block_id).first()
            students = selected_block.students

        elif 'search' in args:
            name_query = args['search']
            students = Student.query.filter(
                or_(
                    Student.first_name.like(name_query),
                    Student.last_name.like(name_query),
                ),
            ).all()
        else:
            selected_block = None
            students = Student.query.filter(
                Student.classes.any(teacher_id=teacher.id),
            )
    else:
        blocks = teacher.blocks
        selected_block = None
        students = Student.query.filter(
            Student.classes.any(teacher_id=teacher.id),
        )

    return render_template(
        'students/students.html',
        blocks=blocks,
        students=students,
        selected_block=selected_block,
    )


@app.route('/add/student', methods=['GET', 'POST'])
@login_required
def add_student():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    subjects = Subject.query.all()
    students = Student.query.all()
    form = AppendStudentForm()
    form.class_subject.choices = [
        (subject.id, subject.title)
        for subject in subjects
    ]

    if form.validate_on_submit():
        selected = request.form.getlist('select')
        subject_id = form.class_subject.data
        block_title = form.class_block.data
        block = Block.query.filter_by(
            subject_id=subject_id, title=block_title,
        ).first()
        students = Student.query.filter(Student.id.in_(selected)).all()

        for student in students:
            block.students.append(student)
        db.session.commit()
        return redirect(url_for('students', b=block.id))

    return render_template(
        'students/add_student.html',
        blocks=blocks,
        students=students,
        form=form,
    )


@app.route('/add/student/upload', methods=['GET', 'POST'])
@login_required
def upload_students_file():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    upload_students_form = UploadStudentsFileForm()
    submit_students_form = SubmitStudentsForm()
    if request.method == 'POST':
        if upload_students_form.validate_on_submit():
            f = request.files.get('file')
            df = pd.read_excel(f)
            table_columns = df.columns.tolist()
            messages = []
            try:
                df['DOB'] = df['DOB'].dt.strftime('%m-%d-%y')
            except KeyError:
                print('no dob')
                messages = [{
                    'message': 'Column does not exist',
                    'category': 'Danger',
                }]
            file_students = df.to_dict('index')
            return jsonify(
                table_columns=table_columns,
                file_students=file_students,
                flash_messages=messages,
            )
    return render_template(
        'students/upload_student.html',
        blocks=blocks,
        upload_students_form=upload_students_form,
        submit_students_form=submit_students_form,
    )


@app.route('/add/student/submit', methods=['GET', 'POST'])
@login_required
def submit_students_file():
    submission_dict = dict(request.form.lists())
    first_names = submission_dict['First']
    last_names = submission_dict['Last']
    emails = submission_dict['Email']
    DOBS = submission_dict['DOB']
    students = zip(first_names, last_names, emails, DOBS)
    for s in students:
        student = Student(first_name=s[0], last_name=s[1], email=s[2], dob=s[3])
        db.session.add(student)
        db.session.commit()
    return redirect(url_for('classes'))


@app.route('/edit/student', methods=['GET', 'POST'])
@login_required
def edit_student():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    if request.args:
        args = request.args
        student_id = args['s']
        if 'd' in args:
            block_id = args['d']
            block = Block.query.filter_by(id=block_id).first()
            student = Student.query.filter_by(id=student_id).first()
            block.students.remove(student)
            db.session.commit()

        student = Student.query.filter_by(id=student_id).first()
    return render_template(
        'students/edit_student.html',
        blocks=blocks,
        student=student,
    )


"""
    Classes
"""


@app.route('/classes')
@login_required
def classes():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    selected_block = None

    if request.args:
        args = request.args

        if 'b' in args:
            block_id = args['b']
            selected_block = Block.query.filter_by(id=block_id).first()

    return render_template(
        'classes/classes.html',
        blocks=blocks,
        selected_block=selected_block,
    )


@app.route('/new/class', methods=['GET', 'POST'])
@login_required
def new_class():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    try:
        blocks = teacher.blocks
    except exc.SQLAlchemyError:
        pass
    manual_block_form = ManualBlockForm()

    if manual_block_form.validate_on_submit():
        subject = Subject(title=manual_block_form.class_subject.data)
        db.session.add(subject)
        db.session.commit()
        subject = Subject.query.filter_by(
            title=manual_block_form.class_subject.data,
        ).first()
        block = Block(
            subject_id=subject.id,
            teacher_id=teacher.id,
            title=manual_block_form.class_block.data,
        )
        db.session.add(block)
        db.session.commit()

        return redirect(url_for('classes'))

    return render_template(
        'classes/new_class.html',
        blocks=blocks,
        manual_block_form=manual_block_form,
    )


@app.route('/edit/class', methods=['GET', 'POST'])
@login_required
def edit_class():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    form = ManualBlockForm()

    args = request.args
    block_id = args['b']
    selected_block = Block.query.filter_by(id=block_id).first()
    students = selected_block.students

    if 'd' in args:
        student_id = args['d']
        student = Student.query.filter_by(id=student_id).first()
        selected_block.students.remove(student)
        db.session.commit()

    if form.validate_on_submit():
        selected_block.subject.title = form.class_subject.data
        selected_block.title = form.class_block.data
        db.session.commit()

        return redirect(url_for('edit_class', b=selected_block.id))

    return render_template(
        'classes/edit_class.html',
        blocks=blocks,
        selected_block=selected_block,
        students=students,
        form=form,
    )


"""
    Assignments
"""


@app.route('/assignments', methods=['GET'])
@login_required
def assignments():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    selected_block = None
    weeks = Week.query.filter(Week.block.has(teacher_id=current_user.id)).all()
    # assignments = weeks.assignments
    # assignments = None
    assignments = Assignment.query.join(Week).join(
        Block,
    ).filter(Block.teacher_id == 6).all()

    if request.args:
        args = request.args
        if 'b' in args:
            block_id = args['b']
            selected_block = Block.query.filter_by(id=block_id).first()
            # weeks = selected_block.weeks
            assignments = Assignment.query.filter(
                Assignment.week.has(block_id=selected_block.id),
            ).all()

    return render_template(
        'assignments/assignments.html',
        blocks=blocks,
        selected_block=selected_block,
        weeks=weeks,
        assignments=assignments,
    )


@app.route('/new/assignment', methods=['GET', 'POST'])
@login_required
def new_assignment():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    weeks = Week.query.filter(Week.block.has(teacher_id=current_user.id)).all()
    form = AssignmentForm()
    form.block.choices = [
        (
            block.id,
            f'{block.subject.title} {block.title}',
        ) for block in teacher.blocks
    ]

    if form.validate_on_submit():
        week = Week.query.filter_by(
            block_id=form.block.data, week_number=form.week_number.data,
        ).first()
        if form.end_of_week.data:
            due_date = week.end_date
        else:
            due_date = form.due_date.data
        assignment = Assignment(
            week_id=form.week_number.data,
            due_date=due_date,
            title=form.title.data,
            description=form.description.data,
        )

        week.assignments.append(assignment)
        db.session.commit()

        return redirect(url_for('new_assignment'))

    return render_template(
        'assignments/new_assignment.html',
        blocks=blocks,
        weeks=weeks,
        form=form,
    )


@app.route('/edit/assignment', methods=['GET', 'POST'])
@login_required
def edit_assignment():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    form = AssignmentForm()
    form.block.choices = [
        (
            block.id,
            f'{block.subject.title} {block.title}',
        ) for block in teacher.blocks
    ]

    if request.args:
        args = request.args

        if 'd' in args:
            assignment_id = args['d']
            Assignment.query.filter_by(id=assignment_id).delete()
            db.session.commit()

            return redirect(url_for('assignments'))

        if 'a' in args:
            assignment_id = args['a']
            assignment = Assignment.query.filter_by(id=assignment_id).first()
            form.block.default = assignment.week.block_id
            form.week_number.default = assignment.week.week_number
            form.process()
            form.title.data = assignment.title
            form.description.data = assignment.description

        if form.validate_on_submit():
            assignment.title = form.title.data
            assignment.description = form.description.data
            db.session.commit()

            return redirect(url_for('assignments'))

    return render_template(
        'assignments/edit_assignment.html',
        blocks=blocks,
        assignment=assignment,
        form=form,
    )


"""
    Weeks
"""


@app.route('/weeks', methods=['GET', 'POST'])
@login_required
def weeks():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    weeks = Week.query.filter(Week.block.has(teacher_id=current_user.id)).all()
    selected_block = None

    if request.args:
        args = request.args
        if 'b' in args:
            block_id = args['b']
            weeks = Week.query.filter(Week.block.has(id=block_id)).all()
            selected_block = Block.query.filter_by(id=block_id).one()

    return render_template(
        'weeks/weeks.html',
        blocks=blocks,
        weeks=weeks,
        selected_block=selected_block,
    )


@app.route('/new/week', methods=['GET', 'POST'])
@login_required
def new_week():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    form = WeekForm()
    form.block.choices = [
        (
            block.id,
            f'{block.subject.title} {block.title}',
        ) for block in teacher.blocks
    ]

    if form.validate_on_submit():
        week = Week(
            block_id=int(form.block.data),
            week_number=form.week_number.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
        )
        try:
            db.session.add(week)
            db.session.commit()
        except exc.SQLAlchemyError:
            flash(
                f'Week {form.week_number.data} for this class already exists',
                'warning',
            )

        return redirect(url_for('weeks'))

    return render_template('weeks/new_week.html', blocks=blocks, form=form)


"""
    Whiteboard
"""


@app.route('/whiteboard')
@login_required
def whiteboard():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    return render_template('whiteboard.html', blocks=blocks)


"""
    Online Room
"""


@app.route('/onlineroom')
@login_required
def onlineroom():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    return render_template('onlineroom.html', blocks=blocks)


"""
    Help Desk
"""


@app.route('/helpdesk')
@login_required
def helpdesk():
    teacher = Teacher.query.filter_by(id=current_user.id).first()
    blocks = teacher.blocks
    return render_template('helpdesk.html', blocks=blocks)


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404
