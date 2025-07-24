from API.Model.Team import Team
from API.Model.TeamPlayer import TeamPlayer
from API.config import db
from API.Controller.UserController import UserController
from API.Model.TeamCoach import TeamCoach
from API.Model.User import User
from sqlalchemy import and_


class ManagerController:

    @staticmethod
    def add_team(team_name, players_list, coach_id):
        try:
            is_team_exist = Team.query.filter(Team.name == team_name).first()
            if is_team_exist:
                return {"result": f"{team_name} team already exists. "}
            team = Team(name=team_name)
            db.session.add(team)
            db.session.flush()

            team_coach = TeamCoach(team_id=team.id, coach_id=coach_id)
            db.session.add(team_coach)
            db.session.flush()
            UserController.change_availability(coach_id)

            for player_id in players_list:
                team_player = TeamPlayer(team_id=team.id, player_id=player_id)
                db.session.add(team_player)
                db.session.flush()
                UserController.change_availability(player_id)

            db.session.commit()

            return {"result": "success"}
        except Exception as exp:
            return {"result": f"request failed, error is:{exp}"}

    @staticmethod
    def add_user(name, role, username, password, experience, date_of_birth, contact_no, player_type=None, is_team_assigned="false", is_active="1"):
        check_user = User.query.filter(User.username == username).first()
        if check_user:
            return {"result": False}
        user = User(name=name, role=role, username=username, password=password, experience=experience, date_of_birth=date_of_birth,
                    contact_no=contact_no, is_team_assigned=is_team_assigned, type=player_type, is_active=is_active)
        try:
            db.session.add(user)
            db.session.commit()
            return {"value": True,
                    "result": f"{role} added successfully",
                    "coach_id": 2}
        except Exception as exp:
            return {"result": f"error while add {role} is:{exp}"}

    @staticmethod
    def list_all_users(role):
        try:
            if role == "player":
                result = (
                    db.session.query(User, Team.name.label("team_name"))
                    .outerjoin(TeamPlayer, User.id == TeamPlayer.player_id)  # Use outer join (LEFT JOIN)
                    .outerjoin(Team, Team.id == TeamPlayer.team_id)  # Use outer join (LEFT JOIN)
                    .filter(User.role == role)
                    .all()
                )
            else:
                result = (
                    db.session.query(User, Team.name.label("team_name"))
                    .outerjoin(TeamCoach, User.id == TeamCoach.coach_id)  # Use outer join (LEFT JOIN)
                    .outerjoin(Team, Team.id == TeamCoach.team_id)  # Use outer join (LEFT JOIN)
                    .filter(User.role == role)
                    .all()
                )
            users = [
                {
                    "id": user.id,
                    "name": user.name,
                    "role": user.role,
                    "username": user.username,
                    "password": user.password,
                    "experience": user.experience,
                    "date_of_birth": user.date_of_birth,
                    "contact_no": user.contact_no,
                    "type": user.type,
                    "team_name": team_name
                }
                for user, team_name in result
            ]

            return {f"{role}s": users}
        except Exception as exp:
            return {'error': {exp}}

    @staticmethod
    def list_all_users_by_is_assigned(role, availability):
        #
        # query = (
        #     db.session.query(User, Team.name.label("team_name"))
        #     .join(TeamPlayer, User.id == TeamPlayer.player_id)
        #     .join(Team, Team.id == TeamPlayer.team_id)
        #     .filter(User.is_team_assigned == availability, User.role == role)
        # )
        #
        # # Print the exact SQL query Flask is executing
        # print(str(query.statement.compile(db.engine, compile_kwargs={"literal_binds": True})))

        try:
            result = (
                db.session.query(User, Team.name.label("team_name"))
                .outerjoin(TeamPlayer, User.id == TeamPlayer.player_id)  # Use outer join (LEFT JOIN)
                .outerjoin(Team, Team.id == TeamPlayer.team_id)  # Use outer join (LEFT JOIN)
                .filter(User.is_team_assigned == availability, User.role == role)
                .all()
            )

            users = [
                {
                    "id": user.id,
                    "name": user.name,
                    "role": user.role,
                    "username": user.username,
                    "password": user.password,
                    "experience": user.experience,
                    "date_of_birth": user.date_of_birth,
                    "contact_no": user.contact_no,
                    "type": user.type,
                    "team_name": team_name
                }
                for user, team_name in result
            ]

            return {f"{role}s": users}
        except Exception as exp:
            return {'error': {exp}}

    @staticmethod
    def list_all_teams():
        try:
            teams = Team.query.all()
            all_teams = []
            for team in teams:
                players = ManagerController.list_all_players_by_team(team.id)
                coach = ManagerController.get_coach_by_team(team.id)
                all_teams.append({
                    "id": team.id,
                    "name": team.name,
                    "total_players": len(players) if players else 0,
                    "coach": coach,
                    "players": players
                })
            return {"Teams": all_teams}
        except Exception as exp:
            return {'error': {exp}}

    @staticmethod
    def list_all_players_by_team(team_id):
        team_players = TeamPlayer.query.filter(TeamPlayer.team_id == team_id).all()
        players_id = [player.player_id for player in team_players]
        if not players_id:
            return []

        players = User.query.filter(User.id.in_(players_id)).all()

        return [{"id": player.id, "name": player.name, "date_of_birth": player.date_of_birth, "contact_no": player.contact_no,
                 "experience": player.experience, 'type': player.type} for player in players]

    @staticmethod
    def get_coach_by_team(team_id):
        team_coach = TeamCoach.query.filter(TeamCoach.team_id == team_id).first()
        if not team_coach:
            return []
        coach = User.query.filter(User.id == team_coach.coach_id).first()
        return {"id": coach.id, "name": coach.name, "date_of_birth": coach.date_of_birth, "experience": coach.experience,
                "contact_no": coach.contact_no}

    @staticmethod
    def change_availability(id):
        user = User.query.filter(User.id == id).first()

        if user:
            if user.is_team_assigned == "false":
                user.is_team_assigned = "true"
            else:
                user.is_team_assigned = "false"
            db.session.commit()

    @staticmethod
    def add_player_in_team(team_id, list_of_players_ids):
        team = Team.query.filter(Team.id == team_id).first()
        if not team:
            return "team not found"
        for player_id in list_of_players_ids:
            teamplayer = TeamPlayer(player_id=player_id, team_id=team_id)
            db.session.add(teamplayer)
        db.session.commit()

    @staticmethod
    def remove_player_from_team(team_id, player_id):
        team = Team.query.filter(Team.id == team_id).first()
        if not team:
            return "team not found"
        teamplayer = TeamPlayer.query.filter(TeamPlayer.player_id == player_id).first()
        db.session.delete(teamplayer)
        db.session.commit()
