from ..config import db


class Shot(db.Model):
    __tablename__ = 'Shot'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))

    shot_ideal_angle = db.relationship('ShotIdealAngle', back_populates='shot')   # Done
    coach_angle = db.relationship('CoachAngle', back_populates='shot')   # Done
    session_Shot = db.relationship("SessionShot", back_populates="shot")   # Done
