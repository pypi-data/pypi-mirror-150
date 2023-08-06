__all__ = ['ArrayMapping']


class ArrayMapping:
    def __init__(self, data):
        self._storage = data

    def __len__(self):
        return len(self._storage)