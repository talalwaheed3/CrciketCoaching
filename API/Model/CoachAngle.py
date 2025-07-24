from API.config import db


class CoachAngle(db.Model):
    __tablename__ = 'CoachAngle'
    id = db.Column(db.Integer, primary_key=True)
    coach_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    shot_id = db.Column(db.Integer, db.ForeignKey("Shot.id"), nullable=False)
    # angle_name_id = db.Column(db.Integer, db.ForeignKey("Angle.id"), nullable=False)
    angle_name = db.Column(db.String(30), nullable=False)
    angle_from = db.Column(db.Integer)
    angle_to = db.Column(db.Integer)

    coach = db.relationship('User', back_populates='coach_angle')
    # angle = db.relationship('Angle', back_populates='coach_angle')   # Done
    shot = db.relationship('Shot', back_populates='coach_angle')   # Done
