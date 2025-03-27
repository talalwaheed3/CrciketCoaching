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
        except Exception:
            return {"Result": "Error while adding players in this session."}

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
    def add_shot_result(sessionshot_id, player_angles):

        ideal_shots = ShotIdealAngle.query.all()
        ideal_angles = [{'id': angle.id, 'angle_id': angle.angle_name_id, 'shot_id': angle.shot_id,
                         'angle_from': angle.angle_from, 'angle_to': angle.angle_to} for angle in ideal_shots]

        results = [
            {
                'Left Arm Ideal Angle': [ideal_angles[0]['angle_from'], ideal_angles[0]['angle_to']],
                'Left Arm Played Angle': player_angles['Left Arm Angle'],
                'is_shot_correct': (
                        ideal_angles[0]['angle_from'] < player_angles['Left Arm Angle'] < ideal_angles[0]['angle_to'])
            },
            {
                'Right Arm Ideal Angle': [ideal_angles[1]['angle_from'], ideal_angles[1]['angle_to']],
                'Right Arm Played Angle': player_angles['Right Arm Angle'],
                'is_shot_correct': (
                        ideal_angles[1]['angle_from'] < player_angles['Right Arm Angle'] < ideal_angles[1]['angle_to'])
            },
            {
                'Left Leg Ideal Angle': [ideal_angles[2]['angle_from'], ideal_angles[2]['angle_to']],
                'Left Leg Played Angle': player_angles['Left Leg Angle'],
                'is_shot_correct': (
                        ideal_angles[2]['angle_from'] < player_angles['Left Leg Angle'] < ideal_angles[2]['angle_to'])
            },
            {
                'Right Leg Ideal Angle': [ideal_angles[3]['angle_from'], ideal_angles[3]['angle_to']],
                'Right Leg Played Angle': player_angles['Right Leg Angle'],
                'is_shot_correct': (
                        ideal_angles[3]['angle_from'] < player_angles['Right Leg Angle'] < ideal_angles[3]['angle_to'])
            }
        ]

        shot_check = True
        correct_angle_names_list = []
        incorrect_angle_names_list = []
        for item in results:
            key_name = list(item.keys())[1]
            angle_name = key_name.split(" Played Angle")[0]
            if item["is_shot_correct"]:
                correct_angle_names_list.append(angle_name)
            else:
                check = False
                incorrect_angle_names_list.append(angle_name)
        correct_angle_names = ", ".join(correct_angle_names_list)
        incorrect_angle_names = ", ".join(incorrect_angle_names_list)
        shotresult = ShotResult(session_shot_id=sessionshot_id, is_shot_correct=shot_check,
                                left_arm_angle=player_angles['Left Arm Angle'],
                                right_arm_angle=player_angles['Right Arm Angle'],
                                left_leg_angle=player_angles['Left Leg Angle'],
                                right_leg_angle=player_angles['Right Leg Angle'],
                                correct_angles=correct_angle_names if correct_angle_names else None,
                                incorrect_angles=incorrect_angle_names if incorrect_angle_names else None)
        db.session.add(shotresult)
        db.session.commit()

        return results

# Flash queries corresponding to sql

# Flask: coach = Session.query.filter(Session.date == date, Session.session_from == session_from).with_entities(Session.coach_id).all()
# Sql server: Select coach_id from Session where date = given_date and session_from=given_session_from
