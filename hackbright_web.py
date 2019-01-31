"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def homepage():

    student_list = hackbright.get_all_students()

    project_list = hackbright.get_all_projects()

    return render_template("homepage.html",
                            student_list=student_list,
                            project_list=project_list)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    project_list = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            project_list=project_list)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/add-student-form")
def add_student_form():

    return render_template("add_student.html")

@app.route("/add-student", methods=['POST'])
def add_student():

    github = request.form.get('github')
    fname = request.form.get('fname')
    lname = request.form.get('lname')

    hackbright.make_new_student(fname, lname, github)

    return render_template("student_added.html", fname=fname, lname=lname, github=github)

@app.route("/project-info")
def show_project_info():

    title = request.args.get('title')

    project_title, description, max_grade = hackbright.get_project_by_title(title)

    student_list = hackbright.get_grades_by_title(title)

    return render_template("project.html", 
                            project_title=project_title, 
                            description=description, 
                            max_grade=max_grade,
                            student_list=student_list)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
