"""
Testing select-Link and select-turn analysis. 
"""

import unittest
import pathlib
import os

from context import jodeln
from jodeln.model import Model


class TestSelectLink(unittest.TestCase):

    def test_select_link(self):
        """Test generating select-link analysis."""
        model = Model()
        tests_path = pathlib.Path(__file__).parent.absolute()
        net_path = os.path.join(tests_path, "networks", "net01")
        
        model.load(node_file=os.path.join(net_path, "nodes.csv"),
                   links_file=os.path.join(net_path, "links.csv"),
                   od_seed_file=os.path.join(net_path, "seed_matrix.csv"))
        
        select_link = model.select_link()

        print(f"\nselect-link:\n{select_link}")
        
        expected_select_link = {
            (0, 2): {(0, 4): 1, (0, 5): 1}, 
            (1, 2): {(1, 4): 1, (1, 5): 1}, 
            (2, 3): {(1, 4): 1, (0, 4): 1, (0, 5): 1, (1, 5): 1}, 
            (3, 4): {(0, 4): 1, (1, 4): 1}, 
            (3, 5): {(0, 5): 1, (1, 5): 1}}

        self.assertEqual(select_link == expected_select_link, True)
    
    def test_select_turn(self):
        """Test generating select-turn analysis."""
        model = Model()
        tests_path = pathlib.Path(__file__).parent.absolute()
        net_path = os.path.join(tests_path, "networks", "net01")
        
        model.load(node_file=os.path.join(net_path, "nodes.csv"),
                   links_file=os.path.join(net_path, "links.csv"),
                   od_seed_file=os.path.join(net_path, "seed_matrix.csv"))
        
        select_turn = model.select_turn()

        print(f"\nselect-turn:\n{select_turn}")
        
        expected_select_turn = {
            (0, 2, 3): {(0, 4): 1, (0, 5): 1}, 
            (1, 2, 3): {(1, 4): 1, (1, 5): 1}, 
            (2, 3, 4): {(0, 4): 1, (1, 4): 1}, 
            (2, 3, 5): {(0, 5): 1, (1, 5): 1}}

        self.assertEqual(select_turn == expected_select_turn, True)


if __name__ == '__main__':
    unittest.main()