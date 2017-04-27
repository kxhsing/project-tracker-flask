"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def show_students_and_projects():
    """Show all students and projects"""
    student_names = hackbright.get_all_students()
    print student_names

    project_names = hackbright.get_all_projects()
    print project_names

    return render_template("homepage.html",
                            students=student_names,
                            projects=project_names)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    # import pdb; pdb.set_trace()
    grades = hackbright.get_grades_by_github(github)
    print grades
    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            grades=grades)

    
    return html

@app.route("/project")
def get_project_info():
    """Show project information on project information page"""
    
    title = request.args.get("title")
    title, description, max_grade = hackbright.get_project_by_title(title)

    students = hackbright.get_grades_by_title(title)
    print students

    
    return render_template("project_info.html",
                            title=title,
                            description=description,
                            students=students
                            )


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")



@app.route("/new-student")
def new_student():
    """Creates new student"""
    return render_template("new_student.html")

@app.route("/new-student-database", methods=['POST'])
def add_to_database():
    """add info of new student to database"""
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    github = request.form.get('github')

    hackbright.make_new_student(firstname, lastname, github)
    return render_template("new_student_response.html",
                            firstname=firstname,
                            lastname=lastname,
                            github=github)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.debug=True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0")