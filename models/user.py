import datetime
import os
from typing import List

import requests
from flask import request, url_for
from requests import Response

from db import db
from models.confirmation import ConfirmationModel

MY_DOMAIN_NAME = os.environ.get('MY_DOMAIN_NAME')
MY_API_KEY = os.environ.get('MY_API_KEY')
FROM_EMAIL = os.environ.get('FROM_EMAIL')
FROM_TITLE = "Stores REST API"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    confirmation = db.relationship("ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan")

    def insert_in_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id: int) -> "UserModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> List:
        return cls.query.all()

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(db.desc(ConfirmationModel.expired_at)).first()

    def send_confirmation_mail(self) -> Response:
        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.most_recent_confirmation.id)
    
        requests.post(
            f"https://api.mailgun.net/v3/{MY_DOMAIN_NAME}/messages",
            auth=("api", MY_API_KEY),
            data={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": self.email,
                "subject": "Registration confirmation",
                "text": f"Please click the link to confirm your registration : {link}"
            }
        )