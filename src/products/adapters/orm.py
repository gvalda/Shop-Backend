from sqlalchemy.orm import declarative_base, relationship, mapper
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Table, Column, ForeignKey, Integer, Float, String

from products.domain import model

Base = declarative_base()


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
