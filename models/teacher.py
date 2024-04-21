class Teacher(object):

    def __init__(self, teacher_id, firstname, lastname, email):
        self.teacher_id = teacher_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

    def __repr__(self):
        return f"{self.lastname}"