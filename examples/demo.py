
from motionless import AddressMarker, LatLonMarker,DecoratedMap, CenterMap, VisibleMap

cmap = CenterMap(address='151 third st, san francisco, ca')

cmap1 = CenterMap(lat=48.858278,lon=2.294489,maptype='satellite')

vmap = VisibleMap(maptype='terrain')
vmap.add_address('Sugarbowl, Truckee, CA')
vmap.add_address('Tahoe City, CA')

dmap = DecoratedMap()
dmap.add_marker(AddressMarker('1 Infinite Loop, Cupertino, CA',label='A'))
dmap.add_marker(AddressMarker('1600 Amphitheatre Parkway Mountain View, CA',label='G'))


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
    cmap1.generate_url(), 
    vmap.generate_url(), 
    dmap.generate_url()) 
	 

html = open("demo.html","w")
html.write(htmlPage)
html.close()
print "demo.html created"

