import uuid

from sqlalchemy.orm import declarative_base, relationship, mapper
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, ForeignKey, Integer, Float, String

from allocation.domain import model

Base = declarative_base()

# Allocations = Table(
#     'Allocation',
#     Base.metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('order_line_id', Integer, ForeignKey('order_line.id')),
#     Column('product_id', Integer, ForeignKey('product.id'))
# )


# class OrderLines(Base):
#     __tablename__ = 'order_line'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     sku = Column(String(255))
#     quantity = Column(Integer, nullable=False)
#     order_id = Column(String(255))


class Products(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(255), unique=True)
    name = Column(String(255))
    description = Column(String(1023))


def start_mappers(engine=None):
    if(engine):
        Base.metadata.create_all(engine)
    mapper(model.Product, Products)
    # orderlines_mapper = mapper(model.OrderLine, OrderLines)
    # mapper(model.Product, Products, properties={
    #     '_allocations': relationship(orderlines_mapper, secondary=Allocations, collection_class=set,)
    # })
