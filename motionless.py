import base64
import hmac
import hashlib
import re
from six.moves.urllib.parse import quote, urlparse
from gpolyencode import GPolyEncoder

"""
    motionless is a library that takes the pain out of generating Google Static Map URLs.

    For example code and documentation see:
        http://github.com/ryancox/motionless

    For details about the GoogleStatic Map API see:
        http://code.google.com/apis/maps/documentation/staticmaps/

    If you encounter problems, log an issue on github. 

      Copyright 2010 Ryan A Cox - ryan.a.cox@gmail.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""


__author__ = "Ryan Cox <ryan.a.cox@gmail.com>"
__version__ = "1.3.3"


class Color(object):
    COLORS = ['black', 'brown', 'green', 'purple',
              'yellow', 'blue', 'gray', 'orange', 'red', 'white']
    pat = re.compile("0x[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8}")

    @staticmethod
    def is_valid_color(color):
        return Color.pat.match(color) or color in Color.COLORS

class Marker(object):
    SIZES = ['tiny', 'mid', 'small']
    LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def __init__(self, size, color, label, icon_url):
        if size and size not in Marker.SIZES:
            raise ValueError(
                "[%s] is not a valid marker size. Valid sizes include %s" %
                (size, Marker.SIZES))
        if label and (len(label) != 1 or not label in Marker.LABELS):
            raise ValueError(
                "[%s] is not a valid label. Valid labels are a single character 'A'..'Z' or '0'..'9'" % label)
        if color and not Color.is_valid_color(color):
            raise ValueError(
                "[%s] is not a valid color. Valid colors include %s" %
                (color, Color.COLORS))
        if icon_url and not self.check_icon_url(icon_url):
            raise ValueError(
                "[%s] is not a valid url." % icon_url
            )
        self.size = size
        self.color = color
        self.label = label
        self.icon_url = quote(icon_url) if icon_url else None

    def check_icon_url(self, url):
        result = urlparse(url)
        return result.scheme and result.netloc


class AddressMarker(Marker):

    def __init__(self, address, size=None, color=None, label=None, icon_url=None):
        Marker.__init__(self, size, color, label, icon_url)
        self.address = address


class LatLonMarker(Marker):

    def __init__(self, lat, lon, size=None, color=None, label=None, icon_url=None):
        Marker.__init__(self, size, color, label, icon_url)
        self.latitude = lat
        self.longitude = lon


class Map(object):
    MAX_URL_LEN = 8192  # https://developers.google.com/maps/documentation/static-maps/intro#url-size-restriction

    def __init__(self, size_x, size_y, maptype, zoom=None, scale=1, key=None, language='en', style=None, clientid=None, secret=None, channel=None):
        if key is not None and clientid is not None:
            raise ValueError('Only one of key and clientid may be passed')
        if channel is not None and clientid is None:
            raise ValueError('Must pass clientid if channel is passed')
        if clientid is not None and secret is None:
            raise ValueError('Must pass secret if clientid is passed')
        self.base_url = 'https://maps.googleapis.com'
        self.url_path = '/maps/api/staticmap?'
        self.size_x = size_x
        self.size_y = size_y
        self.sensor = False
        self.format = 'png'
        self.maptype = maptype
        self.zoom = zoom
        self.scale = scale
        self.key = key
        self.clientid = clientid
        self.secret = secret
        self.channel = channel
        self.language = language
        self.style = style

    def __str__(self):
        return self.generate_url()

    def _get_sensor(self):
        if self.sensor:
            return 'true'
        else:
            return 'false'

    def _get_key(self):
        if self.key:
            return ''.join(['key=', self.key, '&'])
        elif self.clientid:
            return ''.join(['client=', self.clientid, '&'])
        else:
            return ''

    def _sign(self, url):
        if self.secret:
            decoded_key = base64.urlsafe_b64decode(self.secret)
            # (normalise URL before signing - fails Google's signature checks otherwise)
            signature = hmac.new(decoded_key, url.replace('%7E', '~').encode('utf-8'), hashlib.sha1)
            return url + '&signature=' + base64.urlsafe_b64encode(signature.digest()).decode('utf-8')
        else:
            return url

    def _check_url(self, url):
        if len(url) > Map.MAX_URL_LEN:
            raise ValueError(
                "Generated URL is %s characters in length. Maximum is %s" %
                (len(url), Map.MAX_URL_LEN))


class CenterMap(Map):

    def __init__(self, address=None, lat=None, lon=None, zoom=17, size_x=400,
                 size_y=400, maptype='roadmap', scale=1, key=None, style=None, language='en', clientid=None, secret=None, channel=None):
        Map.__init__(self, size_x=size_x, size_y=size_y, maptype=maptype,
                     zoom=zoom, scale=scale, key=key, style=style, language=language, clientid=clientid, secret=secret, channel=channel)
        if address:
            self.center = quote(address)
        elif lat and lon:
            self.center = "%s,%s" % (lat, lon)
        else:
            self.center = "1600 Amphitheatre Parkway Mountain View, CA"

    def generate_url(self):
        query = "%smaptype=%s&format=%s&scale=%s&center=%s&zoom=%s&size=%sx%s&sensor=%s&language=%s" % (
            self._get_key(),
            self.maptype,
            self.format,
            self.scale,
            self.center,
            self.zoom,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            self.language)
        if self.channel:
            query += '&channel=%s' % (self.channel)

        url = self.base_url + self._sign(self.url_path + quote(query, safe='/&=%'))

        self._check_url(url)
        return url


class VisibleMap(Map):

    def __init__(self, size_x=400, size_y=400, maptype='roadmap', scale=1, key=None, style=None, language='en', clientid=None, secret=None, channel=None):
        Map.__init__(self, size_x=size_x, size_y=size_y, maptype=maptype, scale=scale, key=key, style=style, language=language, clientid=clientid, secret=secret, channel=channel)
        self.locations = []

    def add_address(self, address):
        self.locations.append(quote(address))

    def add_latlon(self, lat, lon):
        self.locations.append("%s,%s" % (quote(lat), quote(lon)))

    def generate_url(self):
        query = "%smaptype=%s&format=%s&scale=%s&size=%sx%s&sensor=%s&visible=%s&language=%s" % (
            self._get_key(),
            self.maptype,
            self.format,
            self.scale,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            "|".join(self.locations),
            self.language)
        if self.channel:
            query += '&channel=%s' % (self.channel)

        url = self.base_url + self._sign(self.url_path + quote(query, safe='/&=%'))

        self._check_url(url)

        return url


class DecoratedMap(Map):

    METERS_PER_DEGREE = 111111.0

    def __init__(self, lat=None, lon=None, zoom=None, size_x=400, size_y=400,
                 maptype='roadmap', scale=1, region=False, fillcolor='green',
                 pathweight=None, pathcolor=None, key=None, style=None,
                 simplify_threshold_meters=1.11111, language='en', clientid=None, secret=None, channel=None):
        Map.__init__(self, size_x=size_x, size_y=size_y, maptype=maptype,
                     zoom=zoom, scale=scale, key=key, style=style, language=language, clientid=clientid, secret=secret, channel=channel)
        self.markers = []
        self.fillcolor = fillcolor
        self.pathweight = pathweight
        self.pathcolor = pathcolor
        self.region = region
        self.path = []
        self.contains_addresses = False
        if simplify_threshold_meters is None:
            self.simplify_threshold = 0
        else:
            self.simplify_threshold = simplify_threshold_meters / DecoratedMap.METERS_PER_DEGREE
        if lat and lon:
            self.center = "%s,%s" % (lat, lon)
        else:
            self.center = None

    def check_parameters(self):
        if self.region and len(self.path) < 2:
            raise ValueError(
                "At least two path elements required if region is enabled")

        if self.region and self.path[0] != self.path[-1]:
            raise ValueError(
                "If region enabled, first and last path entry must be identical")

        if len(self.path) == 0 and len(self.markers) == 0:
            raise ValueError("Must specify points in path or markers")

        if not Color.is_valid_color(self.fillcolor):
            raise ValueError(
                "%s is not a valid fill color. Must be 24 or 32 bit value or one of %s" %
                (self.fillcolor, Color.COLORS))

        if self.pathcolor and not Color.is_valid_color(self.pathcolor):
            raise ValueError(
                "%s is not a valid path color. Must be 24 or 32 bit value or one of %s" %
                (self.pathcolor, Color.COLORS))

    def _generate_markers(self):
        styles = set()
        data = {}
        ret = []
        # build list of unique styles
        for marker in self.markers:
            styles.add((marker.size, marker.color, marker.label, marker.icon_url))
        # setup styles/location dict
        for style in styles:
            data[style] = []
        # populate styles/location dict
        for marker in self.markers:
            if isinstance(marker, AddressMarker):
                data[(marker.size, marker.color, marker.label, marker.icon_url)
                     ].append(quote(marker.address))
            if isinstance(marker, LatLonMarker):
                location = "%s,%s" % (marker.latitude, marker.longitude)
                data[(marker.size, marker.color, marker.label, marker.icon_url)
                     ].append(location)
        # build markers entries for URL
        for style in data:
            locations = data[style]
            parts = []
            parts.append("markers=")
            if style[0]:
                parts.append("size:%s" % style[0])
            if style[1]:
                parts.append("color:%s" % style[1])
            if style[2]:
                parts.append("label:%s" % style[2])
            if style[3]:
                parts.append("icon:%s" % style[3])
            for location in locations:
                parts.append(location)
            ret.append("|".join(parts))
        return "&".join(ret)

    def _polyencode(self):
        encoder = GPolyEncoder(threshold=self.simplify_threshold)
        points = []
        for point in self.path:
            tokens = point.split(',')
            points.append((float(tokens[1]), float(tokens[0])))
        return encoder.encode(points)['points']

    def add_marker(self, marker):
        if not isinstance(marker, Marker):
            raise ValueError("Must pass instance of Marker to add_marker")
        self.markers.append(marker)

    def add_path_address(self, address):
        self.contains_addresses = True
        self.path.append(quote(address))

    def add_path_latlon(self, lat, lon):
        self.path.append("%s,%s" % (quote(str(lat)), quote(str(lon))))

    def generate_url(self):
        self.check_parameters()
        query = "%smaptype=%s&format=%s&scale=%s&size=%sx%s&sensor=%s&language=%s" % (
            self._get_key(),
            self.maptype,
            self.format,
            self.scale,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            self.language)

        if self.center:
            query = "%s&center=%s" % (query, self.center)

        if self.zoom:
            query = "%s&zoom=%s" % (query, self.zoom)

        if len(self.markers) > 0:
            query = "%s&%s" % (query, self._generate_markers())

        if len(self.path) > 0:
            query = "%s&path=" % query

            if self.pathcolor:
                query = "%scolor:%s|" % (query, self.pathcolor)

            if self.pathweight:
                query = "%sweight:%s|" % (query, self.pathweight)

            if self.region:
                query = "%sfillcolor:%s|" % (query, self.fillcolor)

            query = "%senc:%s" % (query, quote(self._polyencode()))

        if self.style:
            for style_map in self.style:
                query = "%s&style=feature:%s|element:%s|" % (
                    query,
                    (style_map['feature'] if 'feature' in style_map else 'all'),
                    (style_map['element'] if 'element' in style_map else 'all'))
                for prop, rule in style_map['rules'].items():
                    query = "%s%s:%s|" % (query, prop, str(rule).replace('#', '0x'))

        if self.channel:
            query += '&channel=%s' % (self.channel)

        url = self.base_url + self._sign(self.url_path + quote(query, safe='/&=%'))

        self._check_url(url)

        return url
