from abc import ABCMeta, abstractmethod
from pint import UnitRegistry

"""LoadData Class will load data from a file and create a dictionary of data.  Utilizes pandas data structures"""


class AbstractLoadDataClass(object):
    __metaclass__ = ABCMeta
    ureg = UnitRegistry()

    def __init__(self, source):
        self.source = source

    @abstractmethod
    def read_source(self):
        return

