import jsonpickle
import json

class pickable:
    def json(self):
        return json.loads(jsonpickle.encode(self, unpicklable=False))
    