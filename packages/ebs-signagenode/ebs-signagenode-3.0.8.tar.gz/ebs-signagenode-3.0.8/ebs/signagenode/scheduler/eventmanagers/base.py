

import os
from twisted import logger
from datetime import datetime
from datetime import timedelta
from twisted.internet.task import deferLater
from twisted.internet.defer import DeferredSemaphore

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from ebs.linuxnode.core.constants import WEBRESOURCE
from ebs.linuxnode.core.constants import TEXT

from ..events import Event
from ..model import TextEventsModel
from ..model import WebResourceEventsModel
from ..model import metadata


class EventManager(object):
    def __init__(self, node, emid):
        self._emid = emid
        self._node = node
        self._db_engine = None
        self._db = None
        self._db_dir = None
        self._execute_task = None
        self._current_event = None
        self._current_event_resource = None
        self._preprocess_semaphore = None
        self._log = None
        _ = self.db

    @property
    def emid(self):
        return self._emid

    @property
    def log(self):
        if not self._log:
            self._log = logger.Logger(namespace="em.{0}".format(self.emid), source=self)
        return self._log

    @property
    def preprocess_semaphore(self):
        if self._preprocess_semaphore is None:
            self._preprocess_semaphore = DeferredSemaphore(1)
        return self._preprocess_semaphore

    def insert(self, eid, **kwargs):
        event = Event(self, eid, **kwargs)
        event.commit()

    def remove(self, eid):
        session = self.db()
        # print("Trying to remove {0} from edb".format(eid))
        try:
            try:
                eobj = session.query(self.db_model).filter_by(eid=eid).one()
            except NoResultFound:
                return False
            # print("Committing edel")
            session.delete(eobj)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return True

    def _pointers(self, cond, resource=None, follow=False):
        session = self.db()
        try:
            r = self.db_get_events(session, resource=resource).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        e = None
        l = None
        for e in r:
            if l and cond(l, e):
                break
            l = e
        if l:
            if not follow:
                return Event(self, l.eid)
            else:
                if e:
                    ne = Event(self, e.eid)
                else:
                    ne = None
                return Event(self, l.eid), ne
        if follow:
            return None, None
        else:
            return None

    def previous(self, resource=None, follow=False):
        return self._pointers(
            lambda l, e: e.start_time >= datetime.now(),
            resource=resource, follow=follow
        )

    def next(self, resource=None, follow=False):
        return self._pointers(
            lambda l, e: l.start_time >= datetime.now(),
            resource=resource, follow=follow
        )

    def get(self, eid):
        return Event(self, eid)

    def prune(self):
        # TODO This doesn't work!
        # with self.db as db:
        #     r = db[self.db_table_name].find(start_time={'lt': datetime.now()})
        #     for result in r:
        #         print("Removing {0}".format(r))
        #         self.remove(result['eid'])
        session = self.db()
        try:
            results = self.db_get_events(session).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        for result in results:
            if result.start_time >= datetime.now():
                break
            self.log.warn("Pruning missed event {event}", event=result)
            self.remove(result.eid)

    def render(self):
        session = self.db()
        try:
            results = self.db_get_events(session).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for result in results:
            print(Event(self, result.eid))

    def db_get_events(self, session, resource=None):
        q = session.query(self.db_model)
        if resource:
            q = q.filter(
                self.db_model.resource == resource
            )
        q = q.order_by(self.db_model.start_time)
        return q

    @property
    def db_model(self):
        if self._emid == WEBRESOURCE:
            return WebResourceEventsModel
        elif self._emid == TEXT:
            return TextEventsModel

    @property
    def db(self):
        if self._db is None:
            self._db_engine = create_engine(self.db_url)
            metadata.create_all(self._db_engine)
            self._db = sessionmaker(expire_on_commit=False)
            self._db.configure(bind=self._db_engine)
        return self._db

    @property
    def db_url(self):
        return 'sqlite:///{0}'.format(os.path.join(self.db_dir, 'events.db'))

    @property
    def db_dir(self):
        return self._node.db_dir

    @property
    def current_event(self):
        return self._current_event

    @property
    def current_event_resource(self):
        return self._current_event_resource

    def _trigger_event(self, event):
        raise NotImplementedError

    def _finish_event(self, forced):
        if forced:
            self.log.info("Event {eid} was force stopped.",
                          eid=self._current_event)
        else:
            self.log.info("Successfully finished event {eid}",
                          eid=self._current_event)
            self._succeed_event(self._current_event)
        self._current_event = None
        self._current_event_resource = None

    def _succeed_event(self, event):
        raise NotImplementedError

    def _event_scheduler(self):
        event = None
        nevent = None
        le, ne = self.previous(follow=True)
        if le:
            ltd = datetime.now() - le.start_time
            # self.log.debug("S {emid} LTD {ltd}",
            #                ltd=ltd, emid=self._emid)
            if abs(ltd) < timedelta(seconds=3):
                event = le
                nevent = ne
        if not event:
            ne, nne = self.next(follow=True)
            if ne:
                ntd = ne.start_time - datetime.now()
                # self.log.debug("S {emid} NTD {ntd}",
                #                ntd=ntd, emid=self._emid)
                if abs(ntd) < timedelta(seconds=3):
                    event = ne
                    nevent = nne
        if event:
            retry = self._trigger_event(event)
            if retry:
                self._execute_task = deferLater(self._node.reactor, 0.1,
                                                self._event_scheduler)
                return
        self._execute_task = self._event_scheduler_hop(nevent)

    def _event_scheduler_hop(self, next_event=None):
        if not next_event:
            next_event = self.next()
        if not next_event:
            next_start = timedelta(seconds=60)
        else:
            next_start = next_event.start_time - datetime.now()
            # print("Next Start : ", next_start)
            if not next_event or next_start < timedelta(0):
                next_start = timedelta(seconds=60)
            elif next_start > timedelta(seconds=60):
                next_start = timedelta(seconds=60)
        self.log.debug("SCHED {emid} HOP {ns}", emid=self._emid,
                       ns=next_start.seconds)
        return deferLater(self._node.reactor, next_start.seconds,
                          self._event_scheduler)

    def start(self):
        self.log.info("Starting Event Manager {emid} of {name}",
                      emid=self._emid, name=self.__class__.__name__)
        self._event_scheduler()
