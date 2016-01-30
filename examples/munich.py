"""Parse a GPS track and add it to a DecoratedMap."""
from __future__ import print_function
import xml.sax
import os
from motionless import LatLonMarker, DecoratedMap


current_dir = os.path.dirname(os.path.abspath(__file__))

class GPXHandler(xml.sax.handler.ContentHandler):
    """GPS track parser"""
    def __init__(self, gmap):
        self.gmap = gmap
        self.first = True 
        self.prev = None

    def startElement(self, name, attrs):
        if name == 'trkpt': 
            self.gmap.add_path_latlon(attrs['lat'], attrs['lon'])
            self.prev = (attrs['lat'], attrs['lon'])
            if self.first:
                self.first = False
                marker = LatLonMarker(attrs['lat'], attrs['lon'],
                                      color='green', label='S')
                self.gmap.add_marker(marker)

    def endElement(self, name):
        if name == 'trk':
            marker = LatLonMarker(self.prev[0], self.prev[1],
                                  color='red', label='E')
            self.gmap.add_marker(marker)

# Make an empty map and fill it
munich = DecoratedMap(size_x=640, size_y=640, pathweight=8, pathcolor='blue')
parser = xml.sax.make_parser()
parser.setContentHandler(GPXHandler(munich))

fpath = os.path.join(current_dir, 'gps_track.gpx')
with open(fpath) as f:
    parser.feed(f.read())

htmlPage = """
<html>
<body>
<h2>Munich</h2>
<i>Trip from Schwabing (S) to Airport (E). gps_track.gpx file taken of my
Garmin device and edited down to single track.</i>
<p/>
<p/>
<img src="%s"/>
</body>
</html>
""" % munich.generate_url()

with open("munich.html", "w")as html:
    html.write(htmlPage)
print("munich.html file created")
