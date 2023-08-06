

from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui
from ebs.linuxnode.gui.kivy.marquee.mixin import MarqueeGuiMixin

from .eventmanagers.text import TextEventManager
from .eventmanagers.webresource import WebResourceEventManager

from .resources import ScheduledResourceClass

from ebs.linuxnode.core.constants import WEBRESOURCE
from ebs.linuxnode.core.constants import TEXT

try:
    from ebs.linuxnode.gui.kivy.mediaplayer.omxplayer import OMXPlayerGuiMixin
    ActualMediaPlayerMixin = OMXPlayerGuiMixin
except ImportError:
    ActualMediaPlayerMixin = MediaPlayerGuiMixin


class EventManagerMixin(ActualMediaPlayerMixin, MarqueeGuiMixin, BaseIoTNodeGui):
    def __init__(self, *args, **kwargs):
        self._event_managers = {}
        self._success_api_engine = None
        if 'resource_class' in kwargs.keys():
            self.log.warn("'{} resource_class' specified, but the EventManagerMixin is going to force {}"
                          "".format(kwargs['resource_class'], ScheduledResourceClass.__class__))
        kwargs['resource_class'] = ScheduledResourceClass
        super(EventManagerMixin, self).__init__(*args, **kwargs)

    def install(self):
        super(EventManagerMixin, self).install()
        self.event_manager_install(WebResourceEventManager(self, WEBRESOURCE))
        self.event_manager_install(TextEventManager(self, TEXT))

    def event_manager_install(self, manager):
        self.log.info("Installing Event Manager {1} with emid {0}".format(manager.emid, manager))
        self._event_managers[manager.emid] = manager

    def event_manager(self, emid):
        return self._event_managers[emid]

    @property
    def _cache_trim_exclusions(self):
        if self.event_manager(WEBRESOURCE).current_event_resource:
            return [self.event_manager(WEBRESOURCE).current_event_resource]
        else:
            return []

    def api_media_success(self, events):
        if not self._success_api_engine:
            raise NotImplementedError
        self._success_api_engine.api_media_success(events)

    def api_text_success(self, events):
        if not self._success_api_engine:
            raise NotImplementedError
        self._success_api_engine.api_text_success(events)

    def start(self):
        super(EventManagerMixin, self).start()
        for emid, manager in self._event_managers.items():
            manager.start()
