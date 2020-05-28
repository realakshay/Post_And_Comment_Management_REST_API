import traceback

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_refresh_token, create_access_token, jwt_required, get_jwt_identity, get_raw_jwt
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash

from blacklist import BLACKLIST
from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.user import UserSchema
from libs.string import gettext

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserRegister(Resource):

    @classmethod
    def post(cls):
        user_json = request.get_json()
        try:
            user_data = user_schema.load(user_json)
            user_data.password = generate_password_hash(user_data.password)
            print(user_data.password)
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


class User(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": gettext("user_id_not_found_error").format(user_id)}, 401
        return user_schema.dump(user), 201

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": gettext("user_id_not_found_error").format(user_id)}, 401
        user.delete_from_db()
        return {"Message": gettext("user_deleted_successful").format(user_id)}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        user_json = request.get_json()
        try:
            user_data = user_schema.load(user_json, partial=("email",))
        except ValidationError as err:
            return {"Message": err.messages}, 401

        user = UserModel.find_by_username(user_data.username)
        if user and check_password_hash(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.is_confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 201
            return {"Message": gettext("user_not_confirmed_error")}, 401
        return {"Message": gettext("user_invalid_credential_error")}, 401


class TokenRefresh(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        refresh_token = create_access_token(identity=user_id, fresh=False)
        return {"refresh_token": refresh_token}, 201


class UserLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"Message": gettext("user_logout_successful")}, 201


class AllUsers(Resource):

    @classmethod
    @jwt_required
    def get(cls):
        return users_schema.dump(UserModel.find_all())