from API.Model.Session import Session
from API.Model.SessionPlayer import SessionPlayer
from API.Model.Team import Team
from API.Model.TeamPlayer import TeamPlayer
from API.Model.TeamCoach import TeamCoach
from API.Model.TeamManager import TeamManager
from API.Model.User import User
from API.config import db


class AdminController:

    @staticmethod
    def create_team(name, manager_id):
        team = Team(name=name)
        db.session.add(team)
        team_id = team.id

        team_manager = TeamManager(team_id=team_id, manager_id=manager_id)
        AdminController.change_availability(manager_id)
        db.session.add(team_manager)
        db.session.commit()

        return {"value": "True"}

    @staticmethod
    def get_user_by_role(role):
        user = User.query.filter(User.role == role, User.validity == "true").order_by(User.id).first()

        return user.id if user else "not available"

    @staticmethod
    def get_multiple_users_by_role(role, total_users):
        users = User.query.filter(User.role == role, User.validity == "true").order_by(User.id).limit(total_users).all()
        user_ids = []
        if users:
            for u in users:
                user_ids.append(u.id)
            return user_ids
        else:
            return "not available"

    @staticmethod
    def change_availability(id):
        user = User.query.filter(User.id == id).first()

        if user:
            if user.validity == "false":
                user.validity = "true"
            else:
                user.validity = "false"
            db.session.commit()

    @staticmethod
    def delete_team(name):
        team = Team.query.filter(Team.name == name).first()

        team_manager = TeamManager.query.filter(TeamManager.team_id == team.id).first()
        if team_manager:
            AdminController.change_availability(team_manager.manager_id)
            db.session.delete(team_manager)
            db.session.commit()

        db.session.delete(team)
        db.session.commit()

        return f"Teams with name: {name} deleted successfully"

    @staticmethod
    def update_team(name):

        db.session.commit()

    @staticmethod
    def list_all_teams():
        teams = Team.query.all()
        return [{"id": team.id, "name": team.name}
                for team in teams]

    @staticmethod
    def get_team(team_id):
        team = Team.query.filter(Team.id == team_id).first()
        return {"id": team.id, "name": team.name} if team else None

    @staticmethod
    def list_all_players():
        players = User.query.filter(User.role == "player").all()
        return [{"id": player.id, "name": player.name, 'role': player.role, 'username': player.username,
                 'password': player.password, 'experience': player.experience, 'age': player.age,
                 'contact_no': player.contact_no, 'type': player.type} for player in players]

    @staticmethod
    def list_all_players_by_team(team_id):
        team_players = TeamPlayer.query.filter(TeamPlayer.team_id == team_id).all()
        players_id = [player.player_id for player in team_players]
        if not players_id:
            return {"Success": False, "players": []}

        players = User.query.filter(User.id.in_(players_id)).all()

        return {"Success": True,
                "players": [{"id": player.id, "name": player.name, 'type': player.type} for player in players]}

    @staticmethod
    def list_all_coaches():
        coaches = User.query.filter(User.role == "coach").all()
        return {"Success": True, "Coaches": [{"id": coach.id, "name": coach.name, 'role': coach.role,
                                              'username': coach.username, 'password': coach.password,
                                              'experience': coach.experience,
                                              'age': coach.age, 'contact_no': coach.contact_no, 'type': coach.type}
                                             for coach in coaches]} if coaches else {"Success": False, 'coaches': []}

    @staticmethod
    def get_coach_by_team(team_id):
        team_coach = TeamCoach.query.filter(TeamCoach.team_id == team_id).first()
        if not team_coach:
            return {"Success": False, "Coach": []}
        coach = User.query.filter(User.id == team_coach.coach_id).first()
        return {"Success": True, "Coach": {"id": coach.id, "name": coach.name, 'role': coach.role,
                                             'username': coach.username, 'password': coach.password,
                                             'experience': coach.experience,
                                             'age': coach.age, 'contact_no': coach.contact_no, 'type': coach.type}
                }

    @staticmethod
    def list_all_managers():
        managers = User.query.filter(User.role == "manager").all()
        return {"Success": True, "Coaches": [{"id": manager.id, "name": manager.name, 'role': manager.role,
                                              'username': manager.username, 'password': manager.password,
                                              'experience': manager.experience,
                                              'age': manager.age, 'contact_no': manager.contact_no, 'type': manager.type}
                                             for manager in managers]} if managers else {"Success": False, 'coaches': []}

    @staticmethod
    def get_manager_by_team(team_id):
        team_manager = TeamManager.query.filter(TeamManager.team_id == team_id).first()
        if not team_manager:
            return {"Success": False, "Manager": []}
        manager = User.query.filter(User.id == team_manager.manager_id).first()
        return {"Success": True, "Manager": {"id": manager.id, "name": manager.name, 'role': manager.role,
                                             'username': manager.username, 'password': manager.password,
                                             'experience': manager.experience,
                                             'age': manager.age, 'contact_no': manager.contact_no, 'type': manager.type}
                }


