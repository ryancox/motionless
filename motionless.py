
import urllib2
from urllib import quote 

"""
    TODO:
        include sets of valid maptypes,sizes,...
        include factories or new types: centerMap, markerMap, visibleMap,pathMap
        image format
        maptype
        paths 
        encoded polylines: http://code.google.com/p/py-gpolyencode/
        visible / viewports
        shortening urls for markers: http://github.com/bitly/bitly-api-python
        circle / radus drawing: http://code.google.com/p/geopy/
"""

class Marker:
    pass

class AddressMarker(Marker):
    def __init__(self, address, size=None, color=None, label=None):
        self.address = address
        self.size = size
        self.color = color
        self.label = label

class LatLonMarker(Marker):
    def __init__(self, lat, lon, size=None, color=None, label=None):
        self.latitude = lat
        self.longitude = lon
        self.size = size
        self.color = color
        self.label = label

class Map:
    def __init__(self):
        self.base_url = "http://maps.google.com/maps/api/staticmap?"
        self.size_x = 400
        self.size_y = 400
        self.center = quote("1600 Amphitheatre Parkway Mountain View, CA")
        self.sensor = False
        self.zoom = 16
        self.format = "png"
        self.markers = []

    def check_parameters(self):
        pass

    def _get_sensor(self):
        if self.sensor:
            return 'true'
        else:
            return 'false'

    def generate_url(self):
        self.check_parameters();
        return "%scenter=%s&zoom=%s&size=%sx%s&sensor=%s&%s&" % (
            self.base_url,
            self.center,
            self.zoom,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            self._generate_markers())

    def _generate_markers(self):
        styles = set()
        data = {}
        ret = []
        # build list of unique styles
        for marker in self.markers:
            styles.add((marker.size,marker.color,marker.label)) 
        # setup styles/location dict   
        for style in styles:
            data[style] = []
        # populate styles/location dict   
        for marker in self.markers:
            if isinstance(marker,AddressMarker):
                data[(marker.size,marker.color,marker.label)].append(quote(marker.address))
            if isinstance(marker,LatLonMarker):
                location = "%s,%s" % (marker.latitude, marker.longitude)
                data[(marker.size,marker.color,marker.label)].append(location)
        # build markers entries for URL 
        for style in data:
            locations = data[style]
            parts = []
            parts.append("markers=")
            if style[0]:
                parts.append("size:%s"%style[0])
            if style[1]:
                parts.append("color:%s"%style[1])
            if style[2]:
                parts.append("label:%s"%style[2]) 
            for location in locations: 
                parts.append(location)
            ret.append("|".join(parts))
        return "&".join(ret) 

    def download(self, filename): 
        o = urllib2.urlopen(self.generate_url())
        print o.headers
        open(filename,'wb').write(o.read())
    
    def add_marker(self, marker):
        if not isinstance(marker,Marker):
            raise  ValueError("Must pass instance of Marker to add_marker")
        self.markers.append(marker)     
