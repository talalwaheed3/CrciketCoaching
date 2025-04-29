from API.Controller.ManagerController import ManagerController
from API.Controller.PlayerController import PlayerController
from Controller.LoginController import LoginController
from flask import request, jsonify
from API.config import app
from Controller.AdminController import AdminController
from Controller.CoachController import CoachController
from PIL import Image
from API import processing_video
from flask_cors import CORS

CORS(app)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    try:
        user = LoginController.login(data['username'], data['password'])
        if user:
            return jsonify(user)
        else:
            return jsonify("error: incorrect username or password")
    except Exception as exp:
        return jsonify("error while processing the request ")


@app.route('/manager/add_team', methods=['POST'])
def add_team():
    data = request.get_json()

    try:
        print("here in try")
        result = ManagerController.add_team(data['name'], data['list_of_players'], data["coach_id"])
        return jsonify(result)

    except Exception as exp:
        return jsonify(f"error ${exp}: Error while processing the request!!!")


@app.route('/manager/add_coach', methods=['POST'])
def add_coach():
    data = request.get_json()

    try:
        result = ManagerController.add_user(data["name"], data["role"], data["username"], data["password"],
                                            data["experience"], data["age"], data["contact_no"])
        if not result["result"]:
            return jsonify(False)

        return jsonify(result)
    except:
        return jsonify("error while processing the request!!!")


@app.route('/manager/add_player', methods=['POST'])
def add_player():
    data = request.get_json()

    try:
        print('here above result')
        result = ManagerController.add_user(data["name"], data["role"], data["username"], data["password"],
                                            data["experience"], data["date_of_birth"], data["contact_no"], data["type"])
        return jsonify(result)
    except Exception as exp:
        return jsonify(f"error while processing the request is {exp}")


@app.route("/manager/list_all_users", methods=["POST"])
def list_all_users():
    data = request.get_json()
    print("data['role'] is:", data["role"])
    try:
        users = ManagerController.list_all_users(data["role"])
        print("in try before if")
        if users:
            print("true there are users")

            return jsonify(users)
        else:
            print("false there are no users")
            return jsonify(f"error: no f{data['role']} found.")
    except Exception as exp:
        print("True here in exception")
        return jsonify("error while processing the request")


@app.route("/manager/list_all_users_by_is_assigned", methods=["POST"])
def list_all_users_by_is_assigned():
    data = request.get_json()
    try:
        # print("data['checkAssigned'] is:", data["checkAssigned"])
        users = ManagerController.list_all_users_by_is_assigned(data["role"],
                                                                data["checkAssigned"])
        print("in try before if")
        if users:
            print("true there are users")

            # print("check is:", users)
            return jsonify(users)
        else:
            print("false there are no users")
            return jsonify(f"error: no f{data['role']} found.")
    except Exception as exp:
        print("True here in exception")
        return jsonify("error while processing the request")


@app.route("/manager/list_all_teams", methods=["GET"])
def list_all_teams():
    teams = ManagerController.list_all_teams()
    return jsonify(teams)


@app.route('/admin/delete_team', methods=["DELETE"])
def delete_team():
    data = request.get_json()
    required_field = "name"

    if required_field not in data:
        return jsonify(f"error: f{required_field} is missing from data")

    try:
        print("in try")
        print(data["name"])
        result_check = AdminController.delete_team(data["name"])
        return jsonify(result_check)

    except Exception as exp:
        return jsonify("Error while deleting the team")


@app.route("/coach/get_team", methods=['POST'])
def get_team():
    data = request.get_json()
    team = CoachController.get_team(data["coach_id"])
    try:
        if team:
            return jsonify(team)
        else:
            return jsonify(team)
    except Exception as exp:
        return jsonify(f"error in app.py is: {exp}")


@app.route("/coach/get_all_players", methods=['POST'])
def get_all_players():
    data = request.get_json()
    team = CoachController.get_all_players(data["coach_id"])
    try:
        if team:
            return jsonify(team)
        else:
            return jsonify(team)
    except Exception as exp:
        return jsonify(f"error in app.py is: {exp}")


@app.route("/coach/arrange_session", methods=["POST"])
def arrange_session():
    data = request.get_json()
    try:
        result_check = CoachController.arrange_session(data['name'], data['coach_id'], data['player_id'], data['shot_id'], data['venue'],
                                                       data['date'], data['session_from'], data['session_to'])

        return jsonify(result_check)
    except Exception as exp:
        return jsonify(f"error while processing the request is: {exp}")


@app.route("/coach/get_arranged_sessions", methods=["POST"])
def get_arranged_sessions():
    data = request.get_json()
    try:
        result_check = CoachController.get_arranged_sessions(data['coach_id'])

        return jsonify(result_check)
    except Exception as exp:
        return jsonify(f"error while processing the request is: {exp}")


@app.route("/player/get_joined_sessions", methods=["POST"])
def get_joined_sessions():
    data = request.get_json()
    print("data['player_id']", data['player_id'])
    try:
        result_check = PlayerController.get_joined_sessions(data['player_id'])

        return jsonify(result_check)
    except Exception as exp:
        return jsonify(f"error while processing the request is: {exp}")


@app.route("/coach/get_all_shots", methods=["GET"])
def get_all_shots():
    try:
        shots = CoachController.get_all_shots()
        return jsonify(shots)
    except Exception as exp:
        return jsonify(f"error while processing the Http request is:{exp}")


@app.route("/coach/list_all_sessions", methods=["GET"])
def list_all_sessions():
    sessions = CoachController.list_all_sessions()
    if sessions:
        return jsonify(sessions)
    else:
        return jsonify({"Error: Sessions not found"})


@app.route('/coach/process_video', methods=["POST"])
def process_video():
    session_id = request.form.get('session_id')
    shot_name = request.form.get('shot_name')
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        print('video is:', r"Videos\\"+uploaded_file.filename)
        my_angles = processing_video.process_video(r"Videos\\"+uploaded_file.filename)
        # print("my_angles are", my_angles)
        shot_results = CoachController.compare_shot_angles(shot_name, my_angles)
        # results = CoachController.add_shot_result(shot_results, session_id)

        print('results are:', shot_results)
        return jsonify(shot_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/coach/get_shot_result', methods=["POST"])
def get_session_shot_result():
    data = request.get_json()

    try:
        shot_results = CoachController.get_session_shot_result(data['session_id'])

        print('results are:', shot_results)
        return jsonify(shot_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/coach/add_players_in_session/<int:session_id>", methods=["POST"])
def add_players_in_session(session_id):
    data = request.get_json()
    required_field = "player_id"  # List of player ids
    if not required_field:
        return jsonify({f"error: required field f{required_field} is missing from the data"})
    else:
        sessions = CoachController.add_players_in_session(session_id, data["player_id"])
        if sessions:
            return jsonify(sessions)
        else:
            return jsonify({"Error: Sessions not found"})


if __name__ == "__main__":
    app.run(debug=True)
