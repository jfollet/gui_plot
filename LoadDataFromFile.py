import pandas as pd

from AbstractLoadDataClass import AbstractLoadDataClass


class LoadDataFromFile(AbstractLoadDataClass):
    """ Reads the stored pickle files that contain a dateframe of a airplane data tables """

    def __init__(self, filename):
        super().__init__(filename)

    def read_source(self):
        return pd.read_pickle(self.source)


