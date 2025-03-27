from API.Model.User import User


class LoginController:

    @staticmethod
    def login(username, password):
        print("above user")
        print(f"username is:{username} and password is:{password}")
        user = User.query.filter(User.username == username, User.password == password).first()
        print("above if")
        if user:
            print("below if, above return, and user is:", user)
            return {"result": "Login Successful",
                    'user': {'id': user.id, 'name': user.name, 'role': user.role, 'username': user.username,
                             'password': user.password, 'experience': user.experience, 'date_of_birth': user.date_of_birth,
                             'contact_no': user.contact_no, "path": ''}}
        else:
            return None


# from flask import jsonify, request
# from sqlalchemy.exc import SQLAlchemyError
# from config import Session
# from Models.User import User
#
#
# class UserLoginController:
#
#     @staticmethod
#     def sign_in():
#         data = request.get_json()
#         username = data.get("username")
#         password = data.get("password")
#
#         if not username or not password:
#             return jsonify({"value": False, "message": "Username and password are required"}), 400
#
#         session = Session()
#         try:
#             user = session.query(User).filter_by(username=username, password=password).first()
#
#             if user:
#                 if user.role in ["manager", "coach", "player", "admin"]:
#                     return jsonify({
#                         "value": True,
#                         "message": f"Login successful as {user.role}",
#                         "role": user.role
#                     }), 200
#                 else:
#                     return jsonify({"value": False, "message": "Invalid role"}), 403
#             else:
#                 return jsonify({"value": False, "message": "Invalid username or password"}), 401
#
#         except SQLAlchemyError as e:
#             return jsonify({"value": False, "error": str(e)}), 500
#
#         finally:
#             session.close()
