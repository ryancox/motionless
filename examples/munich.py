from motionless import AddressMarker, LatLonMarker,DecoratedMap, CenterMap, VisibleMap
import xml.sax

class GPXHandler(xml.sax.handler.ContentHandler):
    
    def __init__(self,gmap):
        self.gmap = gmap
        self.first = True 
        self.prev = None

    def startElement(self, name, attrs):
        if name == 'trkpt': 
	    self.gmap.add_path_latlon(attrs['lat'],attrs['lon'])
            self.prev = (attrs['lat'],attrs['lon'])
            if self.first:
                self.first = False
                self.gmap.add_marker(LatLonMarker(attrs['lat'],attrs['lon'],color='green',label='S'))

    def endElement(self,name):
        if name == 'trk':
            self.gmap.add_marker(LatLonMarker(self.prev[0],self.prev[1],color='red',label='E'))
        
munich = DecoratedMap(size_x=640,size_y=640,pathweight=8,pathcolor='blue')
parser = xml.sax.make_parser()
parser.setContentHandler(GPXHandler(munich))
parser.feed(open('Current.gpx').read())

htmlPage = """
<html>
<body>
<h2>Munich</h2>
<i>Trip from Schwabing (S) to Airport (E). Current.gpx file taken of my Garmin device and edited down to single track.</i>
<p/>
<p/>
<img src="%s"/>
</body>
</html>	
""" % munich.generate_url()


html = open("munich.html","w")
html.write(htmlPage)
html.close()
print "munich.html file created"

