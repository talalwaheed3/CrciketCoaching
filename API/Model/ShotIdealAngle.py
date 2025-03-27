from API.config import db


class ShotIdealAngle(db.Model):
    __tablename__ = 'ShotIdealAngle'
    id = db.Column(db.Integer, primary_key=True)
    angle_name_id = db.Column(db.Integer, db.ForeignKey("Angle.id"), nullable=False)
    shot_id = db.Column(db.Integer, db.ForeignKey("Shot.id"), nullable=False)
    angle_from = db.Column(db.Integer)
    angle_to = db.Column(db.Integer)

    angle = db.relationship('Angle', back_populates='shot_ideal_angle')   # Done
    shot = db.relationship('Shot', back_populates='shot_ideal_angle')   # Done
