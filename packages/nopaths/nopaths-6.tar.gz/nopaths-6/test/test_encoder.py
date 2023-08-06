# This file is placed in the Public Domain.
# pylint: disable=C0114,C0114,C0115,C0116,C0413,W0611
# pylama: ignore=E303,E402


import sys
import unittest


sys.path.insert(0, "..")


from nopaths.encoder import dumps
from nopaths.objects import Object


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):


    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)
