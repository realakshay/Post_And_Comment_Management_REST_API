from time import time
from db import db
from uuid import uuid4

CONFIRMATION_EXPIRATION_DELTA = 1800


class ConfirmationModel(db.Model):
    __tablename__ = "confirmations"

    id = db.Column(db.String(100), primary_key=True)
    is_confirmed = db.Column(db.Boolean, default=False)
    expired_at = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("UserModel")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.is_confirmed = False
        self.expired_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA

    @classmethod
    def find_by_id(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @property
    def expired(self) -> bool:
        return time() > self.expired_at

    def force_to_expire(self):
        if not self.expired:
            self.expired_at = int(time())
            self.insert_in_db()

    def insert_in_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()