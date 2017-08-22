from loaddata import AbstractLoadDataClass


class LoadDataFromDatabase(AbstractLoadDataClass):

    def __init__(self, database):
        super(self, database)

    def read_source(self):
        print(self.source)
        return
