# This file is placed in the Public Domain.
# pylint: disable=C0413,C0103,C0114,C0115,C0116,R0903
# pylama: ignore=W0611,E303,E402


import os
import sys
import unittest


sys.path.insert(0, "..")


from nopaths.objects import Object
from nopaths.persist import Persist, write


import nopaths.persist


Persist.workdir = '.test'


ATTRS1 = (
          'Persist',
          'last',
          'read',
          'write',
          'writerec'
         )


class TestStorage(unittest.TestCase):

    def test_constructor(self):
        obj = Persist()
        self.assertTrue(type(obj), Persist)

    def test__class(self):
        obj = Persist()
        clz = obj.__class__()
        self.assertTrue('Persist' in str(type(clz)))

    def test_dirmodule(self):
        self.assertEqual(
                         dir(nopaths.persist),
                         list(ATTRS1)
                        )

    def test_module(self):
        self.assertTrue(Persist().__module__, 'nopaths.persist')

    def test_save(self):
        Persist.workdir = '.test'
        obj = Object()
        opath = write(obj)
        self.assertTrue(os.path.exists(Persist.path(opath)))
