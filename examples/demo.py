"""Examples of the various maps that can be created with motionless."""
from __future__ import print_function
from motionless import AddressMarker, DecoratedMap, CenterMap, VisibleMap

cmap = CenterMap(address='151 third st, san francisco, ca')

cmap_sat = CenterMap(lat=48.858278, lon=2.294489, maptype='satellite')

vmap = VisibleMap(maptype='terrain')
vmap.add_address('Sugarbowl, Truckee, CA')
vmap.add_address('Tahoe City, CA')

dmap = DecoratedMap()
dmap.add_marker(AddressMarker('1 Infinite Loop, Cupertino, CA', label='A'))
dmap.add_marker(AddressMarker('1600 Amphitheatre Parkway Mountain View, CA',
                              label='G'))


htmlPage = """
<html>
<body>
<h2>SFMOMA</h2>
<img src="%s"/>
<h2>La Tour Eiffel</h2>
<img src="%s"/>
<h2>Tahoe City and Sugarbowl</h2>
<img src="%s"/>
<h2>Google and Apple</h2>
<img src="%s"/>
</body>
</html>
""" % (
    cmap.generate_url(), 
    cmap_sat.generate_url(),
    vmap.generate_url(), 
    dmap.generate_url()) 

with open("demo.html", "w") as html:
    html.write(htmlPage)
print("demo.html created")
