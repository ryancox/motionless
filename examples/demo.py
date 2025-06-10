"""Examples of the various maps that can be created with motionless."""
from motionless import AddressMarker, CenterMap, DecoratedMap, VisibleMap

cmap = CenterMap(address='151 third st, san francisco, ca')

cmap_sat = CenterMap(lat=48.858278, lon=2.294489, maptype='satellite')

vmap = VisibleMap(maptype='terrain')
vmap.add_address('Sugarbowl, Truckee, CA')
vmap.add_address('Tahoe City, CA')

dmap = DecoratedMap()
dmap.add_marker(AddressMarker('1 Infinite Loop, Cupertino, CA', label='A'))
dmap.add_marker(AddressMarker('1600 Amphitheatre Parkway Mountain View, CA',
                              label='G'))


htmlPage = f"""
<html>
<body>
<h2>SFMOMA</h2>
<img src="{cmap.generate_url()}"/>
<h2>La Tour Eiffel</h2>
<img src="{cmap_sat.generate_url()}"/>
<h2>Tahoe City and Sugarbowl</h2>
<img src="{vmap.generate_url()}"/>
<h2>Google and Apple</h2>
<img src="{dmap.generate_url()}"/>
</body>
</html>
"""

with open("demo.html", "w") as html:
    html.write(htmlPage)
print("demo.html created")
