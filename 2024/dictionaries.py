from collections import UserDict


class DictSet(UserDict):
    def __setitem__(self, key, value):
        raise TypeError("Not allowed to explicitly set")

    def __getitem__(self, key):
        if key not in self.data:
            self.data[key] = set()
        return self.data[key]


class DictList(UserDict):
    def __setitem__(self, key, value):
        if key not in self.data:
            self.data[key] = list()
        self.data[key].add(value)

    def __getitem(self, key):
        if key not in self.data:
            self.data[key] = list()
        return self[key]
