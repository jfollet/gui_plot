from abc import ABCMeta, abstractmethod

"""LoadData Class will load data from a file and create a dictionary of data.  Utilizes pandas data structures"""


class AbstractLoadDataClass:
    __metaclass__ = ABCMeta

    def __init__(self, source):
        self.source = source

    @abstractmethod
    def read_source(self):
        """Returns a pandas dataframe with time, callsign, longitude, latitude, altitude and country"""
        return
