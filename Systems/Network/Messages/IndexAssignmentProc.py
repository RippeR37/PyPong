from Systems.Network.Messages.JsonProc import JsonProc
from Systems.Utils.JsonHelper import *


class IndexAssignmentProc(JsonProc):
    def __init__(self, index):
        super().__init__("index_assignment")
        self.data = dict()
        self.data['index'] = index

    def to_json(self):
        return to_json(self)

    def from_json(self, json_data):
        super().from_json(json_data)
        self.data['index'] = int(json_data['data']['index'])
        return self
