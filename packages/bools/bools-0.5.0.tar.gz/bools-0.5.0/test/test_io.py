import pandas as pd
import unittest
from bools.io import *


class TestIO(unittest.TestCase):
    def test_read_lines(self):
        self.assertEqual(
            read_lines('test.json', lambda x: 3, lambda x: x, log=False),
            [3, 3]
        )
        print('read lines', read_lines('test.json', lambda x: x.split(' '), pd.DataFrame, log=True))

    def test_read_jsons(self):
        self.assertEqual(
            read_jsons('test.json', lambda x: x, log=True),
            [{'a': 1, 'b': 2}]
        )

    def test_pd_mixin(self):
        from bools.mixin import pandas
        pandas.mixin()

        print('read jsons\n', pd.read_jsons('test.json', log=True))
