from ..config import db


class Session(db.Model):
    __tablename__ = "Session"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=False)
    date = db.Column(db.String(10), nullable=False)
    session_from = db.Column(db.String(10), nullable=False)
    session_to = db.Column(db.String(10), nullable=False)
    venue = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(1), nullable=False)

    session_player = db.relationship("SessionPlayer", foreign_keys="SessionPlayer.session_id", back_populates="session")
    coach = db.relationship("User", foreign_keys=[coach_id], back_populates="session")






