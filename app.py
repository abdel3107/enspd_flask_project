from flask import Flask, render_template, request, redirect, url_for, session

from db_util import *
import re

from utils import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.before_request
def create_tables_if_needed():
    """Connects to the database and creates tables if necessary."""
    connection = connect_to_db()
    if connection:
        creat_table_query(connection, "schema.sql")  # Call with path to schema file
        close_connection(connection)


@app.route("/student_home_institutions")
def student_home_institutions():
    if session["role"] == 'student':
        institutions = get_all_institutions()
        # idTest = institutions[0].get_id()
        # print("The type of id is: ", type(idTest))
        return render_template("student_home_institutions.html", institutions=institutions)
    return render_template("index.html")


@app.route("/student_home_courses")
def student_home_courses():
    if session["role"] == 'student':
        courses = get_all_courses_student()
        return render_template("student_home_courses.html", courses=courses)
    return render_template("index.html")


@app.route("/createCours", methods=["GET", "POST"])
def createCours():
    msg = ''
    institutions = get_all_institutions()
    teacher_id = get_teacher_id(session['id'])
    is_confirmed = False
    if request.method == 'POST' and 'institution' in request.form and 'title' in request.form and 'description' in request.form:
        inst_id = request.form['institution']
        title = request.form['title']
        description = request.form['description']
        if len(description) > 240:
            msg = 'Enter a less than 240 characters description'
            return render_template("createCours.html", msg=msg, institutions=institutions)
        connection = connect_to_db()
        insert_course(connection, teacher_id, inst_id, title, description, is_confirmed)
        connection.close()
        msg = 'Bravo !'
        return redirect(url_for('dashboard_teacher'))
    return render_template("createCours.html", msg=msg, institutions=institutions)


@app.route('/student_view_institution_courses/<int:inst>')
def student_view_institution_courses(inst):
    courses = []
    inst_id = inst
    courses.extend(get_courses_by_institution(inst_id))
    # print(courses)
    return render_template("student_home_inst_courses.html", courses=courses)


@app.route('/student_view_course_content/<int:courseId>')
def student_view_course_content(courseId):
    contents = get_course_content_by_course_id(courseId)
    return render_template("student_view_course_content.html", contents=contents)


@app.route('/course_content', methods=['POST'])
def course_content():
    contents = []
    if request.method == 'POST' and 'course_id' in request.form:
        course_id = request.form['course_id']
        course = get_course_by_course_id(course_id)
        contents = get_course_content_by_course_id(course_id)
        print(contents)
        return render_template('course_content.html', course=course, contents=contents)
    else:
        return redirect(url_for('dashboard_teacher'))


@app.route('/create_course_content', methods=['POST'])
def create_course_content():
    if request.method == 'POST' and 'course_id' in request.form:
        course_id = request.form['course_id']
        course = get_course_by_course_id(course_id)
        return render_template('create_course_content.html', course=course)


@app.route('/content', methods=['POST'])
def content():
    if request.method == 'POST' and 'course_id' in request.form and 'content_type' in request.form and 'content_data' in request.form:
        course_id = request.form['course_id']
        content_type = request.form['content_type']
        content_data = request.form['content_data']
        # course = get_course_by_course_id(course_id)
        insert_course_content(course_id, content_type, content_data)
        return redirect(url_for('dashboard_teacher'))


@app.route("/createInst", methods=['GET', 'POST'])
def createInst():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'tel' in request.form and 'website' in request.form and 'country' in request.form and 'town' in request.form and 'address' in request.form:
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        website = request.form['website']
        country = request.form['country']
        town = request.form['town']
        address = request.form['address']
        user_id = session['id']
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'email invalide !'
        elif not name or not email or not tel or not website or not country or not address or not town:
            msg = 'Veuillez remplir tous les champs'
        else:
            connection = connect_to_db()
            insert_institution(connection, user_id, name, email, tel, website, country,
                               town, address)
            connection.close()
            msg = 'Bravo !'
            return redirect(url_for('dashboard_admin'))

    return render_template("createInst.html", msg=msg)


@app.route('/approveCourse', methods=['POST'])
def approve():
    if request.method == 'POST' and 'course_id' in request.form:
        course_id = request.form['course_id']
        change_course_status(course_id)
    return redirect(url_for('tousLesCoursAdmin'))


@app.route('/choose_admin')
def choose_admin():
    if 'email' in session and session['role'] == 'admin':
        return redirect(url_for('dashboard_admin'))
    else:
        return render_template(url_for('login'))


@app.route('/tousLesCoursAdmin')
def tousLesCoursAdmin():
    hasCourse = False
    response = []
    try:
        user_id = session['id']
        admin_id = get_admin_id(user_id)
        response = get_courses_by_admin(admin_id)
        if len(response) != 0:
            hasCourse = True
    except (Exception, psycopg2.Error) as error:
        print("Error : ", error)

    return render_template('tousLesCoursAdmin.html', hasCourse=hasCourse, courses=response)


@app.route('/dashboard_admin')
def dashboard_admin():
    hasInstitution = False
    response = ''
    try:
        user_id = session['id']
        admin_id = get_admin_id(user_id)
        connection = connect_to_db()
        cursor = connection.cursor()
        query = """SELECT institution_name,
                       country, town, address,
                       website, email, phone_number 
                    FROM instadmin
                    INNER JOIN institution ON instadmin.admin_id = institution.admin_id
                    WHERE instadmin.admin_id = %s                    
            """
        cursor.execute(query, (admin_id,))
        response = cursor.fetchone()
        close_connection(connection)
        print(response)
        if response:
            hasInstitution = True
    except (Exception, psycopg2.Error) as error:
        print("Error : ", error)

    return render_template('dashboard_admin.html', hasInstitution=hasInstitution, institution=response)


@app.route('/dashboard_teacher')
def dashboard_teacher():
    hasCourse = False
    response = []
    try:
        user_id = session['id']
        teacher_id = get_teacher_id(user_id)
        # institution = get_institution_by_id(inst_id)
        response = get_courses_by_teacher(teacher_id)
        if len(response) != 0:
            hasCourse = True
    except (Exception, psycopg2.Error) as error:
        print("Error : ", error)

    return render_template('dashboard_teacher.html', hasCourse=hasCourse, courses=response)


@app.route('/choose_teacher')
def choose_teacher():
    if 'email' in session and session['role'] == 'teacher':
        return render_template(url_for('teacher'))
    else:
        return render_template(url_for('login'))


@app.route('/')
# @app.route('/index')
def home():
    if 'email' in session and session['role'] == 'admin':
        return redirect(url_for('dashboard_admin'))
    elif 'email' in session and session['role'] == 'teacher':
        return render_template('home_teacher.html')
    else:
        return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'emailLogin' in request.form and 'passwordLogin' in request.form:
        email = request.form['emailLogin']
        password = request.form['passwordLogin']
        cursor = connect_to_db().cursor()
        cursor.execute("""SELECT * FROM mainuser WHERE email = %s""", (email,))
        account = cursor.fetchone()
        if account and check_password(account[4], password):
            session['loggedin'] = True
            session['firstname'] = account[2]
            session['id'] = account[0]
            session['email'] = account[3]
            session['role'] = check_role(account[0])
            msg = 'Bravo!'
            return role(role_argument=session.get("role"))
        else:
            msg = 'Incorrect username / password !'
    return render_template("login.html", msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'password' in request.form and 'email' in request.form and 'role' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        email = request.form['email']
        role = request.form['role']
        cursor = connect_to_db().cursor()
        cursor.execute('''SELECT * FROM mainuser WHERE email = %s''', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Compte existe deja!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'email invalide !'
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'Username must contain only characters and numbers !'
        elif not firstname or not lastname or not password or not email or not role:
            msg = 'Veuillez remplir tous les champs!'
        elif not password == confirmPassword:
            msg = 'Mot de passe ne correspond pas'
        else:
            hashed_password = hash_password(password)
            connection = connect_to_db()
            insert_user(connection, firstname, lastname, email, hashed_password, role)
            connection.close()
            msg = 'Bravo !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


# @app.route('/role')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('loggedin', None)
    session.pop('firstname', None)
    session.pop('id', None)
    session.pop('role', None)
    return redirect(url_for('home'))


@app.route('/admin')
def admin():
    return redirect(url_for('dashboard_admin'))
    # return render_template("home_admin.html")


@app.route('/teacher')
def teacher():
    return redirect(url_for('dashboard_teacher'))
    # return render_template("home_teacher.html")


if __name__ == '__main__':
    app.run(debug=True)
