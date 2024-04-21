import psycopg2

from db_util import connect_to_db
from models.institutions import Institution


def get_institutions():
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
