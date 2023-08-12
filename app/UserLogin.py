from .models import Users
# from db.db_utils import Database
from flask_login import UserMixin

# dbase = Database()


class UserLogin(UserMixin):
    def __init__(self):
        self.__user = None

    def from_db(self, user_id):
        self.__user = Users.query.get(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.id)

    def get_user(self, user_id):
        self.__user = Users.query.get(user_id)
        return self

    # def is_admin(self):
    #     user_status = self.__user[0]['role']
    #     if user_status == 'admin':
    #         return True
