import psycopg2

from models.institutions import Institution
from models.teacher import Teacher


class Course(object):

    def __init__(self, course_id, teacher_id, inst_id, title, description, is_confirmed):
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.inst_id = inst_id
        self.title = title
        self.description = description
        self.is_confirmed = is_confirmed

    def __repr__(self):
        return f"{self.title}"

    def get_id(self):
        return self.course_id

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_confirmation_status(self):
        return self.is_confirmed

    def get_teacher_name(self):
        teacher = get_teacher(self.teacher_id)
        return teacher.lastname + " " + teacher.firstname

    def get_teacher_email(self):
        teacher = get_teacher(self.teacher_id)
        return teacher.email

    def get_institution_name(self):
        institution = get_institution_by_id(self.inst_id)
        return institution.institution_name


def get_institution_by_id(inst_id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = """ SELECT * FROM institution WHERE inst_id = %s"""
        cursor.execute(query, (inst_id,))
        response = cursor.fetchone()
        institution = Institution(*response)
        return institution
    except (Exception, psycopg2.Error) as error:
        print("Error geting institution:", error)
        return None
    finally:
        cursor.close()


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