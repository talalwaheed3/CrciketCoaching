from API.Model.User import User
from API.config import db


class UserController:

    @staticmethod
    def list_all_users(role):
        users = User.query.filter(User.role == role, User.validity == "true").all()
        print("here in list_all_users")
        return {"Success": True, "Coaches": [{"id": user.id, "name": user.name, 'role': user.role,
                                              'username': user.username, 'password': user.password,
                                              'experience': user.experience,
                                              'age': user.age, 'contact_no': user.contact_no, 'type': user.type}
                                             for user in users]} if users else {"Success": False, 'users': []}

    @staticmethod
    def change_availability(id):
        user = User.query.filter(User.id == id).first()

        if user:
            if user.validity == "false":
                user.validity = "true"
            else:
                user.validity = "false"
            db.session.commit()
