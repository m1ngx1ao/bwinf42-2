from .besiedlungsplan import TPunkt

class Polygon:
    def __init__(self, linienzug: list[TPunkt]):
        assert linienzug[0] == linienzug[-1]
        self.__linienzug = linienzug
    def enthaelt(self, p: TPunkt):
        return False
    