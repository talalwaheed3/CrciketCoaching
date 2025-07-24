from ..config import db


class ShotResult(db.Model):
    __tablename__ = "ShotResult"
    id = db.Column(db.Integer, primary_key=True)
    session_shot_id = db.Column(db.Integer, db.ForeignKey('SessionShot.id'), nullable=False)
    is_shot_correct = db.Column(db.Boolean, nullable=False)
    elbow_angle = db.Column(db.Integer, nullable=False)
    shoulder_inclination = db.Column(db.Integer, nullable=False)
    wrist_angle = db.Column(db.Integer, nullable=False)
    hip_angle = db.Column(db.Integer, nullable=False)
    knee_angle = db.Column(db.Integer, nullable=False)
    bat_hip_distance = db.Column(db.Integer, nullable=False)
    correct_angles = db.Column(db.String(100), nullable=True)
    incorrect_angles = db.Column(db.String(100), nullable=True)
    best_frame_path = db.Column(db.String(250), nullable=True)

    session_shot = db.relationship("SessionShot", back_populates="shot_result")     # Done
