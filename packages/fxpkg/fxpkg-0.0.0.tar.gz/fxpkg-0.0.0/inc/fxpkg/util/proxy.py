class DictObjectPorxy:
    def __init__(self, o: object):
        self.o = o

    def keys(self):
        return dir(self.o)

    def items(self):
        for k in self.keys():
            yield getattr(self.o, k)

    def __getitem__(self, key):
        return getattr(self.o, key)

    def __setitem__(self, key, value):
        setattr(self.o, key, value)

    def __delitem__(self, key):
        delattr(self.o, key)

    def __contains__(self, key):
        return hasattr(self.o, key)

    def update(self, d: dict, cond=None):
        if cond is not None:
            for k, v in d.items():
                if cond(k, v):
                    self[k] = v
        for k, v in d.items():
            self[k] = v

    def get(self, key, default = None):
        if key in self:
            return self[key]
        else:
            return default
