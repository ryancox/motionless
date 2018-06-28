motionless
==========

[![fury.io](https://badge.fury.io/py/motionless.svg)](https://pypi.python.org/pypi/motionless/)
[![Build Status](https://travis-ci.org/ryancox/motionless.svg)](https://travis-ci.org/ryancox/motionless)
[![Coverage Status](https://coveralls.io/repos/ryancox/motionless/badge.svg?branch=master&service=github)](https://coveralls.io/github/ryancox/motionless?branch=master)


motionless is a Python library that takes the pain out of generating [Google Static Map](http://code.google.com/apis/maps/documentation/staticmaps/) URLs. Three map types are supported. Each is illustrated below. For fully worked code see the examples directory for code that parses and visualizes both GeoRSS feeds and GPX files.

motionless is tested with Python versions 2.7, 3.4, 3.5 and 3.6.

Code is licensed under Apache 2.0

For DecoratedMaps, paths are encoded using [gpolyencode](http://code.google.com/p/py-gpolyencode/) (shipped with motionless). This is useful for keeping URLs with in the 2048 character limit imposed by the service.


CenterMap
=========

CenterMaps show a map with no markers or paths, centered on a single location.

```python
from motionless import CenterMap
cmap = CenterMap(address='151 third st, san francisco, ca')
print(cmap.generate_url())
```

![SFMOMA](http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&scale=1&center=151%20third%20st%2C%20san%20francisco%2C%20ca&zoom=17&size=400x400&sensor=false&language=en)

```python 
from motionless import CenterMap
cmap = CenterMap(lat=48.858278,lon=2.294489,maptype='satellite')
print(cmap.generate_url())
```

![La Tour Eiffel](http://maps.google.com/maps/api/staticmap?maptype=satellite&format=png&scale=1&center=48.858278,2.294489&zoom=17&size=400x400&sensor=false&language=en)

VisibleMap
==========

VisibleMaps show a map with no markers or paths, automatically sized and zoomed to make the specified locations visible.

```python
from motionless import VisibleMap
vmap = VisibleMap(maptype='terrain')
vmap.add_address('Sugarbowl, Truckee, CA')
vmap.add_address('Tahoe City, CA')
print(vmap.generate_url())
```

![Sugarbowl and Tahoe City](http://maps.google.com/maps/api/staticmap?maptype=terrain&format=png&scale=1&size=400x400&sensor=false&visible=Sugarbowl%2C%20Truckee%2C%20CA|Tahoe%20City%2C%20CA&language=en)

DecoratedMap
============

DecoratedMaps contain markers and/or paths. They are automatically sized and 
zoomed to make the specified elements visible. 

```python
from motionless import DecoratedMap, LatLonMarker
dmap = DecoratedMap(maptype='satellite')
dmap.add_marker(LatLonMarker(27.988056, 86.925278, label='S'))
dmap.add_marker(LatLonMarker(28.007222, 86.859444, label='B'))
print(dmap.generate_url())
```

![Everest Basecamp](https://maps.google.com/maps/api/staticmap?maptype=satellite&format=png&scale=1&size=400x400&sensor=false&language=en&markers=|label:B|28.007222,86.859444&markers=|label:S|27.988056,86.925278)

You can add a list of [style definitions](https://developers.google.com/maps/documentation/static-maps/intro#StyledMaps) 
to add custom styling to your map.

```python
from motionless import DecoratedMap, AddressMarker
road_styles = [{
    'feature': 'road.highway',
    'element': 'geomoetry',
    'rules': {
        'visibility': 'simplified',
        'color': '#c280e9'
    }
}, {
    'feature': 'transit.line',
    'rules': {
        'visibility': 'simplified',
        'color': '#bababa'
    }
}]
dmap = DecoratedMap(style=road_styles)
dmap.add_marker(AddressMarker('1 Infinite Loop, Cupertino, CA',label='A'))
dmap.add_marker(AddressMarker('1600 Amphitheatre Parkway Mountain View, CA',label='G'))
print(dmap.generate_url())
```

![Apple and Google](http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&scale=1&size=400x400&sensor=false&language=en&markers=|label:G|1600%20Amphitheatre%20Parkway%20Mountain%20View%2C%20CA&markers=|label:A|1%20Infinite%20Loop%2C%20Cupertino%2C%20CA&style=feature:road.highway|element:geomoetry|visibility:simplified|color:0xc280e9|&style=feature:transit.line|element:all|visibility:simplified|color:0xbababa|)


Further examples
================


![Munich](http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&scale=1&size=640x640&sensor=false&language=en&markers=|color:red|label:E|48.351883,11.791474&markers=|color:green|label:S|48.167051,11.565088&path=color:blue|weight:8|enc:as%7EdHwxqeAc%40VPL_%40M%7DCOuBBgGn%40qDX%7BFmAoHyBcGaDeCwC%7BDwAeBwHaCcNK_AKcBD%7BBC_FEcAnCasA%7EDcOXNp%40Et%40DXCf%40IRSR%5DL%5DJgABe%40%3Fi%40QwAa%40mAy%40_AcN%7DKmHoGmGiGwHiKmEmLwBsK%7DByO%7BC%7DK_FoK_HsI_JoGgJcEeJsD%7BUaJge%40aRko%40oWiQ_Hym%40qVuf%40yRc%5C_Ncp%40gW%7D%7B%40w%5Dqd%40%7BPwP_CgPHyQnC%7Bz%40dSwo%40%60PwSjHek%40jVm%5BpN_k%40vX_HjDiK%60FuLnGiIlDoGjDcJhCkGm%40cIaEeFeGyEkLqIqTmIcUsJyVkFyQyFkUcJmc%40aHwd%40sEsd%40sDkj%40qA_e%40Ye%60%40Kad%40_Amf%40cC_%5CgDwTiHaX_KeU%7DKmPmOiQkNuRgJoRiGiRgJySuBwKYsJv%40mWa%40oUiCkv%40mAq%60%40aAqX%7D%40eZo%40%7B%5Dg%40mZHiFRmBNu%40Nq%40l%40%7BAVm%40rA%7BB%60AaAb%40WrBq%40xJyBx%40%5Bn%40i%40%7C%40yAN%5Df%40mBNoA%3FmCm%40aPI%7DRc%40cPq%40qS%5DiA%3Fq%40COGMGIM%3FOJENq%40TmHTgDNW%5CA%7D%40KsA_%40a%40c%40B)

Produced from parsing GPX file. See [examples/munich.py](http://github.com/ryancox/motionless/blob/master/examples/munich.py)

![Earthquakes](http://maps.google.com/maps/api/staticmap?maptype=roadmap&format=png&scale=1&size=640x440&sensor=false&language=en&markers=|size:small|color:yellow|-37.3966,179.2975|18.1886,-68.0525|40.7350006,-121.5250015|59.6106,-152.614|23.1201,92.7926|36.3268,-97.5206|19.0485,-67.8165|61.527,-140.6969|22.8923,94.5887|58.4735,-142.7151|38.7783318,-122.7251663|18.5077,-66.8375|7.0757,92.4647|22.2016,143.8421|16.1949,-61.5038|-4.655,152.8474|36.8669,141.4995|43.5941,11.0652|56.7258,-158.2067|-15.6005,-175.2807|37.1526,-97.8354|19.2084,-64.5278|-4.8954,-81.2859|58.9019,-154.4725|39.0330009,-122.591835|7.8674,137.2171|18.9843,-65.3223|17.8446,-65.6494|36.6558,58.6261|-16.7046,-173.882|61.4964,-151.3278|-6.629,154.8844&markers=|size:small|color:orange|-15.6259,-174.9113)

Produced from geojson feed. See [examples/earthquakes.py](http://github.com/ryancox/motionless/blob/master/examples/earthquakes.py)
