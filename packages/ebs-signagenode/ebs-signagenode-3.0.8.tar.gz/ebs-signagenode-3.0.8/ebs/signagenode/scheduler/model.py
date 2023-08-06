

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class WebResourceEventsModel(Base):
    __tablename__ = 'events_1'

    id = Column(Integer, primary_key=True)
    eid = Column(Text, unique=True, index=True)
    etype = Column(Integer)
    resource = Column(Text, index=True)
    start_time = Column(DateTime, index=True)
    duration = Column(Text)

    def __repr__(self):
        return "{0:3} {2} {3:.2f} {1}".format(
            self.eid, self.resource, self.etype,
            (self.start_time - datetime.now()).total_seconds()
        )


class TextEventsModel(Base):
    __tablename__ = 'events_2'

    id = Column(Integer, primary_key=True)
    eid = Column(Text, unique=True, index=True)
    etype = Column(Integer)
    resource = Column(Text)
    start_time = Column(DateTime, index=True)
    duration = Column(Integer)

    def __repr__(self):
        return "{0:3} {2} {3:.2f} {1}".format(
            self.eid, self.resource, self.etype,
            (self.start_time - datetime.now()).total_seconds()
        )
