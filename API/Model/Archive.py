from API.config import db


class Archive(db.Model):
    __tablename__ = "Archive"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)

    # archive_user = db.relationship("User", foreign_keys=[user_id], back_populates="archive")
    user = db.relationship("User", backref="archives")  # Change back_populates to backref