import traceback

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.user import UserSchema
from libs.string import gettext

user_schema = UserSchema()


class UserRegister(Resource):

    @classmethod
    def post(cls):
        user_json = request.get_json()
        try:
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 401

        if UserModel.find_by_username(user_data.username):
            return {"Message": gettext("user_username_already_exist").format(user_data.username)}, 401

        if UserModel.find_by_email(user_data.email):
            return {"Message": gettext("user_email_already_exist").format(user_data.email)}, 401

        try:
            user_data.insert_in_db()
            confirmation = ConfirmationModel(user_data.id)
            confirmation.insert_in_db()
            user_data.send_confirmation_mail()
            return {"Message": gettext("user_registration_successful")}, 201

        except MailGunException as me:
            user_data.delete_from_db()
            return {"Message": gettext("user_email_sending_failed")}, 501

        except:
            traceback.print_exc()
            return {"Message": gettext("user_internal_server_error")}, 501
