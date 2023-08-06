

from starxmedia.app import StarXMediaApplication
from .node import KioskMultiWebNode


class KioskMultiWebApplication(StarXMediaApplication):
    _node_class = KioskMultiWebNode
