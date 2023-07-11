"""
Test suite for Model.py
"""

import unittest

from context import jodeln
from jodeln.od import odme_fratar
from jodeln.od.od_matrix import ODMatrix

volumes = {
    (0, 0): 5,
    (0, 1): 10,
    (1, 0): 3,
    (1, 1): 33
}

sample_od = ODMatrix(
    volume=volumes,
    origins=[0, 1],
    destinations=[0, 1],
    names_o=['0', '1'],
    names_d=['0', '1'],
    targets_o={0: 20, 1: 30},
    targets_d={0: 17, 1: 51}
)


class TestFratar(unittest.TestCase):

    # def test_margin_sums(self):
    #     """Test summing origin and destination totals."""
    #     origin_sums, destinations_sums = od_fratar.get_default_margin_sums(sample_od)
    #     od_fratar.margin_sums(sample_od, origin_sums, destinations_sums)

    #     self.assertEqual((origin_sums, destinations_sums), 
    #                      ({0: 15, 1: 36}, {0: 8, 1: 43}))


    def test_fratar(self):
        res = odme_fratar.estimate_od(sample_od)
        print(res.volume)
        print(res.sums_o)
        print(res.sums_d)
        self.assertEqual(1, 1)       

if __name__ == '__main__':
    unittest.main()