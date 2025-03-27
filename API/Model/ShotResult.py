from ..config import db


class ShotResult(db.Model):
    __tablename__ = "ShotResult"
    id = db.Column(db.Integer, primary_key=True)
    session_shot_id = db.Column(db.Integer, db.ForeignKey('SessionShot.id'), nullable=False)
    is_shot_correct = db.Column(db.String(10), nullable=False)
    left_arm_angle = db.Column(db.Integer, nullable=False)
    right_arm_angle = db.Column(db.Integer, nullable=False)
    left_leg_angle = db.Column(db.Integer, nullable=False)
    right_leg_angle = db.Column(db.Integer, nullable=False)
    correct_angles = db.Column(db.String(60), nullable=False)
    incorrect_angles = db.Column(db.String(60), nullable=False)

    session_shot = db.relationship("SessionShot", back_populates="shot_result")     # Done
