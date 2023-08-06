import json

class BuildAttrs:

    def append(self, key, value=None):
        setattr(self, key, value)

    def toDict(self):
        return vars(self)

    def toJson(self):
        return json.dumps(self.toDict())

    def toString(self):
        return self.toJson()

    def get(self, key):
        return getattr(self, key)
