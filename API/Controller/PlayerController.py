from . import Session
from . import SessionPlayer
from . import ShotResult
from . import SessionShot
from API.config import db
from .CoachController import CoachController
from ..Model.Team import Team
from ..Model.TeamCoach import TeamCoach
from ..Model.TeamPlayer import TeamPlayer
from ..Model.User import User


class PlayerController:

    @staticmethod
    def get_team(player_id):
        team_player = TeamPlayer.query.filter(TeamPlayer.player_id == player_id).first()
        if not team_player:
            return []
        team = Team.query.filter(Team.id == team_player.team_id).first()
        all_team_players = TeamPlayer.query.filter(TeamPlayer.team_id == team.id).all()
        team_players_ids = [player.player_id for player in all_team_players]
        all_players = User.query.filter(User.id.in_(team_players_ids)).all()
        players = [{"id": player.id, "name": player.name, "date_of_birth": player.date_of_birth,
                    "contact_no": player.contact_no,
                    "experience": player.experience, 'type': player.type} for player in all_players]
        coach_id = (TeamCoach.query.filter(TeamCoach.team_id == team.id).first()).coach_id
        coach = User.query.filter(User.id == coach_id).first()
        team_coach = {"id": coach.id, "name": coach.name, "date_of_birth": coach.date_of_birth,
                      "contact_no": coach.contact_no,
                      "experience": coach.experience}

        return {"playerController":
                    {"id": team.id, "team_name": team.name, 'team_coach': team_coach, "team_players": players}}

    @staticmethod
    def get_joined_sessions(player_id):
        print("player_id is:", player_id)
        try:
            allSessionPlayers = SessionPlayer.query.filter(SessionPlayer.player_id == player_id).all()
            print("1,:", allSessionPlayers)
            sessionsIds = [sessionPlayer.session_id for sessionPlayer in allSessionPlayers]
            print("2:", sessionsIds)
            sessions = Session.query.filter(Session.id.in_(sessionsIds), Session.status == 'not_processed').all()
            print("3:", sessions)
            return {'joinedSessions': [{'id': session.id,
                                        'name': session.name,
                                        'coach': (User.query.filter(User.id == session.coach_id).first()).name,
                                        'date': session.date,
                                        'session_from': session.session_from,
                                        'session_to': session.session_to,
                                        'venue': session.venue} for session in sessions]
                    }
        except Exception as exp:
            return {'result': f"{exp}"}

    @staticmethod
    def list_all_sessions(player_id):
        player_sessions = SessionPlayer.query.filter(SessionPlayer.player_id == player_id).all()
        session_ids = [player_session.session_id for player_session in player_sessions]
        sessions = Session.query.filter(Session.id.in_(session_ids)).all()
        return [{"id": session.id, "name": session.name, "coach_id": session.coach_id,
                 "date": session.date, "time": session.time, "venue": session.venue} for session in sessions]

    # @staticmethod
    # def get_player_session_performance(player_id):
    #     try:
    #         session_player_ids = [sp.id for sp in SessionPlayer.query.filter(SessionPlayer.player_id == player_id).all()]
    #         print('session_player_ids are:', session_player_ids)
    #         shot_ids = [ss.shot_id for ss in SessionShot.query.filter(SessionShot.session_player_id == session_player_ids).all()]
    #
    #         print("shot_ids are:", shot_ids)
    #         ideal_angles = [CoachController.get_angle_comparison(shot_id) for shot_id in shot_ids]
    #         session_shot_ids = [ss.id for ss in SessionShot.query.filter(SessionShot.session_player_id._in(session_player_ids)).all()]
    #
    #         shotResults = ShotResult.query.filter(ShotResult.session_shot_id._in(session_shot_ids)).all()
    #
    #         return {"Results": [{'id': result.id, 'is_shot_correct': result.is_shot_correct,
    #                              'elbow_angle': result.elbow_angle, 'shoulder_inclination': result.shoulder_inclination,
    #                              'wrist_angle': result.wrist_angle, 'knee_angle': result.knee_angle,
    #                              'hip_angle': result.hip_angle, 'bat_hip_distance':
    #                                  result.bat_hip_distance, 'correct_angles': result.correct_angles,
    #                              'incorrect_angles':
    #                                  result.incorrect_angles, 'best_frame_path': result.best_frame_path} for result in
    #                             shotResults],
    #                 "Ideal Angles": ideal_angles}
    #     except Exception as exp:
    #         return {"Error": str(exp)}

    @staticmethod
    def get_player_session_performance(session_id):
        try:
            session_player_id = (SessionPlayer.query.filter(SessionPlayer.session_id == session_id).first()).id
            print("session_player_id is:", session_player_id)

            session_shot_id = (
                SessionShot.query.filter(SessionShot.session_player_id == session_player_id).first()).id
            print("session_shot_id is:", session_shot_id)
            shot_id = (SessionShot.query.filter(SessionShot.id == session_shot_id).first()).shot_id
            ideal_angles = CoachController.get_angle_comparison(shot_id)

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

