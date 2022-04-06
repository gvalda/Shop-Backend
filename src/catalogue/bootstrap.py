from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from allocation.service_layer import unit_of_work
from allocation.adapters.orm import start_mappers
from allocation import config


def bootstrap():
    engine = create_engine(
        config.get_postgres_uri(),
        isolation_level='REPEATABLE READ'
    )
    start_mappers(engine)

    session_factory = sessionmaker(bind=engine)
    uow = unit_of_work.SqlAlchemyUnitOfWork(session_factory)
    return uow
