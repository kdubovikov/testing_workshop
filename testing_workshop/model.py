from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)

    def __repr__(self):
        return "<Metric(name='%s', value='%s')>" % (
            self.name, self.value)

def create_db():
    Base.metadata.create_all(engine)
