
motionless is a Python library that takes the pain out of generating Google Static Map URLs. Three map types are supported.

CenterMap
=========

    from motionless import CenterMap
    cmap = CenterMap(address='151 third st, san francisco, ca')
    print cmap.generate_url()

![SFMOMA][http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&center=151%20third%20st%2C%20san%20francisco%2C%20ca&zoom=17&size=400x400&sensor=false]

VisibleMap
==========

    from motionless import VisibleMap
    vmap = VisibleMap(maptype='terrain')
    vmap.add_address('Sugarbowl, Truckee, CA')
    vmap.add_address('Tahoe City, CA')
    print vmap.generate_url()

![Sugarbowl and Tahoe City][http://maps.google.com/maps/api/staticmap?maptype=terrain&format=png&size=400x400&sensor=false&visible=Sugarbowl%2C%20Truckee%2C%20CA|Tahoe%20City%2C%20CA]

DecoratedMap
============

    from motionless import VisibleMap
    dmap = DecoratedMap()
    dmap.add_marker(AddressMarker('1 Infinite Loop, Cupertino, CA',label='A'))
    dmap.add_marker(AddressMarker('1600 Amphitheatre Parkway Mountain View, CA',label='G'))
    print dmap.generate_url()


![Apple and Google][http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&size=400x400&sensor=false&markers=|label:G|1600%20Amphitheatre%20Parkway%20Mountain%20View%2C%20CA&markers=|label:A|1%20Infinite%20Loop%2C%20Cupertino%2C%20CA]
