from Systems.Network.Messages.JsonProc import JsonProc
from Systems.Utils.JsonHelper import *


class ServerReadyProc(JsonProc):
    def __init__(self):
        super().__init__("server_ready")

    def to_json(self):
        return to_json(self)

    def from_json(self, json_data):
        super().from_json(json_data)
        return self
