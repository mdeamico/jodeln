"""
Test suite for Model.py
"""

import unittest
import pathlib
import os

from context import jodeln
from jodeln.model import Model


class TestModel(unittest.TestCase):

    def test_load(self):
        """Test loading an empty network."""
        model = Model()
        # passing no arguments to model.load should return False
        res = model.load()
        self.assertEqual(res, False)

    def test_od_estimation(self):
        """Test a simple OD estimation."""
        model = Model()
        tests_path = pathlib.Path(__file__).parent.absolute()
        net_path = os.path.join(tests_path, "networks", "net01")
        
        model.load(node_file=os.path.join(net_path, "nodes.csv"),
                   links_file=os.path.join(net_path, "links.csv"),
                   od_seed_file=os.path.join(net_path, "seed_matrix.csv"))
        
        res = model.estimate_od_cmaes(1, 1, 1)

        print(f"\nestimated od: {model.od_estimated}\n")

        print(f"\nres (before taking abs value): {res}\n")
        odme_res = [round(abs(x), 4) for x in res]

        expected_res = [0.5839, 0.9216, 0.5537, 1.1827]
        
        self.assertEqual(odme_res == expected_res, True)


if __name__ == '__main__':
    unittest.main()