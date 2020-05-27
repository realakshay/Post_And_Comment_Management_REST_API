from ma import ma
from models.user import UserModel
from marshmallow import pre_dump


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        dump_only = ("id", "reg_date",)
        load_only = ("password",)
        include_fk = True

    # @pre_dump
    # def _pre_dump(self, user: UserModel):
    #     user.confirmation = [user.most_recent_confirmation]
    #     return user