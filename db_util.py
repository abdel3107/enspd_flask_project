import psycopg2

from models.course import Course
from models.course_content import Content
from models.institutions import Institution
from models.teacher import Teacher


def connect_to_db():
    """Connects to the PostgreSQL database and returns a connection object."""
    try:
        connection = psycopg2.connect(
            database="EduApp",
            user="postgres",
            password="Alima",
            host="localhost",
            port="5432",  # Default PostgreSQL port
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database:", error)
        return None


def creat_table_query(connection, filename):
    """Executes SQL queries from a file and optionally fetches results."""
    cursor = connection.cursor()
    try:
        with open(filename, 'r') as file:
            schema = file.read()
        cursor.execute(schema)
        connection.commit()
        return None
    except (Exception, psycopg2.Error) as error:
        print("Error executing queries from file:", error)
        return None


def get_all_institutions():
    institutions = []
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT * FROM institution """
        cursor.execute(query)
        response = cursor.fetchall()
        for element in response:
            institution = Institution(*element)
            institutions.append(institution)
        return institutions
    except (Exception, psycopg2.Error) as error:
        print("Error geting teacher id:", error)
        return None
    finally:
        cursor.close()


# def get_institution_by_id(inst_id):
#     connection = connect_to_db()
#     cursor = connection.cursor()
#     try:
#         query = """ SELECT * FROM institution WHERE inst_id = %s"""
#         cursor.execute(query, (inst_id,))
#         response = cursor.fetchone()
#         institution = Institution(*response)
#         return institution
#     except (Exception, psycopg2.Error) as error:
#         print("Error geting institution:", error)
#         return None
#     finally:
#         cursor.close()


def execute_query(connection, query, fetch=False):
    """Executes a SQL query and optionally fetches results."""
    cursor = connection.cursor()
    cursor.execute(query)
    if fetch:
        return cursor.fetchall()
    connection.commit()
    return None


def get_admin_id(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT * FROM instadmin WHERE user_id = %s """
        cursor.execute(query, (user_id,))
        admin_id = cursor.fetchone()[0]
        return admin_id
    except (Exception, psycopg2.Error) as error:
        print("Error geting admin id:", error)
        return None
    finally:
        cursor.close()


def get_teacher_id(user_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT * FROM teacher WHERE user_id = %s """
        cursor.execute(query, (user_id,))
        teacher_id = cursor.fetchone()[0]
        return teacher_id
    except (Exception, psycopg2.Error) as error:
        print("Error geting teacher id:", error)
        return None
    finally:
        cursor.close()


def change_course_status(course_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ UPDATE course
                    SET is_confirmed = NOT is_confirmed
                    WHERE course_id = %s
                    """
        cursor.execute(query, (course_id,))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error changing status:", error)
    finally:
        cursor.close()


def get_teacher(teacher_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT teacher_id, firstname, lastname, email FROM mainuser
                    INNER JOIN teacher ON mainuser.user_id = teacher.user_id
                    WHERE teacher_id = %s """
        cursor.execute(query, (teacher_id,))
        response = cursor.fetchone()
        teacher = Teacher(*response)
        return teacher
    except (Exception, psycopg2.Error) as error:
        print("Error geting teacher id:", error)
        return None
    finally:
        cursor.close()


def get_courses_by_teacher(teacher_id):
    courses = []
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT * FROM course WHERE teacher_id = %s """
        cursor.execute(query, (teacher_id,))
        response = cursor.fetchall()
        for element in response:
            course = Course(*element)
            courses.append(course)
        return courses
    except (Exception, psycopg2.Error) as error:
        print("Error geting courses by teacher:", error)
        return None
    finally:
        cursor.close()


def get_course_by_course_id(course_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """SELECT * FROM course WHERE course_id = %s """
        cursor.execute(query, (course_id,))
        response = cursor.fetchone()
        course = Course(*response)
        return course
    except (Exception, psycopg2.Error) as error:
        print("Error getting course by course_id: ", error)
    finally:
        cursor.close()


def get_course_content_by_course_id(course_id):
    course_contents = []
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """SELECT content_id, course_id, content_type, content_data FROM content WHERE course_id = %s"""
        cursor.execute(query, (course_id,))
        response = cursor.fetchall()
        # print(response)
        for element in response:
            # print(element)
            course_content = Content(*element)
            course_contents.append(course_content)
        return course_contents
    except (Exception, psycopg2.Error) as error:
        print("Error getting courses content : ", error)
    finally:
        cursor.close()


def get_courses_by_admin(admin_id):
    courses = []
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT course_id, teacher_id, course.inst_id, title, description, is_confirmed FROM course 
                    INNER JOIN institution ON course.inst_id = institution.inst_id
                    WHERE admin_id = %s """
        cursor.execute(query, (admin_id,))
        response = cursor.fetchall()
        for element in response:
            course = Course(*element)
            courses.append(course)
        return courses
    except (Exception, psycopg2.Error) as error:
        print("Error geting courses by admin:", error)
        return None
    finally:
        cursor.close()


def get_courses_by_institution(inst_id):
    courses = []
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT course_id, teacher_id, inst_id, title, description, is_confirmed FROM course
                    WHERE (inst_id, is_confirmed) = (%s, %s) """
        cursor.execute(query, (inst_id, 'true'))
        response = cursor.fetchall()
        print("response : ", response)
        for element in response:
            course = Course(*element)
            courses.append(course)
        return courses
    except (Exception, psycopg2.Error) as error:
        print("Error geting courses by institution:", error)
        return None
    finally:
        cursor.close()

def get_all_courses_student():
    courses = []
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT course_id, teacher_id, inst_id, title, description, is_confirmed FROM course
                        WHERE is_confirmed = %s """
        cursor.execute(query, ('true',))
        response = cursor.fetchall()
        print("response : ", response)
        for element in response:
            course = Course(*element)
            courses.append(course)
        return courses
    except (Exception, psycopg2.Error) as error:
        print("Error geting all courses for student:", error)
        return None
    finally:
        cursor.close()

def insert_institution(connection, user_id, name, email, tel, website, country,
                       town, address):
    admin_id = get_admin_id(user_id)
    cursor = connection.cursor()
    try:
        insert_query = """ INSERT INTO institution (admin_id, institution_name, country, town, address, website, email, phone_number)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
         """
        cursor.execute(insert_query, (admin_id, name, country, town, address, website, email, tel))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting Institution:", error)
        return None
    finally:
        cursor.close()


def insert_course(connection, teacher_id, inst_id, title, description, is_confirmed):
    cursor = connection.cursor()
    try:
        insert_query = """ INSERT INTO course (teacher_id, inst_id, title, description, is_confirmed)
                        VALUES (%s, %s, %s, %s, %s);
         """
        cursor.execute(insert_query, (teacher_id, inst_id, title, description, is_confirmed))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting course :", error)
        return None
    finally:
        cursor.close()


def insert_course_content(course_id, content_type, content_data):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        insert_query = """ INSERT INTO content (course_id, content_type, content_data)
                            VALUES (%s, %s, %s);
                            """
        cursor.execute(insert_query, (course_id, content_type, content_data))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting course content : ", error)
    finally:
        cursor.close()


def insert_user(connection, firstname, lastname, email, hashed_password, role):
    """Inserts a new user based on role and returns the generated user_id.

  Args:
      connection: A psycopg2 connection object.
      name: User's name (string).
      email: User's email address (string).
      hashed_password: Hashed password (string).
      role: User's role (string, e.g., 'admin', 'teacher', 'student').
      firstname : User's firstname (string).
      lastname: User's lastname (string).

  Returns:
      The generated user_id (integer) or None on failure.
  """
    cursor = connection.cursor()
    try:
        # Insert user data into the user table with RETURNING clause
        insert_user_query = """
      INSERT INTO mainuser (lastname, firstname, email, password)
      VALUES (%s, %s, %s, %s)
      RETURNING user_id;
    """
        cursor.execute(insert_user_query, (lastname, firstname, email, hashed_password))
        connection.commit()
        # Fetch the generated user_id
        user_id = cursor.fetchone()[0]

        # Insert data into role-specific table based on role
        if role == 'admin':
            insert_admin_query = """
        INSERT INTO instadmin(user_id)
        VALUES (%s);
      """
            cursor.execute(insert_admin_query, (user_id,))
        elif role == 'teacher':
            insert_teacher_query = """
        INSERT INTO teacher (user_id)
        VALUES (%s);
      """
            cursor.execute(insert_teacher_query, (user_id,))
        elif role == 'student':
            insert_student_query = """
        INSERT INTO student (user_id)
        VALUES (%s);
      """
            cursor.execute(insert_student_query, (user_id,))
        else:
            print(f"Invalid role: {role}. User created only in user table.")
        connection.commit()
        return user_id
    except (Exception, psycopg2.Error) as error:
        print("Error inserting user:", error)
        return None
    finally:
        cursor.close()  # Always close the cursor


def close_connection(connection):
    """Closes the connection to the database."""
    if connection:
        connection.close()
        print("Connection to PostgreSQL database closed")
