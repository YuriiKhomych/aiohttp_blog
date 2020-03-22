from marshmallow import Schema, fields, ValidationError, pre_load
# https://marshmallow.readthedocs.io/en/latest/examples.html#quotes-api-flask-sqlalchemy


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    body = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)


post_schema = PostSchema()
posts_schema = PostSchema(many=True)
