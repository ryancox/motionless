"""
Unit tests
"""
from __future__ import print_function
import unittest

from motionless import CenterMap, DecoratedMap, LatLonMarker
from motionless import VisibleMap, AddressMarker


class TestMotionless(unittest.TestCase):
    """
    Unit tests for motionless
    """

    def setUp(self):
        self.address = '151 third st, san francisco, ca'
        self.lat = 48.858278
        self.lon = 2.294489

    def test_centermap_sat(self):

        cmap_sat = CenterMap(lat=48.858278, lon=2.294489, maptype='satellite')

        self.assertEqual(
            cmap_sat.generate_url(),
            'https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&f'
            'ormat=png&scale=1&center=48.858278%2C2.294489&zoom=17&'
            'size=400x400&sensor=false&language=en')

    def test_visible(self):

        vmap = VisibleMap(maptype='terrain')
        vmap.add_address('Sugarbowl, Truckee, CA')
        vmap.add_address('Tahoe City, CA')

        self.assertEqual(
            vmap.generate_url(),
            'https://maps.googleapis.com/maps/api/staticmap?maptype=terrain&'
            'format=png&scale=1&size=400x400&sensor=false&'
            'visible=Sugarbowl%2C%20Truckee%2C%20CA%7CTahoe%20City%2C%20CA&'
            'language=en')

    def test_create_map_with_address(self):
        """Checks the correct url generated with an address"""
        center_map = CenterMap(address=self.address)

        self.assertEqual(
            center_map.generate_url(),
            'https://maps.googleapis.com/maps/api/staticmap?maptype=roadmap&'
            'format=png&scale=1&center=151%20third%20st%2C%20san%20francisco'
            '%2C%20ca&zoom=17&size=400x400&sensor=false&language=en')

    def test_addressmarker(self):

        # For some reason the url is not always same. So the test is... well.
        dmap = DecoratedMap()
        am = AddressMarker('1 Infinite Loop, Cupertino, CA', label='A')
        dmap.add_marker(am)
        am = AddressMarker('1600 Amphitheatre Parkway Mountain View, CA',
                           label='G')
        dmap.add_marker(am)
        _ = dmap.generate_url()

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
            'https://maps.googleapis.com/maps/api/staticmap?maptype=roadmap&'
            'format=png&scale=1&size=400x400&sensor=false&language=en&'
            'markers=%7Clabel%3AG%7C37.422782%2C-122.085099&'
            'style=feature%3Aroad.highway%7Celement%3Ageomoetry%7C'
            'color%3A0xc280e9%7C'
        )

    def test_demos(self):

        # Quick n dirty test to see if demos are OK
        import os
        import sys
        test_dir = os.path.dirname(os.path.abspath(__file__))
        ex_dir = os.path.join(test_dir, os.pardir, 'examples')
        ex_dir = os.path.abspath(ex_dir)
        if not os.path.exists(ex_dir):
            # This can happen, it doesn't really matter
            return

        sys.path.append(ex_dir)
        import demo
        import munich
        try:
            import geojson
            import earthquakes
        except ImportError:
            pass

if __name__ == "__main__":
    unittest.main()
