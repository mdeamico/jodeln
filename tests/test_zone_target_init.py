"""
Test suite for Model.py
"""

import unittest
import pathlib
import os

from context import jodeln
from jodeln.model import Model


class TestZoneTargetInit(unittest.TestCase):
    def test_zone_target_import(self):
        """Test initializing OD zone targets based on incoming/outgoing link targets."""
        model = Model()
        tests_path = pathlib.Path(__file__).parent.absolute()
        net_path = os.path.join(tests_path, "networks", "net01")
        
        # Do not load the zone targets from csv. model.load will internally init zone targets. 
        model.load(node_file=os.path.join(net_path, "nodes.csv"),
                   links_file=os.path.join(net_path, "links.csv"),
                   od_seed_file=os.path.join(net_path, "seed_matrix.csv"),
                   turns_file=os.path.join(net_path, "turns.csv"))
        
        self.assertEqual(model.od_seed.targets_o == {0: 100.0, 1: 75.0, 4: 0, 5: 0}, True)
        self.assertEqual(model.od_seed.targets_d == {0: 0, 1: 0, 4: 50.0, 5: 125.0}, True)
                


if __name__ == '__main__':
    unittest.main()