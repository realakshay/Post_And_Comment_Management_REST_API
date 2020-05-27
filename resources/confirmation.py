from flask_restful import Resource
from models.confirmation import ConfirmationModel
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