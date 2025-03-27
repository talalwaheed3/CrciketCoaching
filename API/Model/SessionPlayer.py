from ..config import db


class SessionPlayer(db.Model):
    __tablename__ = "SessionPlayer"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('Session.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    session = db.relationship("Session", foreign_keys=[session_id], back_populates="session_player")
    player = db.relationship("User", foreign_keys=[player_id], back_populates="session_Player")
    session_Shot = db.relationship("SessionShot", back_populates="session_player")



