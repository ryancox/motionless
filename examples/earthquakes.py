"""Get the current USGS earthquake feed and add it to a DecoratedMap."""
from __future__ import print_function
from motionless import LatLonMarker, DecoratedMap
from six.moves.urllib import request
try:
    import geojson
except ImportError:
    print('This example requires the geojson package')
    quit()

# Get the geojson feed from USGS
opener = request.urlopen('http://earthquake.usgs.gov/earthquakes/feed/v1.0'
                         '/summary/2.5_day.geojson')

# Parse it
gjs = geojson.loads(opener.read().decode('utf-8'))

# Prepare a map and add the points
gmap = DecoratedMap(size_x=640, size_y=440)
for feat in gjs.features[:260]:  # in case there are many earthquakes today
    magnitude = feat['properties']['mag']
    lon, lat, _ = feat['geometry']["coordinates"]
    if magnitude > 2:
        color = 'yellow'
        size = 'small'
    if magnitude > 5:
        color = 'orange'
        size = 'small'
    if magnitude > 7:
        color = 'red'
        size = 'mid'
    gmap.add_marker(LatLonMarker(lat, lon, color=color, size=size))

htmlPage = """
<html>
<body>
<h2>Earthquakes 2.5+ today</h2>
<i>GeoRSS feed parsed and visualized. Colors assigned to markers based on
magnitudes. Details can be found on the
<a href='http://earthquake.usgs.gov/earthquakes/'>USGS web site</a>.
<p/>
<p/>
<img src="%s"/>
</body>
</html>
""" % gmap.generate_url()

with open("earthquakes.html", "w")as html:
    html.write(htmlPage)
print("earthquakes.html file created")
