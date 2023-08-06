

from ebs.linuxnode.gui.kivy.utils.application import BaseIOTNodeApplication
from .node import SignageNode


class SignageApplication(BaseIOTNodeApplication):
    _node_class = SignageNode
