from API.config import db


class Team(db.Model):
    __tablename__ = 'Team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    team_Coach = db.relationship("TeamCoach", back_populates="team")
    team_Player = db.relationship("TeamPlayer", back_populates="team")
    team_Manager = db.relationship("TeamManager", back_populates="team")






