from ..config import db


class SessionShot(db.Model):
    __tablename__ = "SessionShot"
    id = db.Column(db.Integer, primary_key=True)
    session_player_id = db.Column(db.Integer, db.ForeignKey('SessionPlayer.id'), nullable=False)
    shot_id = db.Column(db.Integer, db.ForeignKey('Shot.id'), nullable=False)

    session_player = db.relationship("SessionPlayer", back_populates="session_Shot")   # Done
    shot = db.relationship("Shot", back_populates="session_Shot")   # Done
    shot_result = db.relationship("ShotResult", back_populates="session_shot")  # Done
