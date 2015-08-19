# coding: utf-8
"""
Unit tests for pypvwatts.

"""
import unittest
from motionless import CenterMap


class Test(unittest.TestCase):
    """
    Unit tests for motionless
    """

    def setUp(self):
        self.address = '151 third st, san francisco, ca'
        self.lat = 48.858278
        self.lon = 2.294489

    def test_create_map_with_address(self):
        """Checks the correct url generated with an address"""
        center_map = CenterMap(address=self.address)
        # cmap1 = CenterMap(lat=48.858278,lon=2.294489,maptype='satellite')
        self.assertEqual(
            center_map.generate_url(),
            'https://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&scale=1&center=151%20third%20st%2C%20san%20francisco%2C%20ca&zoom=17&size=400x400&sensor=false&language=en')

if __name__ == "__main__":
    unittest.main()
