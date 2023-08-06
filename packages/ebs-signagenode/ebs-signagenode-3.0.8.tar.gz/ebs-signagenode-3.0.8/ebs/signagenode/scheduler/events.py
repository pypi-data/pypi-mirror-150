

import os
from datetime import datetime
from six.moves.urllib.parse import urlparse
from sqlalchemy.orm.exc import NoResultFound

from ebs.linuxnode.core.constants import WEBRESOURCE
from ebs.linuxnode.core.constants import TEXT


class Event(object):
    def __init__(self, manager, eid, etype=None, resource=None,
                 start_time=None, duration=None):
        self._manager = manager
        self._eid = eid

        self._etype = None
        self.etype = etype

        self._resource = None
        self.resource = resource

        self._start_time = None
        self.start_time = start_time

        self._duration = None
        self.duration = duration
        if not self._etype:
            self.load()

    @property
    def eid(self):
        return self._eid

    @property
    def etype(self):
        return self._etype

    @etype.setter
    def etype(self, value):
        if value not in [None, WEBRESOURCE, TEXT]:
            raise ValueError
        self._etype = value

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, value):
        if self.etype == WEBRESOURCE:
            self._resource = os.path.basename(urlparse(value).path)
        elif self.etype == TEXT:
            self._resource = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        if not value:
            return
        if isinstance(value, datetime):
            self._start_time = value
        else:
            self._start_time = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    @property
    def duration(self):
        return self._duration or None

    @duration.setter
    def duration(self, value):
        self._duration = int(value) if value else None

    def commit(self):
        session = self._manager.db()
        try:
            try:
                eobj = session.query(self._db_model).filter_by(eid=self.eid).one()
            except NoResultFound:
                eobj = self._db_model()
                eobj.eid = self.eid

            eobj.etype = self._etype
            eobj.resource = self.resource
            eobj.start_time = self.start_time
            eobj.duration = self.duration

            session.add(eobj)
            session.flush()
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def load(self):
        session = self._manager.db()
        try:
            eobj = session.query(self._db_model).filter_by(eid=self._eid).one()
            self.etype = eobj.etype
            self.resource = eobj.resource
            self._start_time = eobj.start_time
            self.duration = eobj.duration
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @property
    def _db_model(self):
        return self._manager.db_model

    def __repr__(self):
        return "{0:3} {2} {3:.2f} {1}".format(
            self.eid, self.resource, self.etype,
            (self.start_time - datetime.now()).total_seconds()
        )
