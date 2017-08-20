import os
from tkinter import filedialog as fdlg

import LoadDataFromAPI

import LoadDataFromFile


def FileLoaderChooser(choice):
    choices = {'file': file,
               'api': api,
               'database': database}
    return choices[choice]()


def file():
    "Open dialog box, select and store filename into a global list"
    filenames = fdlg.askopenfilenames(filetypes=[("Python pickle", "*.pickle")])  # returns empty if canceled
    dirname = os.path.dirname(os.path.abspath(filenames[0]))
    data = []
    for i in range(len(filenames)):
        filename = os.path.join(dirname, 'state_{}.pickle'.format(i))
        fdata = LoadDataFromFile.LoadDataFromFile(filename)
        data.append(fdata.read_source())
    return data


def api():
    dataconnect = LoadDataFromAPI.LoadDataFromApi('United States')
    df = dataconnect.read_source()


def database():
    return
