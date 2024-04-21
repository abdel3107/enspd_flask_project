from flask_login import UserMixin

from db_util import connect_to_db, execute_query


class User(UserMixin):

    def __init__(self, user_id, firstname, lastname, email, role, password_hash):
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.role = role
        self.password_hash = password_hash

    def verify_password(self, password):
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    # def query(self) -> list:
    #     connection = connect_to_db()
    #     if connection:
    #         cursor = connection.cursor()
    #         query1 = """SELECT * FROM mainuser WHERE email = 'tnopaz@gmail.com' """
    #
    #         cursor.execute(query1, )
    #         result = cursor.fetchone()
    #         return result


