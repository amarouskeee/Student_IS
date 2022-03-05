from flask import render_template, redirect, url_for
from app import app, db
from forms import StudentForm, SubjectForm
from models import Subjects, Students


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    students = Students.query.all()  # достаю всех студентов из БД
    if form.validate_on_submit():
        student = Students(
            name=form.name.data,
            birth_date=form.birth_date.data,
            mark=form.mark.data,
            status=form.status.data
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('add_student'))

    return render_template('add_students.html', form=form, items=students)


@app.route('/add-subject', methods=['GET', 'POST'])
def add_subject():
    form = SubjectForm()
    subjects = Subjects.query.order_by(Subjects.name).all()  # SELECT * FROM subjects ORDER BY name
    if form.validate_on_submit():
        subj = Subjects(
            name=form.name.data
        )
        db.session.add(subj)
        db.session.commit()
        return redirect(url_for('add_subject'))
    return render_template('add_subject.html', form=form, items=subjects)


@app.route('/update-student/<int:id>', methods=['GET', 'POST'])  # mysite.com/update/4 <- мы обвноялем конкретный элемент из базы данных по id
def update_student(id):
    """
    Function update the student information by id.
    :param id: student id from database
    :return: html template add_student page
    """
    students = Students.query.get_or_404(id)  # если id студента не будет найден в БД, вылетит ошибка 404
    form = StudentForm()
    if form.validate_on_submit():
        student = Students(
            name=form.name.data,
            birth_date=form.birth_date.data,
            mark=form.mark.data,
            status=form.status.data
        )
        try:
            db.session.add(student)
            db.session.commit()
        except:
            return 'There was a problem updating data.'
        return redirect(url_for('add_student'))
    else:
        return render_template('update-student.html', form=form, student=students)
