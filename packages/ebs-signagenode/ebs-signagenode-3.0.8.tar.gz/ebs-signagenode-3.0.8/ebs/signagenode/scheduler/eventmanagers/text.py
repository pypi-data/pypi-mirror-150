

from .base import EventManager
from ebs.linuxnode.gui.kivy.marquee.mixin import MarqueeBusy


class TextEventManager(EventManager):
    def _trigger_event(self, event):
        try:
            d = self._node.marquee_play(text=event.resource,
                                        duration=event.duration)
            d.addCallback(self._finish_event)
            self.log.info("Executed Event : {0}".format(event))
            self._current_event = event.eid
            self._current_event_resource = event.resource
        except MarqueeBusy as e:
            # self._node.log.warn("Marquee busy for {event} : {e}",
            #                     event=event, e=e.now_playing)
            return e.collision_count
        self.remove(event.eid)
        self.prune()

    def _succeed_event(self, event):
        try:
            self._node.api_text_success([event])
        except NotImplementedError:
            self.log.warn("Node has no text event success reporter")
