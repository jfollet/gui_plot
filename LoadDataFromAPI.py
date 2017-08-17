from operator import attrgetter

import numpy as np
import pandas as pd
from opensky_api import OpenSkyApi

from AbstractLoadDataClass import AbstractLoadDataClass


class LoadDataFromApi(AbstractLoadDataClass):
    def __init__(self, url):
        super().__init__(url)

    def read_source(self):
        api = OpenSkyApi()
        states = api.get_states()
        df = pd.DataFrame.from_items([
            ('origin_country', self._convert_state_api('origin_country', states.states)),
            ('callsign', self._convert_state_api('callsign', states.states)),
            ('longitude', self._convert_state_api('longitude', states.states)),
            ('latitude', self._convert_state_api('latitude', states.states)),
            ('altitude', self._convert_state_api('altitude', states.states)), ])
        filter_out = (df['origin_country'] == self.source) \
                     & df['callsign'] \
                     & ~np.isnan(df['longitude']) \
                     & ~np.isnan(df['latitude']) \
                     & ~np.isnan(df['altitude'])
        # print(df[filter_out])
        return df[filter_out]

    @staticmethod
    def _convert_state_api(param, states):
        return list(map(attrgetter(param), states))

if __name__ == '__main__':
    dl = LoadDataFromApi('United States').read_source()
    print(dl)
