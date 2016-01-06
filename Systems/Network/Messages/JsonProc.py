from Systems.Utils.JsonHelper import *


class JsonProc:
    def __init__(self, proc):
        self.proc = proc

    def to_json(self):
        return to_json(self)

    def from_json(self, json_data):
        self.proc = json_data['proc']
        return self
