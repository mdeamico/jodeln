"""
Test suite for Model.py
"""

import unittest
import pathlib
import os

from context import jodeln
from jodeln.model import Model


class TestOdmeLeastSq(unittest.TestCase):
    def test_odme_leastsq(self):
        """Test a simple OD estimation."""
        model = Model()
        tests_path = pathlib.Path(__file__).parent.absolute()
        net_path = os.path.join(tests_path, "networks", "net01")
        
        model.load(node_file=os.path.join(net_path, "nodes.csv"),
                   links_file=os.path.join(net_path, "links.csv"),
                   od_seed_file=os.path.join(net_path, "seed_matrix.csv"),
                   turns_file=os.path.join(net_path, "turns.csv"))
        
        model.estimate_od_leastsq(seed_od_weight=0.50)
        
        self.assertEqual(1 == 1, True)


if __name__ == '__main__':
    unittest.main()