# This file is placed in the Public Domain.


"object programming tests"


import inspect
import os
import sys
import unittest


from obj import Object, keys, values
from tbl import Table


import cmds


Table.add(cmds)


class Test_Table(unittest.TestCase):

    def test_mod(self):
        self.assertTrue("cmds" in keys(Table.mod))
