

import os
from datetime import datetime
from datetime import timedelta
from twisted.internet.task import deferLater
from twisted.internet.threads import deferToThread

from kivy_garden.ebs.pdfplayer.widget import generate_pdf_images
from ebs.linuxnode.mediaplayer.manager import MediaPlayerBusy

from .base import EventManager


class WebResourceEventManager(EventManager):
    def _trigger_event(self, event):
        r = self._node.resource_manager.get(event.resource)
        if r.available:
            try:
                d = self._node.mediaview.play(content=r,
                                              duration=event.duration)
                d.addCallback(self._finish_event)
                self.log.info("Executed Event : {0}".format(event))
                self._current_event = event.eid
                self._current_event_resource = event.resource
            except MediaPlayerBusy as e:
                # self.log.warn("Media player busy for {event} : {e}",
                #               event=event, e=e.now_playing)
                return e.collision_count
        else:
            self.log.warn("Media not ready for {event}", event=event)
        self.remove(event.eid)
        self.prune()

    def _succeed_event(self, event):
        try:
            self._node.api_media_success([event])
        except NotImplementedError:
            self.log.warn("Node has no media event success reporter")

    def _preprocess_pdf(self, filepath):
        name = os.path.splitext(os.path.basename(filepath))[0]
        target = os.path.join(self._node.temp_dir, name)
        return deferToThread(generate_pdf_images, filepath, target, None)

    def _preprocess_resource(self, maybe_failure, resource):
        if os.path.splitext(resource.filename)[1] == '.pdf':
            self.preprocess_semaphore.run(
                self._preprocess_pdf, resource.filepath
            )

    def _fetch(self):
        self.log.debug("Triggering WebResource Fetch")
        session = self.db()
        try:
            results = self.db_get_events(session).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for e in results:
            if e.start_time - datetime.now() > timedelta(seconds=1200):
                break
            r = self._node.resource_manager.get(e.resource)
            d = self._node.resource_manager.prefetch(
                r, semaphore=self._node.http_semaphore_download
            )
            d.addCallback(self._preprocess_resource, r)
        self._fetch_task = deferLater(self._node.reactor, 600, self._fetch)

    def _fetch_scheduler(self):
        self._fetch()

    def _prefetch(self):
        self.log.debug("Triggering WebResource Prefetch")
        session = self.db()
        try:
            results = self.db_get_events(session).all()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        for e in results:
            if e.start_time - datetime.now() > timedelta(seconds=(3600 * 6)):
                break
            r = self._node.resource_manager.get(e.resource)
            self._node.resource_manager.prefetch(
                r, semaphore=self._node.http_semaphore_background
            )
        self._prefetch_task = deferLater(self._node.reactor, 3600, self._prefetch)

    def _prefetch_scheduler(self):
        self._prefetch()

    def start(self):
        super(WebResourceEventManager, self).start()
        self._fetch_scheduler()
        self._prefetch_scheduler()
