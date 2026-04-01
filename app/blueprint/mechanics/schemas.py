from app.extensions import ma
from app.models import Mechanics
from marshmallow import fields


class MechanicsSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(load_only=True)

    class Meta:
        model = Mechanics


mechanic_schema = MechanicsSchema()
mechanics_schema = MechanicsSchema(many=True)
mechanic_login_schema = MechanicsSchema(only=['email', 'password'])
