class Content(object):

    def __init__(self, content_id, course_id, content_type, content_data):
        self.content_id = content_id
        self.course_id = course_id
        self.content_type = content_type
        self.content_data = content_data

    def __repr__(self):
        return f"{self.content_id}:{self.content_type}:{self.content_data}"

    def get_content(self):
        return self.content_data

