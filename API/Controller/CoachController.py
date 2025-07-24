import os

import cv2

from API.Model.User import User
from API.Model.Session import Session
from API.Model.SessionPlayer import SessionPlayer
from API.Model.ShotResult import ShotResult
from API.config import db
from . import ShotIdealAngle
from API.Model.Team import Team
from API.Model.TeamCoach import TeamCoach
from API.Model.TeamPlayer import TeamPlayer
from API.Model.SessionShot import SessionShot
from API.Model.Shot import Shot
from API.Model.Angle import Angle
from API.Model.CoachAngle import CoachAngle
from datetime import datetime


class CoachController:

    @staticmethod
    def get_team(coach_id):
        team_coach = TeamCoach.query.filter(TeamCoach.coach_id == coach_id).first()
        if not team_coach:
            return []
        team = Team.query.filter(Team.id == team_coach.team_id).first()
        all_team_players = TeamPlayer.query.filter(TeamPlayer.team_id == team.id).all()
        team_players_ids = [player.player_id for player in all_team_players]
        all_players = User.query.filter(User.id.in_(team_players_ids)).all()
        players = [{"id": player.id, "name": player.name, "date_of_birth": player.date_of_birth,
                    "contact_no": player.contact_no,
                    "experience": player.experience, 'type': player.type} for player in all_players]

        return {"coachController": [{"id": team.id, "team_name": team.name, "team_players": players}]}

    @staticmethod
    def get_all_players(coach_id):
        team_id = (TeamCoach.query.filter(TeamCoach.coach_id == coach_id).first()).team_id
        teams_players = TeamPlayer.query.filter(TeamPlayer.team_id == team_id).all()
        players_id = [player.player_id for player in teams_players]
        players = User.query.filter(User.id.in_(players_id)).all()

        return {"players": [{"id": player.id, "name": player.name, 'role': player.role, 'username': player.username,
                             'password': player.password, 'experience': player.experience,
                             'date_of_birth': player.date_of_birth,
                             'contact_no': player.contact_no, 'type': player.type} for player in players]}

    @staticmethod
    def arrange_session(name, coach_id, player_id, shot_id, venue, date, session_from, session_to, status='not_processed'):
        try:
            check_coach_session = Session.query.filter(
                Session.coach_id == coach_id,
                Session.date == date,
                db.or_(
                    db.and_(Session.session_from < session_to, Session.session_to > session_from),
                    db.and_(Session.session_from >= session_from, Session.session_to <= session_to),
                    db.and_(Session.session_from <= session_from, Session.session_to >= session_to)
                )
            ).first()
            # A session overlaps when:
            # 1.	The new session starts during an existing session:
            # new_session_from >= existing_session_from AND new_session_from < existing_session_to
            # 2.	The new session ends during an existing session:
            # new_session_to > existing_session_from AND new_session_to <= existing_session_to
            # 3.	The new session completely covers an existing session:
            # new_session_from <= existing_session_from AND new_session_to >= existing_session_to

            if check_coach_session:
                return {"Result": f"You are already in session with id:{check_coach_session.id} at date "
                                  f"{check_coach_session.date} and session_from {check_coach_session.session_from} in "
                                  f"{check_coach_session.venue}"}

            session = Session(name=name, coach_id=coach_id, date=date, session_from=session_from,
                              session_to=session_to, venue=venue, status=status)
            db.session.add(session)
            db.session.flush()
            db.session.refresh(session)

            print(f"Session ID: {session.id}")

            # Create SessionPlayer
            sessionplayer = SessionPlayer(session_id=session.id, player_id=player_id)
            db.session.add(sessionplayer)
            db.session.flush()
            db.session.refresh(sessionplayer)  # Ensure sessionplayer.id is updated

            print(f"SessionPlayer ID: {sessionplayer.id}")

            sessionshot = SessionShot(session_player_id=sessionplayer.id, shot_id=shot_id)
            db.session.add(sessionshot)

            db.session.commit()

            return {"Result": "Session created successfully"}

        except Exception as exp:
            return {"Result": f"Error while creating session is:{exp}"}

    @staticmethod
    def get_arranged_sessions(coach_id):
        try:
            sessions = Session.query.filter(Session.coach_id == coach_id, Session.status == 'not_processed').all()
            return {'arrangedSessions': [{'id': session.id,
                                          'name': session.name,
                                          'player': (User.query.filter(User.id ==
                                                                       (SessionPlayer.query.filter(
                                                                           SessionPlayer.session_id ==
                                                                           session.id).first()).player_id).first()).name,
                                          'date': session.date,
                                          'session_from': session.session_from,
                                          'session_to': session.session_to,
                                          'venue': session.venue} for session in sessions]
                    }
        except Exception as exp:
            return {'result': f"{exp}"}

    @staticmethod
    def get_all_shots():
        try:
            shots = Shot.query.all()
            return {"shots": [{'id': shot.id, 'name': shot.name} for shot in shots]}
        except Exception as exp:
            return {'shots': f"error while fetching shots is {exp}"}

    @staticmethod
    def add_players_in_session(session_id, player_ids):
        try:
            for id in player_ids:
                session_player = SessionPlayer(session_id=session_id, player_id=id)
                db.session.add(session_player)
            db.session.commit()

            return {"Result": "Players added successfully"}
        except Exception as exp:
            return {"Error": exp}

    @staticmethod
    def update_session(session_id):

        db.session.commit()

    @staticmethod
    def delete_session(session_id):

        db.session.commit()

    @staticmethod
    def list_all_sessions():
        sessions = Session.query.all()
        return [{"session_id": session.id, "session_name": session.name,
                 "coach_id": (User.query.filter(User.id == session.coach_id).first()).name, "date": session.date,
                 "session_from": session.session_from.strfsession_from("%H:%M:%S"), "venue": session.venue} for session
                in sessions]

    def get_angle_comparison(shot_id, coach_id, player_angles=None):
        try:
            print("in get_angle_comparison")
            print("coach_id is:", coach_id)
            print("player_angles are:", player_angles)
            # ideal_angles = ShotIdealAngle.query.filter(ShotIdealAngle.shot_id == shot_id).all()
            ideal_angles = CoachAngle.query.filter(CoachAngle.shot_id == shot_id, CoachAngle.coach_id == coach_id).all()
            # ideal_angles = [angle for angle in ideal_angle if angle.coach_id == coach_id]

            if len(ideal_angles) == 0:
                return {"Result": "You need to insert ground truth first to compare."}

            print("ideal_angles are:", ideal_angles)
            angle_map = {}
            for entry in ideal_angles:
                print("entry is:", entry)
                angle_name = entry.angle_name.lower()
                print("angle_name is:", angle_name)
                angle_map[angle_name] = {
                    'from': entry.angle_from,
                    'to': entry.angle_to
                }
            print("angle_map is:", angle_map)
            if player_angles:
                results = [
                    {
                        'Elbow Ideal Angle From': angle_map['elbow angle']['from'],
                        'Elbow Ideal Angle To': angle_map['elbow angle']['to'],
                        'Player Elbow Angle': player_angles['Front Elbow Angle'],
                        'is_angle_correct': angle_map['elbow angle']['from'] < player_angles['Front Elbow Angle'] <
                                            angle_map['elbow angle']['to']
                    },
                    {
                        'Shoulder Inclination Ideal From': angle_map['shoulder inclination']['from'],
                        'Shoulder Inclination Ideal To': angle_map['shoulder inclination']['to'],
                        'Player Shoulder Inclination': player_angles['Shoulder Inclination'],
                        'is_angle_correct': angle_map['shoulder inclination']['from'] < player_angles[
                            'Shoulder Inclination'] < angle_map['shoulder inclination']['to']
                    },
                    {
                        'Wrist Ideal Angle From': angle_map['wrist angle']['from'],
                        'Wrist Ideal Angle To': angle_map['wrist angle']['to'],
                        'Player Wrist Angle': player_angles['Front Wrist Angle'],
                        'is_angle_correct': angle_map['wrist angle']['from'] < player_angles['Front Wrist Angle'] <
                                            angle_map['wrist angle']['to']
                    },
                    {
                        'Hip Ideal Angle From': angle_map['hip angle']['from'],
                        'Hip Ideal Angle To': angle_map['hip angle']['to'],
                        'Player Hip Angle': player_angles['Front Hip Angle'],
                        'is_angle_correct': angle_map['hip angle']['from'] < player_angles['Front Hip Angle'] <
                                            angle_map['hip angle']['to']
                    },
                    {
                        'Knee Ideal Angle From': angle_map['knee angle']['from'],
                        'Knee Ideal Angle To': angle_map['knee angle']['to'],
                        'Player Knee Angle': player_angles['Front Knee Angle'],
                        'is_angle_correct': angle_map['knee angle']['from'] < player_angles['Front Knee Angle'] <
                                            angle_map['knee angle']['to']
                    },
                    {
                        'Bat-Hip Distance Ideal From': angle_map['bat hip distance']['from'],
                        'Bat-Hip Distance Ideal To': angle_map['bat hip distance']['to'],
                        'Player Bat-Hip Distance': player_angles['Bat-Hip Distance'],
                        'is_angle_correct': angle_map['bat hip distance']['from'] < player_angles[
                            'Bat-Hip Distance'] <
                                            angle_map['bat hip distance']['to']
                    },
                ]
            else:  # jab only existing session results ki zaroorat ho performance screen main
                results = {
                    "elbow ideal": {
                        'Elbow Ideal Angle From': angle_map['elbow angle']['from'],
                        'Elbow Ideal Angle To': angle_map['elbow angle']['to'],
                    },
                    "shoulder ideal": {
                        'Shoulder Inclination Ideal From': angle_map['shoulder inclination']['from'],
                        'Shoulder Inclination Ideal To': angle_map['shoulder inclination']['to'],
                    },
                    "wrist ideal": {
                        'Wrist Ideal Angle From': angle_map['wrist angle']['from'],
                        'Wrist Ideal Angle To': angle_map['wrist angle']['to'],
                    },
                    "hip ideal": {
                        'Hip Ideal Angle From': angle_map['hip angle']['from'],
                        'Hip Ideal Angle To': angle_map['hip angle']['to'],
                    },
                    "knee angle": {
                        'Knee Ideal Angle From': angle_map['knee angle']['from'],
                        'Knee Ideal Angle To': angle_map['knee angle']['to'],
                    },
                    "bat-hip ideal distance": {
                        'Bat-Hip Distance Ideal From': angle_map['bat hip distance']['from'],
                        'Bat-Hip Distance Ideal To': angle_map['bat hip distance']['to'],
                    },
                }

            return results
        except Exception as exp:
            return {"error": str(exp)}

    @staticmethod
    def compare_shot_angles(shot_name, player_angles, coach_id):
        print("in compare_shot_angles, shot_name is:", shot_name)
        try:
            shot = Shot.query.filter(Shot.name == shot_name).first()
            print("shot name is:", shot.name)
            print("shot id is:", shot.id)
            # ideal_shots = ShotIdealAngle.query.all()
            # ideal_angles = [{'id': angle.id, 'angle_id': angle.angle_name_id, 'shot_id': angle.shot_id,
            #                  'angle_from': angle.angle_from, 'angle_to': angle.angle_to} for angle in ideal_shots]

            # results = [
            #     {
            #         'Elbow Ideal Angle': [ideal_angles[shot_id]['elbow angle']['angle_from'],
            #                               ideal_angles[shot_id]['elbow angle']['angle_to']],
            #         'Player Elbow Angle': player_angles['Front Elbow Angle'],
            #         'is_shot_correct': (
            #                 ideal_angles[shot_id]['elbow angle']['angle_from'] < player_angles['Front Elbow Angle'] <
            #                 ideal_angles[shot_id]['elbow angle']['angle_to'])
            #     },
            #     {
            #         'Ideal shoulder inclination': [ideal_angles[shot_id]['shoulder inclination']['angle_from'],
            #                                        ideal_angles[shot_id]['shoulder inclination']['angle_to']],
            #         'Player shoulder inclination': player_angles['Shoulder Inclination'],
            #         'is_shot_correct': (
            #                 ideal_angles[shot_id]['shoulder inclination']['angle_from'] < player_angles[
            #             'Shoulder Inclination'] < ideal_angles[shot_id]['shoulder inclination']['angle_to'])
            #     },
            #     {
            #         'Ideal wrist Angle': [ideal_angles[shot_id]['wrist angle']['angle_from'],
            #                               ideal_angles[shot_id]['wrist angle']['angle_to']],
            #         'Player wrist Angle': player_angles['Front Wrist Angle'],
            #         'is_shot_correct': (
            #                 ideal_angles[shot_id]['wrist angle']['angle_from'] < player_angles['Front Wrist Angle'] <
            #                 ideal_angles[shot_id]['wrist angle']['angle_to'])
            #     },
            #     {
            #         'Ideal hip Angle': [ideal_angles[shot_id]['hip angle']['angle_from'],
            #                             ideal_angles[shot_id]['hip angle']['angle_to']],
            #         'Player hip Angle': player_angles['Front Hip Angle'],
            #         'is_shot_correct': (
            #                 ideal_angles[shot_id]['hip angle']['angle_from'] < player_angles['Front Hip Angle'] <
            #                 ideal_angles[shot_id]['hip angle']['angle_to'])
            #     },
            #     {
            #         'Ideal knee Angle': [ideal_angles[shot_id]['knee angle']['angle_from'],
            #                              ideal_angles[shot_id]['knee angle']['angle_to']],
            #         'Player knee Angle': player_angles['Front Knee Angle'],
            #         'is_shot_correct': (
            #                 ideal_angles[shot_id]['knee angle']['angle_from'] < player_angles['Front Knee Angle'] <
            #                 ideal_angles[shot_id]['knee angle']['angle_to'])
            #     },
            #     {
            #         'Ideal bat and hip distance': [ideal_angles[shot_id]['bat and hip distance']['angle_from'],
            #                                        ideal_angles[shot_id]['bat and hip distance']['angle_to']],
            #         'Player bat and hip distance': player_angles['Bat-Hip Distance'],
            #         'is_shot_correct': (
            #                 ideal_angles[shot_id]['bat and hip distance']['angle_from'] < player_angles[
            #             'Bat-Hip Distance'] < ideal_angles[shot_id]['bat and hip distance']['angle_to'])
            #     },
            # ]
            print("in compare_shot_angles, coach_id is:", coach_id)
            results = CoachController.get_angle_comparison(shot.id, coach_id, player_angles)

            return results

        except Exception as exp:
            return {"Error": str(exp)}

    @staticmethod
    def add_shot_result(results, session_id, best_frame, clip_name):
        print("here in add_shot_result")
        print("results, session_id, best_frame, clip_name are:", results, session_id, best_frame, clip_name)

        try:
            correct_angle_names_list = []
            incorrect_angle_names_list = []
            correct_angle_names = ""
            incorrect_angle_names = ""

            shots = {}
            check_for_shot_correction = True
            for result in results:
                player_key = [key for key in result.keys() if 'Player' in key]
                print(f"Shot angle is:{player_key} and is_angle_correct?:{result['is_angle_correct']}")
                if result['is_angle_correct']:
                    angle_name = player_key[0].replace("Player ", "")
                    correct_angle_names_list.append(angle_name)
                    shots[angle_name] = result[player_key[0]]
                else:
                    check_for_shot_correction = False
                    angle_name = player_key[0].replace("Player ", "")
                    incorrect_angle_names_list.append(angle_name)
                    shots[angle_name] = result[player_key[0]]

            correct_angle_names = ", ".join(correct_angle_names_list)
            incorrect_angle_names = ", ".join(incorrect_angle_names_list)

            session = Session.query.filter(Session.id == session_id).first()
            session_player_id = (SessionPlayer.query.filter(SessionPlayer.session_id == session.id).first()).id
            print("session_player_id is:", session_player_id)

            session_shot_id = (
                SessionShot.query.filter(SessionShot.session_player_id == session_player_id).first()).id
            print("session_shot_id is:", session_shot_id)
            shot_id = (SessionShot.query.filter(SessionShot.id == session_shot_id).first()).shot_id
            shot_name = (Shot.query.filter(Shot.id == shot_id).first()).name

            shotResult = ShotResult(session_shot_id=session_shot_id, is_shot_correct=check_for_shot_correction,
                                    elbow_angle=shots['Elbow Angle'],
                                    shoulder_inclination=shots['Shoulder Inclination'],
                                    wrist_angle=shots['Wrist Angle'], hip_angle=shots['Hip Angle'],
                                    knee_angle=shots['Knee Angle'],
                                    bat_hip_distance=shots['Bat-Hip Distance'], correct_angles=correct_angle_names,
                                    incorrect_angles=incorrect_angle_names)

            db.session.add(shotResult)
            db.session.commit()
            db.session.flush()
            last_row = ShotResult.query.order_by(ShotResult.id.desc()).first()
            new_session_shot_id_for_best_frame = last_row.id
            best_frame_saving_path = fr"D:\BIIT\Semester-7(FYP-1)\CrciketCoaching\Frontend\cricket-coaching\public\images\Sessions_best_frame\{shot_name}" + str(
                fr"\sessionId-{session_id}")
            best_frame_path = os.path.join(best_frame_saving_path, shot_name + "-shotResultId-" + str(
                new_session_shot_id_for_best_frame) + ".jpg")
            try:
                os.makedirs(best_frame_saving_path, exist_ok=True)
                print("✅ Folder created or already exists:", best_frame_saving_path)

                success = cv2.imwrite(best_frame_path, best_frame)
                if success:
                    print("✅ First frame saved at:", best_frame_saving_path)
                    last_row.best_frame_path = best_frame_path

                    db.session.commit()
                    db.session.flush()
                else:
                    print("❌ Failed to save the frame. Check path or permissions.")

            except Exception as e:
                print("❌ Failed to create folder:", e)
                exit()
            return {f"Result": f"Results added successfully in database for clip:{clip_name}"}
        except Exception as exp:
            return {"Result": f"error for precessing clip:{clip_name}] is:" + str(exp)}

        # correct_angle_names = ""
        # incorrect_angle_names = ""
        #
        # shots = {}
        # check_for_shot_correction = True
        # for result in results:
        #     player_key = [key for key in result.keys() if 'Player' in key]
        #     print(f"Shot angle is:{player_key[0]} and is_angle_correct?:{result['is_angle_correct']}")
        #     if result['is_angle_correct']:
        #         angle_name = player_key[0].replace("Player ", "")
        #         correct_angle_names = correct_angle_names + angle_name + " "
        #         shots[angle_name] = result[player_key]
        #     else:
        #         check_for_shot_correction = False
        #         angle_name = player_key[0].replace("Player ", "")
        #         incorrect_angle_names = incorrect_angle_names + angle_name + " "
        #         shots[angle_name] = result[player_key]
        # print('here')
        # print("shots['Elbow Angle'] is:", shots['Elbow Angle'])
        # print("correct_angle_names are", correct_angle_names)
        # print("incorrect_angle_names are", incorrect_angle_names)
        # session_player_id = (SessionPlayer.query.filter(SessionPlayer.session_id == session_id).first()).id
        # print("session_player_id is:", session_player_id)
        #
        # session_shot_id = (
        #     SessionShot.query.filter(SessionPlayer.session_player_id == session_player_id).first()).id
        # print("session_shot_id is:", session_shot_id)
        #
        # shotResult = ShotResult(session_shot_id=session_shot_id, is_shot_correct=check_for_shot_correction,
        #                         elbow_angle=shots['Elbow Angle'],
        #                         shoulder_inclination=shots['Shoulder Inclination'],
        #                         wrist_angle=shots['Wrist Angle'], hip_angle=shots['Hip Angle'],
        #                         knee_angle=shots['Knee Angle'],
        #                         bat_hip_distance=shots['Bat-Hip Distance'], correct_angles=correct_angle_names,
        #                         incorrect_angles=incorrect_angle_names)
        #
        # db.session.add(shotResult)
        # db.session.commit()
        #
        # return {"Result: Results added successfully in database"}

    @staticmethod
    def update_session_status(session_id):
        try:
            session = Session.query.filter(Session.id == session_id).first()
            session.status = "processed"
            db.session.commit()
            db.session.flush()
            return {"Result: Success:"}
        except Exception as exp:
            return {f"Result: {exp}"}

    @staticmethod
    def get_session_shot_result(session_id, coach_id):
        try:
            session_player_id = (SessionPlayer.query.filter(SessionPlayer.session_id == session_id).first()).id
            print("session_player_id is:", session_player_id)

            session_shot_id = (
                SessionShot.query.filter(SessionShot.session_player_id == session_player_id).first()).id
            print("session_shot_id is:", session_shot_id)
            shot_id = (SessionShot.query.filter(SessionShot.id == session_shot_id).first()).shot_id
            ideal_angles = CoachController.get_angle_comparison(shot_id, coach_id)

            shotResults = ShotResult.query.filter(ShotResult.session_shot_id == session_shot_id).all()

            return {"Results": [{'id': result.id, 'is_shot_correct': result.is_shot_correct,
                                 'elbow_angle': result.elbow_angle, 'shoulder_inclination': result.shoulder_inclination,
                                 'wrist_angle': result.wrist_angle, 'knee_angle': result.knee_angle,
                                 'hip_angle': result.hip_angle, 'bat_hip_distance':
                                     result.bat_hip_distance, 'correct_angles': result.correct_angles,
                                 'incorrect_angles':
                                     result.incorrect_angles, 'best_frame_path': result.best_frame_path} for result in
                                shotResults],
                    "Ideal Angles": ideal_angles}
        except Exception as exp:
            return {"Error": str(exp)}

    @staticmethod
    def get_ideal_angles(shot_id):
        try:
            # shot_ideal = ShotIdealAngle.query.filter(ShotIdealAngle.shot_id == shot_id).all()
            shot_ideal = db.session.query(ShotIdealAngle, Angle.name).join(Angle).filter(
                ShotIdealAngle.shot_id == shot_id).all()
            ideal_angles = []
            for angle_data, angle_name in shot_ideal:
                # print(f"Angle: {angle_name}, From: {angle_data.angle_from}, To: {angle_data.angle_to}")
                ideal_angles.append(
                    {f"angle_name": angle_name, "angle_id": angle_data.angle_name_id, "From": angle_data.angle_from,
                     "To": angle_data.angle_to})
            return {"Shot Ideal Range": ideal_angles}
        except Exception as exp:
            return {"Error": str(exp)}

    @staticmethod
    def get_angle_name(angle_id):
        try:
            angle = Angle.query.filter(Angle.id == angle_id).first()
            angle_name = angle.name
            return {"Result": angle_name}
        except Exception as exp:
            return {"Error": str(exp)}

    @staticmethod
    def update_ideal_angles(shot_id, angle_id, angle_from, angle_to):
        try:
            shot_ideal = ShotIdealAngle.query.filter(ShotIdealAngle.shot_id == shot_id,
                                                     ShotIdealAngle.angle_name_id == angle_id).first()
            shot_ideal.angle_from = angle_from
            db.session.commit()

            shot_ideal.angle_to = angle_to
            db.session.commit()

            db.session.flush()

            return {"Result": "Angle updated successfully"}
        except Exception as exp:
            return {"Error": str(exp)}

    #
    # @staticmethod
    # def track_shot_progress(player_id, shot_id):
    #     session_players = SessionPlayer.query.filter_by(player_id=player_id).all()
    #
    #     session_shots = SessionShot.query.filter(
    #         SessionShot.session_player_id.in_([sp.id for sp in session_players]),
    #         SessionShot.shot_id == shot_id
    #     ).all()
    #
    #     shot_result_data = ShotResult.query.filter(
    #         ShotResult.session_shot_id.in_([ss.id for ss in session_shots])
    #     ).all()
    #
    #     total = len(shot_result_data)
    #
    #     if total == 0:
    #         return {"Result": "No data available for this shot"}
    #
    #     incorrect_count = sum(1 for res in shot_result_data if not res.is_shot_correct)
    #     accuracy = round(((total - incorrect_count) / total) * 100, 2)
    #
    #     if accuracy < 75:
    #         return {"Result": f"Player's shot accuracy is {accuracy}. Player needs to practice this shot more"}
    #     else:
    #         return {"Result": f"Player's shot accuracy is {accuracy}. Player is doing well with this shot"}

    @staticmethod
    def track_shot_progress(player_id, shot_id):
        try:
            session_players = SessionPlayer.query.filter_by(player_id=player_id).all()
            session_player_ids = [sp.id for sp in session_players]

            if not session_player_ids:
                return {"Result": "No sessions found for this player."}

            session_shots = SessionShot.query.filter(
                SessionShot.session_player_id.in_(session_player_ids),
                SessionShot.shot_id == shot_id
            ).all()

            session_shot_ids = [ss.id for ss in session_shots]
            if not session_shot_ids:
                return {"Result": "No shots of this type found for the player."}

            shot_results = ShotResult.query.filter(
                ShotResult.session_shot_id.in_(session_shot_ids)
            ).all()

            if not shot_results:
                return {"Result": "No shot results found. Upload video in this session to get results."}

            total_shots = len(shot_results)
            incorrect_count = sum(1 for res in shot_results if not res.is_shot_correct)
            accuracy = round(((total_shots - incorrect_count) / total_shots) * 100, 2)

            session_summary = []

            for session_player in session_players:
                session_id = session_player.session_id

                for ss in session_shots:
                    results = [r for r in shot_results if r.session_shot_id == ss.id]

                    total = len(results)
                    correct = sum(1 for r in results if r.is_shot_correct)
                    incorrect = total - correct
                    accuracy = round((correct / total) * 100, 2) if total > 0 else 0.0

                    session_summary.append({
                        "session_id": session_id,
                        "total_shots": total,
                        "correct_shots": correct,
                        "incorrect_shots": incorrect,
                        "accuracy": accuracy
                    })

            return {"Tracking Progress": {
                "player_id": player_id,
                "shot_id": shot_id,
                "overall_accuracy": accuracy,
                "total_sessions": len(session_summary),
                "total_shots": total_shots,
                "session_summary": session_summary,
                "recommendation": f"Player's shot accuracy is {accuracy}. Player needs to practice this shot more" if accuracy < 75 else
                f"Player's shot accuracy is {accuracy}. Player is doing well with this shot"
            }}
        except Exception as exp:
            return {"Error": str(exp)}

    # @staticmethod
    # def compare_player_performance(data):
    #     try:
    #         player_id = data["player_id"]
    #         shot_id = data["shot_id"]
    #         date_from = datetime.strptime(data["dateFrom"], "%Y-%m-%d").date()
    #         date_to = datetime.strptime(data["dateTo"], "%Y-%m-%d").date()
    #
    #         sessions_in_range = Session.query.filter(
    #             Session.date >= date_from,
    #             Session.date <= date_to
    #         ).all()
    #         session_ids = [s.id for s in sessions_in_range]
    #
    #         # Step 2: Get session_player entries for this player and sessions
    #         session_players = SessionPlayer.query.filter(
    #             SessionPlayer.player_id == player_id,
    #             SessionPlayer.session_id.in_(session_ids)
    #         ).all()
    #         session_player_ids = [sp.id for sp in session_players]
    #
    #         # Step 3: Get session_shots for the given shot
    #         session_shots = SessionShot.query.filter(
    #             SessionShot.session_player_id.in_(session_player_ids),
    #             SessionShot.shot_id == shot_id
    #         ).all()
    #         session_shot_ids = [ss.id for ss in session_shots]
    #
    #         # Step 4: Get shot results for these session shots
    #         shot_results = ShotResult.query.filter(
    #             ShotResult.session_shot_id.in_(session_shot_ids)
    #         ).all()
    #
    #         if not shot_results:
    #             return jsonify({"Result": "No performance data available for given player, shot, and date range"}), 200
    #
    #         # Step 5: Group by session and summarize
    #         session_summary = []
    #         for sp in session_players:
    #             session = next((s for s in sessions_in_range if s.id == sp.session_id), None)
    #             session_shot = next((ss for ss in session_shots if ss.session_player_id == sp.id), None)
    #             if not session or not session_shot:
    #                 continue
    #
    #             results = [sr for sr in shot_results if sr.session_shot_id == session_shot.id]
    #             if not results:
    #                 continue
    #
    #             total = len(results)
    #             correct = sum(1 for r in results if r.is_shot_correct)
    #             incorrect = total - correct
    #             accuracy = round((correct / total) * 100, 2)
    #
    #             session_summary.append({
    #                 "session_id": session.id,
    #                 "session_date": session.date.strftime("%Y-%m-%d"),
    #                 "total_shots": total,
    #                 "correct_shots": correct,
    #                 "incorrect_shots": incorrect,
    #                 "accuracy": accuracy
    #             })
    #
    #         return {
    #             "player_id": player_id,
    #             "shot_id": shot_id,
    #             "date_from": date_from.strftime("%Y-%m-%d"),
    #             "date_to": date_to.strftime("%Y-%m-%d"),
    #             "performance": session_summary
    #         }, 200
    #
    #     except Exception as e:
    #         return {"error": str(e)}, 500

    @staticmethod
    def add_ideal_angles(coach_id, shot_id, elbow_angle, wrist_angle,
                         shoulder_inclination, hip_angle, knee_angle, bat_hip_distance):
        try:
            c_angle = CoachAngle(coach_id=coach_id, shot_id=shot_id, angle_name="elbow angle",
                                 angle_from=elbow_angle["from"], angle_to=elbow_angle["to"])
            db.session.add(c_angle)
            db.session.commit()
            c_angle = CoachAngle(coach_id=coach_id, shot_id=shot_id, angle_name="wrist angle",
                                 angle_from=wrist_angle["from"], angle_to=wrist_angle["to"])
            db.session.add(c_angle)
            db.session.commit()
            c_angle = CoachAngle(coach_id=coach_id, shot_id=shot_id, angle_name="shoulder inclination",
                                 angle_from=shoulder_inclination["from"], angle_to=shoulder_inclination["to"])
            db.session.add(c_angle)
            db.session.commit()
            c_angle = CoachAngle(coach_id=coach_id, shot_id=shot_id, angle_name="hip angle",
                                 angle_from=hip_angle["from"], angle_to=hip_angle["to"])
            db.session.add(c_angle)
            db.session.commit()
            c_angle = CoachAngle(coach_id=coach_id, shot_id=shot_id, angle_name="knee angle",
                                 angle_from=knee_angle["from"], angle_to=knee_angle["to"])
            db.session.add(c_angle)
            db.session.commit()
            c_angle = CoachAngle(coach_id=coach_id, shot_id=shot_id, angle_name="bat hip distance",
                                 angle_from=bat_hip_distance["from"], angle_to=bat_hip_distance["to"])
            db.session.add(c_angle)
            db.session.commit()
            db.session.flush()

            return {"Result": "Ideal Angles added successfully"}
        except Exception as exp:
            return {"Error": str(exp)}

# Flash queries corresponding to sql

# Flask: coach = Session.query.filter(Session.date == date, Session.session_from == session_from).with_entities(Session.coach_id).all()
# Sql server: Select coach_id from Session where date = given_date and session_from=given_session_from
