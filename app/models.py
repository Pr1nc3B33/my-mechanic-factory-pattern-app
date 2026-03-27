from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List





class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


service_mechanic = db.Table(
    'service_mechanic',
    Base.metadata,
    db.Column('ticket_id', db.Integer, db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanics.id'))
)

class Customer(Base):
    __tablename__ = 'customer'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

    
    service: Mapped[List['Service_Tickets']] = db.relationship(back_populates='customer')
    
class Ticket_Inventory(Base):
    __tablename__ = 'ticket_inventory'

    ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_tickets.id'), primary_key=True)
    inventory_id: Mapped[int] = mapped_column(db.ForeignKey('inventory.id'), primary_key=True)
    quantity: Mapped[int] = mapped_column(db.Integer, default=1)

    ticket: Mapped['Service_Tickets'] = db.relationship(back_populates='inventory_items')
    inventory: Mapped['Inventory'] = db.relationship(back_populates='ticket_items')


class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

    ticket_items: Mapped[List['Ticket_Inventory']] = db.relationship(back_populates='inventory')


class Service_Tickets(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'))
    service_date: Mapped[date] = mapped_column(db.Date)
    service_type: Mapped[str] = mapped_column(db.String(100))
    vin: Mapped[str] = mapped_column(db.String(17))
    
    customer: Mapped['Customer'] = db.relationship(back_populates='service')
    mechanic: Mapped[List['Mechanics']] = db.relationship('Mechanics', secondary=service_mechanic, back_populates='service')
    inventory_items: Mapped[List['Ticket_Inventory']] = db.relationship(back_populates='ticket')
    
    
class Mechanics(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20))
    salary: Mapped[float] = mapped_column(db.Float)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)

    service: Mapped[List['Service_Tickets']] = db.relationship('Service_Tickets', secondary=service_mechanic, back_populates='mechanic')
    