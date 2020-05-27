import traceback
from time import time

from flask_restful import Resource

from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema
from libs.string import gettext

confirmation_schema = ConfirmationSchema()


class Confirmation(Resource):

    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"Message": gettext("confirmation_token_not_found")}
        if confirmation.expired:
            return {"Message": gettext("confirmation_token_expired")}
        if confirmation.is_confirmed:
            return {"Message": gettext("confirmation_already_confirmed")}

        confirmation.is_confirmed = True
        confirmation.insert_in_db()
        return {"Message": gettext("confirmation_successful")}


class ConfirmationByUser(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": gettext("confirmation_user_not_found").format(user_id)}
        return (
            {
                "current time": int(time()),
                "confirmation": [
                    confirmation_schema.dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expired_at)
                ],
            },
            200,
        )

    @classmethod
    def post(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"Message": gettext("confirmation_user_not_found").format(user_id)}, 401
        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.is_confirmed:
                    return {"Message": gettext("confirmation_already_confirmed")}, 401
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.insert_in_db()
            user.send_confirmation_mail()
            return {"Message": gettext("confirmation_mail_resend_successful")}, 201

        except MailGunException as me:
            return {"Message": str(me)}, 501

        except:
            traceback.print_exc()
            return {"Message": gettext("confirmation_mail_resend_failed")}, 401
