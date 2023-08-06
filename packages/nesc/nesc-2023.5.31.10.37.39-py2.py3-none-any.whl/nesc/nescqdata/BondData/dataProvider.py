from ..baseDataProvider import TypeOfProvider


class DataProvider(TypeOfProvider):

    def __init__(self, dfs=None):
        super(DataProvider, self).__init__("bond", dfs)
