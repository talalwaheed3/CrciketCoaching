from .AngleLine import AngleLine
from ..config import db


class JointLine(db.Model):
    __tablename__ = 'JointLine'
    id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(30))
    joint_id1 = db.Column(db.Integer, db.ForeignKey('Joint.id'), nullable=False)
    joint_id2 = db.Column(db.Integer, db.ForeignKey('Joint.id'), nullable=False)

    joint1 = db.relationship("Joint", foreign_keys=[joint_id1], back_populates="jointLine_joint1")    # Done
    joint2 = db.relationship("Joint", foreign_keys=[joint_id2], back_populates="jointLine_joint2")    # Done

    angleLine_as_line1 = db.relationship(
        'AngleLine',
        foreign_keys="AngleLine.line_id1",
        back_populates='jointLine_line1'
    )    # Done
    angleLine_as_line2 = db.relationship(
        'AngleLine',
        foreign_keys="AngleLine.line_id2",
        back_populates='jointLine_line2'
    )    # Done


# from ..config import db
#
#
# class JointLine(db.Model):
#     __tablename__ = 'JointLine'
#     id = db.Column(db.Integer, primary_key=True)
#     line_name = db.Column(db.String(30))
#     joint_id1 = db.Column(db.Integer, db.ForeignKey('Joint.id'), nullable=False)
#     joint_id2 = db.Column(db.Integer, db.ForeignKey('Joint.id'), nullable=False)
#
#     # Relationships with Joint table
#     joint1 = db.relationship("Joint", foreign_keys=[joint_id1], back_populates="jointLine_joint1")
#     joint2 = db.relationship("Joint", foreign_keys=[joint_id2], back_populates="jointLine_joint2")
#
#     # Relationships with AngleLine
#     angleLines_as_line1 = db.relationship(
#         "AngleLine",
#         foreign_keys="AngleLine.line_id1",
#         back_populates="jointLine_line1"
#     )
#     angleLines_as_line2 = db.relationship(
#         "AngleLine",
#         foreign_keys="AngleLine.line_id2",
#         back_populates="jointLine_line2"
#     )
