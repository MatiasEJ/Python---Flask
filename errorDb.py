from flask_mysqldb import MySQL

class NotFoundError(Exception):
    pass
class NotAuthError(Exception):
    pass