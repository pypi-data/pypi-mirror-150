

import os
from ebs.linuxnode.gui.kivy.core.basenode import BaseIoTNodeGui
from ebs.linuxnode.gallery.mixin import GalleryMixin
from ebs.linuxnode.gui.kivy.gallery.mixin import GalleryGuiMixin
from ebs.linuxnode.bgsequence.mixin import EffectiveBackgroundMixin
from .scheduler.mixin import EventManagerMixin

try:
    from ebs.linuxnode.gui.kivy.exim.mixin import EximGuiMixin
except ImportError:
    class EximGuiMixin(object):
        pass


class SignageNode(EffectiveBackgroundMixin,
                  GalleryGuiMixin,
                  GalleryMixin,
                  EventManagerMixin,
                  EximGuiMixin,
                  BaseIoTNodeGui):
    def install(self):
        super(SignageNode, self).install()
        self.config.register_application_root(
            os.path.abspath(os.path.dirname(__file__))
        )
