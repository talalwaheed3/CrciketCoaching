from API.config import db


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.String(12), nullable=False)
    contact_no = db.Column(db.String(20), nullable=False)
    is_team_assigned = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(25), nullable=True)
    is_active = db.Column(db.String(1), nullable=False)

    session = db.relationship("Session", foreign_keys="Session.coach_id", back_populates="coach")   # Done

    session_Player = db.relationship("SessionPlayer", foreign_keys="SessionPlayer.player_id", back_populates="player")  # Done
    team_Coach = db.relationship("TeamCoach", back_populates="user")        # Done
    team_Manager = db.relationship("TeamManager", back_populates="user")    # Done
    team_Player = db.relationship("TeamPlayer", back_populates="user")      # Done
    coach_angle = db.relationship("CoachAngle", back_populates="coach")      # Done
    # archive = db.relationship("Archive", foreign_keys="Archive.user_id", back_populates="archive_user")
