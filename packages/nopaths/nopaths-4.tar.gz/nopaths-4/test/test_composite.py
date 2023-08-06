# This file is placed in the Public Domain.
# pylint: disable=E1101


import os
import sys
import unittest


sys.path.insert(0, "..")


from nopaths.objects import Object
from nopaths.persist import read, write


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")

    def testcompositeprint(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        pth = write(obj)
        oo = Object()
        read(oo, pth)
        #self.assertEqual(oo.obj.a, "test")
        self.assertTrue(oo.obj)
