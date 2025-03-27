from ..config import db


class Joint(db.Model):
    __tablename__ = 'Joint'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))

    jointLine_joint1 = db.relationship("JointLine",  foreign_keys="JointLine.joint_id1", back_populates="joint1")    # Done
    jointLine_joint2 = db.relationship("JointLine",  foreign_keys="JointLine.joint_id2", back_populates="joint2")    # Done
