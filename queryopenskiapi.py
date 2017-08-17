from LoadDataFromAPI import LoadDataFromApi
import pandas as pd
import os
import pathlib
import time
import copy

dataconnect = LoadDataFromApi('United States')
for i in range(101):
    path = pathlib.Path(os.path.join(os.getcwd(), 'pdata'))
    path.mkdir(parents=True, exist_ok=True)
    filepath = path.joinpath('state_{}.pickle'.format(i))
    df = dataconnect.read_source()
    # if i != 0:
    #     print(df, pd.read_pickle(path.joinpath('state_{}.pickle'.format(i-1))))
    df.to_pickle(filepath)
    time.sleep(60)


