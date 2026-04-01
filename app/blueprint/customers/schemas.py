from app.models import Customer
from app.extensions import ma
from marshmallow import fields



class CustomerSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(load_only=True)

    class Meta:
        model = Customer #using the SQLAlchemy model to create fields used in serialization, deserialization, and validation   

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True) #variant that allows for the serialization of many Users,
login_schema = CustomerSchema(only=['email', 'password'])