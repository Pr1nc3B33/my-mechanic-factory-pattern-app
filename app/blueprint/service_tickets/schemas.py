from marshmallow import fields

from app.extensions import ma
from app.models import Service_Tickets


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanic_ids = fields.Method('get_mechanic_ids', dump_only=True)

    class Meta:
        model = Service_Tickets
        include_fk = True

    def get_mechanic_ids(self, obj):
        return [mechanic.id for mechanic in obj.mechanic]


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
