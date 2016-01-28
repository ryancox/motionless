# coding: utf-8
"""
Unit tests for pypvwatts.

"""
import unittest

from motionless import CenterMap, DecoratedMap, LatLonMarker


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

        self.assertEqual(
            center_map.generate_url(),
            'https://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&scale=1&center=151%20third%20st%2C%20san%20francisco%2C%20ca&zoom=17&size=400x400&sensor=false&language=en')

    def test_create_marker_map_with_styles(self):
        """Check correct url generated with markers + styles"""
        styles = [{
            'feature': 'road.highway',
            'element': 'geomoetry',
            'rules': {
                'color': '#c280e9'
            }
        }]
        decorated_map = DecoratedMap(style=styles)
        decorated_map.add_marker(LatLonMarker('37.422782', '-122.085099',
                                              label='G'))
        self.assertEqual(
            decorated_map.generate_url(),
            'https://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&scale=1&size=400x400&sensor=false&language=en&markers=|label:G|37.422782,-122.085099&style=feature:road.highway|element:geomoetry|color:0xc280e9|'
        )


if __name__ == "__main__":
    unittest.main()
