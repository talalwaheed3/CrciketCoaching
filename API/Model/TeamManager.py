from ..config import db


class TeamManager(db.Model):
    __tablename__ = "TeamManager"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('Team.id'), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    team = db.relationship("Team", back_populates="team_Manager")
    user = db.relationship("User", back_populates="team_Manager")
