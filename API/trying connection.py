from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from API import angles


@app.route('/ideal_shots', methods=['GET', 'POST'])
def get_ideal_shots():
    if request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        file = request.files['image']
        try:
            # Open the image and pass it to MediaPipe for pose landmarks extraction
            image = Image.open(file.stream)

            # Calculate angles
            my_angles = angles.processing_image(image)
            ideal_shots = ShotIdealAngle.query.all()
            ideal_angles = [{'id': angle.id, 'angle_id': angle.angle_name_id, 'shot_id': angle.shot_id,
                             'angle_from': angle.angle_from, 'angle_to': angle.angle_to} for angle in ideal_shots]

            results = [
                {
                    'Left Arm Ideal Angle': [ideal_angles[0]['angle_from'], ideal_angles[0]['angle_to']],
                    'Left Arm Played Angle': my_angles['Left Arm Angle'],
                    'is_shot_correct': (ideal_angles[0]['angle_from'] < my_angles['Left Arm Angle'] < ideal_angles[0]['angle_to'])
                },
                {
                    'Right Arm Ideal Angle': [ideal_angles[1]['angle_from'], ideal_angles[1]['angle_to']],
                    'Right Arm Played Angle': my_angles['Right Arm Angle'],
                    'is_shot_correct': (ideal_angles[1]['angle_from'] < my_angles['Right Arm Angle'] < ideal_angles[1]['angle_to'])
                },
                {
                    'Left Leg Ideal Angle': [ideal_angles[2]['angle_from'], ideal_angles[2]['angle_to']],
                    'Left Leg Played Angle': my_angles['Left Leg Angle'],
                    'is_shot_correct': (ideal_angles[2]['angle_from'] < my_angles['Left Leg Angle'] < ideal_angles[2]['angle_to'])
                },
                {
                    'Right Leg Ideal Angle': [ideal_angles[3]['angle_from'], ideal_angles[3]['angle_to']],
                    'Right Leg Played Angle': my_angles['Right Leg Angle'],
                    'is_shot_correct': (ideal_angles[3]['angle_from'] < my_angles['Right Leg Angle'] < ideal_angles[3]['angle_to'])
                }
            ]

            return jsonify(results), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # # Render the upload form on GET request
    # return render_template('upload_form.html')

# @app.route('/ideal_shots', methods=['GET', 'POST'])
# def get_ideal_shots():
#     if request.method == 'POST':
#         if 'image' not in request.files:
#             return jsonify({"error": "No image provided"}), 400
#
#         file = request.files['image']
#         try:
#             # Open the image and pass it to MediaPipe for pose landmarks extraction
#             image = Image.open(file.stream)
#
#             # Calculate angles
#             my_angles = angles.processing_image(image)
#             ideal_shots = ShotIdealAngle.query.all()
#             ideal_angles = [{'id': angle.id, 'angle_id': angle.angle_name_id, 'shot_id': angle.shot_id,
#                              'angle_from': angle.angle_from, 'angle_to': angle.angle_to} for angle in ideal_shots]
#
#             results = {
#                 'Left Arm': {
#                     'Ideal Angle': [ideal_angles[0]['angle_from'], ideal_angles[0]['angle_to']],
#                     'Played Angle': my_angles['Left Arm Angle'],
#                     'is_shot_correct': (ideal_angles[0]['angle_from'] < my_angles['Left Arm Angle'] < ideal_angles[0]['angle_to'])
#                 },
#                 'Right Arm': {
#                     'Ideal Angle': [ideal_angles[1]['angle_from'], ideal_angles[1]['angle_to']],
#                     'Played Angle': my_angles['Right Arm Angle'],
#                     'is_shot_correct': (ideal_angles[1]['angle_from'] < my_angles['Right Arm Angle'] < ideal_angles[1]['angle_to'])
#                 },
#                 'Left Leg': {
#                     'Ideal Angle': [ideal_angles[2]['angle_from'], ideal_angles[2]['angle_to']],
#                     'Played Angle': my_angles['Left Leg Angle'],
#                     'is_shot_correct': (ideal_angles[2]['angle_from'] < my_angles['Left Leg Angle'] < ideal_angles[2]['angle_to'])
#                 },
#                 'Right Leg': {
#                     'Ideal Angle': [ideal_angles[3]['angle_from'], ideal_angles[3]['angle_to']],
#                     'Played Angle': my_angles['Right Leg Angle'],
#                     'is_shot_correct': (ideal_angles[3]['angle_from'] < my_angles['Right Leg Angle'] < ideal_angles[3]['angle_to'])
#                 }
#             }
#
#             return jsonify(results), 200
#
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
#
#     # Render the upload form on GET request
#     return render_template('upload_form.html')



@app.route('/get_user')
def get_user():
    users = User.query.all()
    user_data = [{'id': user.id, 'name': user.name, 'role': user.role} for user in users]
    return user_data


@app.route('/get_team')
def get_team():
    teams = Team.query.all()
    team_data = [{'id': team.id, 'name': team.name} for team in teams]
    return team_data


if __name__ == '__main__':
    app.run(debug=True)




