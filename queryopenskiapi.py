import os
import pathlib
import time

from loaddata.LoadDataFromApi import LoadDataFromApi

dataconnect = LoadDataFromApi('United States')
for i in range(101):
    df = dataconnect.read_source()
    path = pathlib.Path(os.path.join(os.getcwd(), 'pdata'))
    path.mkdir(parents=True, exist_ok=True)
    filepath = path.joinpath('state_{}.pickle'.format(i))
    # if i != 0:
    #     print(df, pd.read_pickle(path.joinpath('state_{}.pickle'.format(i-1))))
    df.to_pickle(filepath)
    print("file {} written!".format(filepath))
    time.sleep(2*60)


