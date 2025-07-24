import cv2

from API.Controller.ManagerController import ManagerController
from API.Controller.PlayerController import PlayerController
from Controller.LoginController import LoginController
from flask import request, jsonify
from API.config import app
from Controller.AdminController import AdminController
from Controller.CoachController import CoachController
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
        result = ManagerController.add_team(data['name'], data['players'], data["coach_id"])
        return jsonify(result)

    except Exception as exp:
        return jsonify(f"error ${exp}: Error while processing the request!!!")


@app.route('/manager/add_coach', methods=['POST'])
def add_coach():
    data = request.get_json()
    print("data.items is:", data.items())
    try:
        result = ManagerController.add_user(data["name"], "coach", data["username"], data["password"],
                                            data["experience"], data["date_of_birth"], data["contact_no"])
        if not result["result"]:
            return jsonify(False)

        return jsonify(result)
    except Exception as exp:
        return jsonify("error while processing the request!!!", exp)


@app.route('/manager/add_player', methods=['POST'])
def add_player():
    data = request.get_json()

    try:
        print('here above result')
        result = ManagerController.add_user(data["name"], "player", data["username"], data["password"],
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
        users = ManagerController.list_all_users_by_is_assigned(data["role"], data["checkAssigned"])
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


# @app.route('/manager/delete_team', methods=["DELETE"])
# def delete_team():
#     data = request.get_json()
#     required_field = "name"
#
#     if required_field not in data:
#         return jsonify(f"error: f{required_field} is missing from data")
#
#     try:
#         print("in try")
#         print(data["name"])
#         result_check = AdminController.delete_team(data["name"])
#         return jsonify(result_check)
#
#     except Exception as exp:
#         return jsonify("Error while deleting the team")


# <-------------------------- Coach Routes -------------------------->
# <-------------------------- Coach Routes -------------------------->
# <-------------------------- Coach Routes -------------------------->

@app.route("/coach/get_team", methods=['POST'])
def get_coach_team():
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
        result_check = CoachController.arrange_session(data['name'], data['coach_id'], data['player_id'],
                                                       data['shot_id'], data['venue'],
                                                       data['date'], data['session_from'], data['session_to'])

        return jsonify(result_check)
    except Exception as exp:
        return jsonify(f"error while processing the request is: {exp}")


@app.route("/coach/get_arranged_sessions", methods=["POST"])
def get_arranged_sessions():
    data = request.get_json()
    try:
        result_check = CoachController.get_arranged_sessions(data['user_id'])

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


@app.route('/coach/process_video', methods=["POST"])
def process_video():
    session_id = request.form.get('session_id')
    coach_id = request.form.get('coach_id')
    print("in proceess video, coach_id is:", coach_id)
    print("in proceess video, session_id is:", session_id)
    print("in proceess video, coach_id is:", coach_id)

    shot_name = request.form.get('shot_name')
    print("in proceess video, shot_name is:", shot_name)

    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400
    try:
        print('video is:', r"Videos\\Pullshot_ideal_angles\\" + uploaded_file.filename)
        result = processing_video.process_video(r"Videos\\Testing Videos\\" + uploaded_file.filename,
                                                uploaded_file.filename, session_id, shot_name, coach_id)

        # list_of_angles_result = processing_video.process_video(r"Videos\\Testing Videos\\" + uploaded_file.filename,
        #                                                        uploaded_file.filename, session_id, shot_name)
        # print('list_of_angles_result are:', list_of_angles_result)
        #
        # results = {"Result": []}
        # for item in list_of_angles_result:
        #     shot_results = CoachController.compare_shot_angles(shot_name, item['angles'])
        #     result = CoachController.add_shot_result(shot_results, session_id, item['image'], item["clip_name"])
        #     results["Result"].append(result)

        # is_update_status = CoachController.update_session_status(session_id)
        # results.append(is_update_status)
        print(' ')
        print('results are:', result)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/coach/get_shot_result', methods=["POST"])
def get_session_shot_result():
    data = request.get_json()
    print('successfully hitting the api')
    try:
        print("data['session_id'], data['coach_id'] is:", data['session_id'], data['coach_id'])
        shot_results = CoachController.get_session_shot_result(data['session_id'], data['coach_id'])

        # print('results are:', shot_results)
        return jsonify(shot_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/coach/get_ideal_angles', methods=["POST"])
def get_ideal_angles():
    data = request.get_json()
    print('data["shot_id"] is:', data["shot_id"])
    try:
        shot_results = CoachController.get_ideal_angles(data["shot_id"])
        print("shot_results are:", shot_results)
        return jsonify(shot_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/coach/update_ideal_angles', methods=["PUT"])
def update_ideal_angles():
    data = request.get_json()
    print('data["from"] is:', data["from"])
    try:
        shot_results = CoachController.update_ideal_angles(data["shot_id"], data["angle_id"], data["from"], data["to"])
        print("result is:", shot_results)
        return jsonify(shot_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route('/coach/track_shot_progress', methods=["POST"])
# def track_shot_progress():
#     data = request.get_json()
#     try:
#         player_id = data['player_id']
#         shot_id = data['shot_id']
#         result = CoachController.track_shot_progress(player_id, shot_id)
#         return jsonify(result)
#
#     except Exception as exp:
#         return jsonify({"error": str(exp)}), 500

@app.route('/coach/add_ideal_angles', methods=["POST"])
def add_ideal_angles():
    data = request.get_json()
    try:
        result = CoachController.add_ideal_angles(data['coach_id'], data['shot_id'], data['elbow_angle'], data['wrist_angle'],
                                                  data['shoulder_inclination'], data['hip_angle'], data['knee_angle'], data['bat_hip_distance'])
        return jsonify(result)
    except Exception as exp:
        return jsonify({"error": str(exp)}), 500


@app.route("/coach/compare_performance", methods=["POST"])
def compare_player_performance():
    data = request.get_json()

    try:
        result = CoachController.compare_player_performance(data)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/coach/get_angle_name", methods=["POST"])
def get_angle_name():
    data = request.get_json()

    try:
        result = CoachController.get_angle_name(data["angle_id"])
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# <-------------------------- Player Routes -------------------------->
# <-------------------------- Player Routes -------------------------->
# <-------------------------- Player Routes -------------------------->

@app.route("/player/get_team", methods=['POST'])
def get_player_team():
    data = request.get_json()
    team = PlayerController.get_team(data["player_id"])
    try:
        if team:
            return jsonify(team)
        else:
            return jsonify(team)
    except Exception as exp:
        return jsonify(f"error in get_team() is: {exp}")


@app.route("/player/get_joined_sessions", methods=["POST"])
def get_joined_sessions():
    data = request.get_json()
    # print("data['user_id'] is:", data['player_id'])
    try:
        result_check = PlayerController.get_joined_sessions(data['user_id'])
        return jsonify(result_check)
    except Exception as exp:
        return jsonify(f"error while processing the request is: {exp}")


@app.route('/player/get_shot_result', methods=["POST"])
def get_player_session_performance():
    data = request.get_json()
    print('successfully hitting the api')
    try:
        shot_results = PlayerController.get_player_session_performance(data['session_id'])

        print('results are:', shot_results)
        return jsonify(shot_results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
