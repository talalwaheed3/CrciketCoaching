from ..config import db


class TeamCoach(db.Model):
    __tablename__ = "TeamCoach"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('Team.id'), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    team = db.relationship("Team", back_populates="team_Coach")
    user = db.relationship("User", back_populates="team_Coach")
