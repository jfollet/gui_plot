import os
from unittest import TestCase

import pandas

from loaddata import *


class LoadDataFromApiTests(TestCase):
    def test_loading(self):
        dataconnect = LoadDataFromApi('United States')
        self.assertIsInstance(dataconnect.read_source(), pandas.DataFrame)


class LoadDataFromFilesTests(TestCase):
    def test_loading(self):
        dirname = 'pdata'
        filename = os.path.join(dirname, 'state_0.pickle')
        fdata = LoadDataFromFile(filename)
        self.assertIsInstance(fdata.read_source(), pandas.DataFrame)


class LoadDataFromDatabaseTests(TestCase):
    def test_loading(self):
        pass
