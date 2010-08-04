from motionless import AddressMarker, LatLonMarker,DecoratedMap, CenterMap, VisibleMap
import xml.sax

import urllib2

class QuakeHandler(xml.sax.handler.ContentHandler):
    
    def __init__(self,gmap):
        self.content = []
        self.gmap = gmap
        self.qname_point = (u'http://www.georss.org/georss',u'point')
        self.qname_title = (u'http://www.w3.org/2005/Atom', u'title')
        self.qname_entry = (u'http://www.w3.org/2005/Atom', u'entry')


    def startElementNS(self, qname, name, attrs):
        if qname in (self.qname_point,self.qname_title):
            self.capture = True
        else:
            self.capture = False

    def endElementNS(self, qname, name):
        element = ''.join(self.content)
        if qname == self.qname_point:
            self.tokens = element.split()
        if qname == self.qname_title:
            element = ''.join(self.content)
            magnitude = element[2]
            if magnitude in ['2','3','4']:
                self.color = 'yellow'
                self.size = 'small'
            if magnitude in ['5','6']:
                self.color = 'orange'
                self.size = 'small'
            if magnitude in ['7','8','9']:
                self.color = 'red'
                self.size = 'mid'

        if qname == self.qname_entry:
            self.gmap.add_marker(LatLonMarker(self.tokens[0],self.tokens[1],color=self.color,size=self.size))

        self.content = []

    def characters(self, ch):
        if self.capture:
            self.content.append(ch)

quake = DecoratedMap(size_x=640,size_y=440)
parser = xml.sax.make_parser()
parser.setContentHandler(QuakeHandler(quake))
parser.setFeature(xml.sax.handler.feature_namespaces, 1)

opener = urllib2.urlopen( 'http://earthquake.usgs.gov/earthquakes/catalogs/1day-M2.5.xml')
parser.feed(opener.read())

htmlPage = """
<html>
<body>
<h2>Earthquakes 2.5+ today</h2>
<i>GeoRSS feed parsed and visualized. Colors assigned to markers based on magnitued. Details can be found on <a href='http://earthquake.usgs.gov/earthquakes/catalogs/'>USGS web site</a>.
<p/>
<p/>
<img src="%s"/>
</body>
</html>	
""" % quake.generate_url()
	 

html = open("earthquakes.html","w")
html.write(htmlPage)
html.close()
print "earthquakes.html file created"
