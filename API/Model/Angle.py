from ..config import db


class Angle(db.Model):
    __tablename__ = 'Angle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    angleLines = db.relationship("AngleLine", back_populates="angle")   # Done
    shot_ideal_angle = db.relationship("ShotIdealAngle", back_populates="angle")   # Done
    # coach_angle = db.relationship("CoachAngle", back_populates="angle")   # Done
