
from motionless import AddressMarker, DecoratedMap, CenterMap, VisibleMap

cmap = CenterMap(address='151 third st, san francisco, ca',zoom=17)
print cmap.generate_url()

cmap1 = CenterMap(lat=48.858278,lon=2.294489,maptype='satellite',zoom=17)
print cmap1.generate_url()

vmap = VisibleMap(maptype='terrain')
vmap.add_address('Sugarbowl, Truckee, CA')
vmap.add_address('Tahoe City, CA')
print vmap.generate_url()

dmap = DecoratedMap(maptype='terrain')
dmap.add_marker(AddressMarker('1 Infinite Loop, Cupertino, CA'))
dmap.add_marker(AddressMarker('1600 Amphitheatre Parkway Mountain View, CA'))
print dmap.generate_url()

