from ..config import db


class AngleLine(db.Model):
    __tablename__ = "AngleLine"
    id = db.Column(db.Integer, primary_key=True)
    angle_id = db.Column(db.Integer, db.ForeignKey("Angle.id"), nullable=False)
    line_id1 = db.Column(db.Integer, db.ForeignKey("JointLine.id"), nullable=False)
    line_id2 = db.Column(db.Integer, db.ForeignKey("JointLine.id"), nullable=False)

    angle = db.relationship("Angle", back_populates="angleLines")

    jointLine_line1 = db.relationship(
        "JointLine",
        foreign_keys=[line_id1],
        back_populates="angleLine_as_line1"
    )    # Done
    jointLine_line2 = db.relationship(
        "JointLine",
        foreign_keys=[line_id2],
        back_populates="angleLine_as_line2"
    )    # Done

    # relationship_var_name = db.relationship("table name", back_populates="relationship_var_name of mapping table")
