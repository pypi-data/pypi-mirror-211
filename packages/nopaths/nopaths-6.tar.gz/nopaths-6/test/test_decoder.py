# This file is placed in the Public Domain.
# pylint: disable=C0114,C0115,C0116,C0413
# pylama: ignore=W0611,E402


import os
import sys
import unittest


sys.path.insert(0, os.getcwd())


from nopaths.decoder import loads
from nopaths.encoder import dumps
from nopaths.objects import Object


class TestDecoder(unittest.TestCase):

    def test_loads(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, "bla")

    def test_doctest(self):
        self.assertTrue(__doc__ is None)
