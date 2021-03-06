from ma import ma
from models.comment import CommentModel


class CommentSchema(ma.ModelSchema):
    class Meta:
        model = CommentModel
        dump_only = ("id",)
        load_only = ("posts","user",)
        include_fk = True