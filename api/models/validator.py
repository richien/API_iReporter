import re

class Validate:

    @staticmethod
    def is_valid_email_format(email):
        if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email) != None:
            return True
        else:
            return False