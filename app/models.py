
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
    
    service: Mapped[List['Service_Tickets']] = db.relationship(back_populates='customer')
    
class Service_Tickets(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'))
    service_date: Mapped[date] = mapped_column(db.Date)
    service_type: Mapped[str] = mapped_column(db.String(100))
    vin: Mapped[str] = mapped_column(db.String(17))
    
    customer: Mapped['Customer'] = db.relationship(back_populates='service')
    mechanic: Mapped[List['Mechanics']] = db.relationship('Mechanics', secondary=service_mechanic, back_populates='service')
    
    
class Mechanics(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(db.String(255), nullable =False)
    email: Mapped[str] = mapped_column(db.String(360), nullable = False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20))
    salary: Mapped[int] = mapped_column(db.Float)   
    
    service: Mapped[List['Service_Tickets']] = db.relationship('Service_Tickets', secondary=service_mechanic, back_populates='mechanic')
    