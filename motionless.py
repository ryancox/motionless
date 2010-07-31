
import urllib2
from urllib import quote 

"""
    TODO:
        implement param checks
        paths 
        encoded polylines: http://code.google.com/p/py-gpolyencode/
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
        self.base_url = 'http://maps.google.com/maps/api/staticmap?'
        self.size_x = 400
        self.size_y = 400
        self.sensor = False
        self.format = 'png'
        self.FORMATS = ['png','png8','png32','gif','jpg','jpg-baseline']
        self.maptype = 'roadmap' 
        self.MAPTYPES = ['roadmap','satellite','hybrid','terrain']

    def check_parameters(self):
        pass

    def _get_sensor(self):
        if self.sensor:
            return 'true'
        else:
            return 'false'

    def download(self, filename): 
        o = urllib2.urlopen(self.generate_url())
        print o.headers
        open(filename,'wb').write(o.read())
    

class CenterMap(Map):
    def __init__(self, address=None):
        Map.__init__(self)                    
        if address: 
            self.center = quote(address)
        else:
            self.center = "1600 Amphitheatre Parkway Mountain View, CA"
        self.zoom = 14

    def set_address(self,address):
        self.center = quote(address)

    def set_lat_lon(self,lat,lon):
        self.center = "%s,%s" % (lat,lon)

    def generate_url(self):
        self.check_parameters();
        return "%smaptype=%s&format=%s&center=%s&zoom=%s&size=%sx%s&sensor=%s" % (
            self.base_url,
            self.maptype,
            self.format,
            self.center,
            self.zoom,
            self.size_x,
            self.size_y,
            self._get_sensor())

class MarkerMap(Map):
    def __init__(self):
        Map.__init__(self)                    
        self.markers = []

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
                data[(marker.size,marker.color,marker.label)].append(quote(location))
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

    def add_marker(self, marker):
        if not isinstance(marker,Marker):
            raise  ValueError("Must pass instance of Marker to add_marker")
        self.markers.append(marker)     

    def generate_url(self):
        self.check_parameters();
        return "%smaptype=%s&format=%s&size=%sx%s&sensor=%s&%s&" % (
            self.base_url,
            self.maptype,
            self.format,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            self._generate_markers())

class VisibleMap(Map):
    def __init__(self):
        Map.__init__(self)                    
        self.locations = []

    def add_address(self, address):
        self.locations.append(quote(address))

    def add_lat_lon(self, lat, lon):
        self.locations.append("%s,%s" % (quote(lat),quote(lon)))

    def generate_url(self):
        self.check_parameters();
        return "%smaptype=%s&format=%s&size=%sx%s&sensor=%s&visible=%s" % (
            self.base_url,
            self.maptype,
            self.format,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            "|".join(self.locations))

class PathMap(Map):
    def __init__(self):
        Map.__init__(self)                    
        self.locations = []

    def add_address(self, address):
        self.locations.append(quote(address))

    def add_lat_lon(self, lat, lon):
        self.locations.append("%s,%s" % (quote(lat),quote(lon)))

    def generate_url(self):
        self.check_parameters();
        return "%smaptype=%s&format=%s&size=%sx%s&sensor=%s&path=%s" % (
            self.base_url,
            self.maptype,
            self.format,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            "|".join(self.locations))

class RegionMap(Map):
    pass
