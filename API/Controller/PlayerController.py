from . import Session
from . import SessionPlayer
from . import ShotResult
from . import SessionShot
from API.config import db
from ..Model.Team import Team
from ..Model.TeamCoach import TeamCoach
from ..Model.TeamPlayer import TeamPlayer
from ..Model.User import User


class PlayerController:

    # @staticmethod
    # def get_team(player_id):
    #     team_player = TeamPlayer.query.filter(TeamPlayer.player_id == player_id).first()
    #     if not team_player:
    #         return []
    #     team = Team.query.filter(Team.id == team_player.team_id).first()
    #     if not team:
    #         return []
    #     team_coach = (TeamCoach.query.filter(TeamCoach.team_id == team.id).first()).coach_id
    #     team =
    #
    #     return {"playerController": [{"id": team.id, "team_name": team.name, "team_players": players}]}

    @staticmethod
    def get_joined_sessions(player_id):
        try:
            allSessionPlayersIds = SessionPlayer.query.filter(SessionPlayer.player_id == player_id).all()
            sessionsIds = [sessionPlayer.session_id for sessionPlayer in allSessionPlayersIds]
            print("sessionsIds are:", sessionsIds)
            sessions = Session.query.filter(Session.id.in_(sessionsIds), Session.status == '0').all()
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

    @staticmethod
    def get_performance(player_id, session_id):
        session_player = SessionPlayer.query.filter(SessionPlayer.player_id == player_id
                                                    and SessionPlayer.session_id == session_id).first()
        session_shot = SessionShot.query.filter(SessionShot.session_player_id == session_player.id).first()
        shot_result = ShotResult.query.filter(ShotResult.session_shot_id == session_shot.id).all()
        return {"id": shot_result.id, "session_shot_id": shot_result.session_shot_id,
                "is_shot_correct": shot_result.is_shot_correct, "left_arm_angle": shot_result.left_arm_angle,
                "right_arm_angle": shot_result.right_arm_angle, "left_leg_angle": shot_result.left_leg_angle,
                "right_leg_angle": shot_result.right_leg_angle, "correct_angles": shot_result.correct_angles,
                "incorrect_angles": shot_result.incorrect_angles}

