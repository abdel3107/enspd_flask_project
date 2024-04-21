class Institution(object):

    def __init__(self, inst_id, admin_id, institution_name, country, town, address, website, email, phone_number):
        self.inst_id = inst_id
        self.admin_id = admin_id
        self.institution_name = institution_name
        self.country = country
        self.town = town
        self.address = address
        self.website = website
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return self.institution_name

    def get_id(self):
        return self.inst_id

    def get_name(self):
        return self.institution_name
