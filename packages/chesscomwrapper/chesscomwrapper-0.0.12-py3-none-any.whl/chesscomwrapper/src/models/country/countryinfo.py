class CountryInfo(object):
    """A class to represent a country info with the name, code and id"""
    def __init__(self, data) -> None:
        self.name = data.get('name',None)
        self.code = data.get('code',None)
        self.id = data.get('@id',None)