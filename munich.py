from motionless import DecoratedMap,LatLonMarker
import urllib2
import xml.sax

"""
    Note:
        Assumes single 'trk'
        May exceed max url length if gpolyencode not avaiable
"""

class Handler(xml.sax.handler.ContentHandler):
    
    def __init__(self,map):
        self.map = map
        self.first = True 
        self.prev = None

    def startElement(self, name, attrs):
        if name == 'trkpt': 
            map.add_path_latlon(attrs['lat'],attrs['lon'])
            self.prev = (attrs['lat'],attrs['lon'])
            if self.first:
                self.first = False
                map.add_marker(LatLonMarker(attrs['lat'],attrs['lon'],color='green',label='S'))

    def endElement(self,name):
        if name == 'trk':
            map.add_marker(LatLonMarker(self.prev[0],self.prev[1],color='red',label='E'))
        
map = DecoratedMap(size_x=640,size_y=640)
parser = xml.sax.make_parser()
parser.setContentHandler(Handler(map))
parser.feed(open('Current.gpx').read())
print map.generate_url()
