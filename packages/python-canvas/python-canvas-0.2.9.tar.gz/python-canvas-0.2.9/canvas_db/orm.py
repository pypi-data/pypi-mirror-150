from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def get_session(config):
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/canvas_production'.format(
        config.user, config.password, config.host), pool_size=10, max_overflow=-1)
    conn = engine.connect()

    session_factory = sessionmaker(bind=engine)
    return session_factory


def get_base():
    return Base
