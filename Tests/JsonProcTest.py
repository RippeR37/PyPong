from Systems.Network.Messages.JsonProc import JsonProc
import unittest
import json


class JsonProcTest(unittest.TestCase):

    def test_constructor(self):
        proc = "proc_name"
        jp = JsonProc(proc)

        self.assertEqual(jp.proc, proc)

    def test_to_json(self):
        proc = "proc_name"
        jp = JsonProc(proc)
        jp_json = jp.to_json()

        self.assertEqual(jp_json, '{"proc": "proc_name"}')

    def test_to_json_from_json(self):
        proc = "proc_name"
        jp = JsonProc(proc)
        jp_json = jp.to_json()
        jp2 = JsonProc("").from_json(json.loads(jp_json))

        self.assertEqual(jp.proc, jp2.proc)
