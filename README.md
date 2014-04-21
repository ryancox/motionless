motionless is a Python library that takes the pain out of generating [Google Static Map](http://code.google.com/apis/maps/documentation/staticmaps/) URLs. Three map types are supported. Each is illustrated below. For fully worked code see the examples directory for code that parses and visualizes both GeoRSS feeds and GPX files. 

Code is licensed under Apache 2.0

For DecoratedMaps, paths are encoded if [gpolyencode](http://code.google.com/p/py-gpolyencode/) is present. This is useful for keeping URLs with in the 2048 character limit imposed by the service.

If you have run into bugs, open a github issue. If you have questions, feel free to email me at ryan.a.cox@gmail.com

-ryan 
@ryancox
[www.asciiarmor.com](http://www.asciiarmor.com)

CenterMap
=========

CenterMaps show a map with no markers or paths, centered on a single location.

    from motionless import CenterMap
    cmap = CenterMap(address='151 third st, san francisco, ca')
    print cmap.generate_url()

![SFMOMA](http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&center=151%20third%20st%2C%20san%20francisco%2C%20ca&zoom=17&size=400x400&sensor=false)

    from motionless import CenterMap
    cmap = CenterMap(lat=48.858278,lon=2.294489,maptype='satellite')
    print cmap.generate_url()

![La Tour Eiffel](http://maps.google.com/maps/api/staticmap?maptype=satellite&format=png&center=48.858278,2.294489&zoom=17&size=400x400&sensor=false)

VisibleMap
==========

VisibleMaps show a map with no markers or paths, automatically sized and zoomed to make the specified locations visible.

    from motionless import VisibleMap
    vmap = VisibleMap(maptype='terrain')
    vmap.add_address('Sugarbowl, Truckee, CA')
    vmap.add_address('Tahoe City, CA')
    print vmap.generate_url()

![Sugarbowl and Tahoe City](http://maps.google.com/maps/api/staticmap?maptype=terrain&format=png&size=400x400&sensor=false&visible=Sugarbowl%2C%20Truckee%2C%20CA|Tahoe%20City%2C%20CA)

DecoratedMap
============

DecoratedMaps contain markers and/or paths. They are automatically sized and zoomed to make the specified elements visible.

    from motionless import DecoratedMap
    dmap = DecoratedMap()
    dmap.add_marker(AddressMarker('1 Infinite Loop, Cupertino, CA',label='A'))
    dmap.add_marker(AddressMarker('1600 Amphitheatre Parkway Mountain View, CA',label='G'))
    print dmap.generate_url()


![Apple and Google](http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&size=400x400&sensor=false&markers=|label:G|1600%20Amphitheatre%20Parkway%20Mountain%20View%2C%20CA&markers=|label:A|1%20Infinite%20Loop%2C%20Cupertino%2C%20CA)

Produced from parsing GPX file. See [examples/munich.py](http://github.com/ryancox/motionless/blob/master/examples/munich.py)

![Munich](http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&size=640x640&sensor=false&markers=|color:green|label:S|48.167051,11.565088&markers=|color:red|label:E|48.351883,11.791474&path=color:blue|weight:8|enc:as%7EdHwxqeAc%40VPL_%40M%7DCOuBBgGn%40qDX%7BFmAoHyBcGaDeCwC%7BDwAeBwHaCcNK_AKcBD%7BBC_FEcAnCasA%7EDcOXNp%40Et%40DXCf%40IRSR%5DL%5DJgABe%40%3Fi%40QwAa%40mAy%40_AcN%7DKmHoGmGiGwHiKmEmLwBsK%7DByO%7BC%7DK_FoK_HsI_JoGgJcEeJsD%7BUaJge%40aRko%40oWiQ_Hym%40qVuf%40yRc%5C_Ncp%40gW%7D%7B%40w%5Dqd%40%7BPwP_CgPHyQnC%7Bz%40dSwo%40%60PwSjHek%40jVm%5BpN_k%40vX_HjDiK%60FuLnGiIlDoGjDcJhCkGm%40cIaEeFeGyEkLqIqTmIcUsJyVkFyQyFkUcJmc%40aHwd%40sEsd%40sDkj%40qA_e%40Ye%60%40Kad%40_Amf%40cC_%5CgDwTiHaX_KeU%7DKmPmOiQkNuRgJoRiGiRgJySuBwKYsJv%40mWa%40oUiCkv%40mAq%60%40aAqX%7D%40eZo%40%7B%5Dg%40mZHiFRmBNu%40Nq%40l%40%7BAVm%40rA%7BB%60AaAb%40WrBq%40xJyBx%40%5Bn%40i%40%7C%40yAN%5Df%40mBNoA%3FmCm%40aPI%7DRc%40cPq%40qS%5DiA%3Fq%40COGMGIM%3FOJENq%40TmHTgDNW%5CA%7D%40KsA_%40a%40c%40B)


Produced from GeoRSS feed. See [examples/earthquakes.py](http://github.com/ryancox/motionless/blob/master/examples/earthquakes.py)

![Earthquakes](http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&size=640x440&sensor=false&markers=|size:small|color:orange|6.6898%2C126.9682|-22.6135%2C171.4428|-9.4975%2C39.0599|38.4507%2C69.6269|1.2434%2C126.2770|-6.5013%2C103.9625|-19.9078%2C-70.4193|10.9153%2C93.1003&markers=|size:small|color:yellow|52.6990%2C-169.5456|25.0323%2C-109.2170|62.2883%2C-151.0877|40.3047%2C-121.1883|36.2482%2C-120.8153|19.0879%2C-67.7389|51.0635%2C179.5235|48.0544%2C154.6778|37.0584%2C141.6820|59.8743%2C-151.6975|2.2654%2C128.6509|62.0074%2C-145.6437|32.1655%2C-115.2977|61.0357%2C-148.2192|38.8964%2C21.4249)
