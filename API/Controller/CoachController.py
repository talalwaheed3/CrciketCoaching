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


class CoachController:

    @staticmethod
    def get_team(coach_id):
        team_coach = TeamCoach.query.filter(TeamCoach.coach_id == coach_id).first()
        if not team_coach:
            return []
        team = Team.query.filter(Team.id == team_coach.team_id).first()
        if not team:
            return []
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
    def arrange_session(name, coach_id, player_id, shot_id, venue, date, session_from, session_to, status='0'):
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
            # Create Session
            session = Session(name=name, coach_id=coach_id, date=date, session_from=session_from,
                              session_to=session_to, venue=venue, status=status)
            db.session.add(session)
            db.session.flush()
            db.session.refresh(session)  # Ensure session.id is updated

            print(f"Session ID: {session.id}")  # Debugging

            # Create SessionPlayer
            sessionplayer = SessionPlayer(session_id=session.id, player_id=player_id)
            db.session.add(sessionplayer)
            db.session.flush()
            db.session.refresh(sessionplayer)  # Ensure sessionplayer.id is updated

            print(f"SessionPlayer ID: {sessionplayer.id}")  # Debugging

            # Create SessionShot
            sessionshot = SessionShot(session_player_id=sessionplayer.id, shot_id=shot_id)
            db.session.add(sessionshot)

            # Commit the entire transaction
            db.session.commit()

            return {"Result": "Session created successfully"}

        except Exception as exp:
            return {"Result": f"Error while creating session is:{exp}"}

    @staticmethod
    def get_arranged_sessions(coach_id):
        try:
            sessions = Session.query.filter(Session.coach_id == coach_id, Session.status == '0').all()
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

    # @staticmethod
    # def uploadSession(videoPath):
    #

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

    @staticmethod
    def compare_shot_angles(shot_name, player_angles):
        try:
            shot = Shot.query.filter(Shot.name == shot_name).first()
            print("shot name is:", shot.name)
            print("shot id is:", shot.id)
            # ideal_shots = ShotIdealAngle.query.all()
            # ideal_angles = [{'id': angle.id, 'angle_id': angle.angle_name_id, 'shot_id': angle.shot_id,
            #                  'angle_from': angle.angle_from, 'angle_to': angle.angle_to} for angle in ideal_shots]

            ideal_angles = ShotIdealAngle.query.filter(ShotIdealAngle.shot_id == shot.id).all()

            # Map ideal angles by angle name
            angle_map = {}
            for entry in ideal_angles:
                angle_obj = Angle.query.filter_by(id=entry.angle_name_id).first()
                angle_name = angle_obj.name.lower()
                angle_map[angle_name] = {
                    'from': entry.angle_from,
                    'to': entry.angle_to
                }
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
                    'Bat-Hip Distance Ideal From': angle_map['bat and hip distance']['from'],
                    'Bat-Hip Distance Ideal To': angle_map['bat and hip distance']['to'],
                    'Player Bat-Hip Distance': player_angles['Bat-Hip Distance'],
                    'is_angle_correct': angle_map['bat and hip distance']['from'] < player_angles['Bat-Hip Distance'] <
                                       angle_map['bat and hip distance']['to']
                },
            ]

            return results

        except Exception as exp:
            return {"Error": str(exp)}

    @staticmethod
    def add_shot_result(results, session_id):

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

            session_player_id = (SessionPlayer.query.filter(SessionPlayer.session_id == session_id).first()).id
            print("session_player_id is:", session_player_id)

            session_shot_id = (
                SessionShot.query.filter(SessionShot.session_player_id == session_player_id).first()).id
            print("session_shot_id is:", session_shot_id)

            shotResult = ShotResult(session_shot_id=session_shot_id, is_shot_correct=check_for_shot_correction,
                                    elbow_angle=shots['Elbow Angle'],
                                    shoulder_inclination=shots['Shoulder Inclination'],
                                    wrist_angle=shots['Wrist Angle'], hip_angle=shots['Hip Angle'],
                                    knee_angle=shots['Knee Angle'],
                                    bat_hip_distance=shots['Bat-Hip Distance'], correct_angles=correct_angle_names,
                                    incorrect_angles=incorrect_angle_names)

            db.session.add(shotResult)
            db.session.commit()

            return {"Result: Results added successfully in database"}
        except Exception as exp:
            return {"Error": str(exp)}

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
    def get_session_shot_result(session_id):
        try:
            session_player_id = (SessionPlayer.query.filter(SessionPlayer.session_id == session_id).first()).id
            print("session_player_id is:", session_player_id)

            session_shot_id = (
                SessionShot.query.filter(SessionPlayer.session_player_id == session_player_id).first()).id
            print("session_shot_id is:", session_shot_id)

            shotResult = ShotResult.query.filter(ShotResult.session_shot_id == session_shot_id).first()

            return shotResult
        except Exception as exp:
            return {"Error": str(exp)}


# Flash queries corresponding to sql

# Flask: coach = Session.query.filter(Session.date == date, Session.session_from == session_from).with_entities(Session.coach_id).all()
# Sql server: Select coach_id from Session where date = given_date and session_from=given_session_from
