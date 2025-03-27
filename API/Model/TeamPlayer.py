from ..config import db


class TeamPlayer(db.Model):
    __tablename__ = "TeamPlayer"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('Team.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    team = db.relationship("Team", back_populates="team_Player")
    user = db.relationship("User", back_populates="team_Player")
