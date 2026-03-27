from app.extensions import ma
from app.models import Mechanics


class MechanicsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics


mechanic_schema = MechanicsSchema()
mechanics_schema = MechanicsSchema(many=True)
mechanic_login_schema = MechanicsSchema(only=['email', 'password'])
