

from ebs.signagenode.app import SignageApplication
from node import ExampleSignageNode


class ExampleSignageApplication(SignageApplication):
    _node_class = ExampleSignageNode
