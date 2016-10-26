import re
import math
from six import StringIO
from six.moves.urllib.parse import quote, urlparse

"""
    motionless is a library that takes the pain out of generating Google Static Map URLs.

    For example code and documentation see:
        http://github.com/ryancox/motionless

    For details about the GoogleStatic Map API see:
        http://code.google.com/apis/maps/documentation/staticmaps/

    If you encounter problems, log an issue on github. If you have questions, drop me an
    email at ryan.a.cox@gmail.com.

"""

"""

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
__version__ = "1.0"


class GPolyEncoder(object):
    """
    = py-gpolyencode : python modules for Google Maps polyline encoding =

    Python port of the Javascript Google Maps polyline encoder from Mark
    McClure, released under a BSD license. Both a pure python (gpolyencode) and
    a C++ extension (cgpolyencode) are implemented, with numerous unit tests.

      * Homepage:                   http://code.google.com/p/py-gpolyencode/
      * Google Maps documentation:  http://code.google.com/apis/maps/documentation/overlays.html#Encoded_Polylines
      * Additional information:     http://facstaff.unca.edu/mcmcclur/GoogleMaps/EncodePolyline/

    Redistributed with permission:

    == Licensing ==

    Copyright (c) 2009, Koordinates Limited
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

      * Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.
      * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
      * Neither the name of the Koordinates Limited nor the names of its
        contributors may be used to endorse or promote products derived from
        this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
    """

    def __init__(self, num_levels=18, zoom_factor=2, threshold=0.00001,
                 force_endpoints=True):
        self._num_levels = num_levels
        self._zoom_factor = zoom_factor
        self._threshold = threshold
        self._force_endpoints = force_endpoints

        self._zoom_level_breaks = []
        for i in range(num_levels):
            self._zoom_level_breaks.append(
                threshold * (zoom_factor ** (num_levels - i - 1)))

    def encode(self, points):
        dists = {}
        # simplify using Douglas-Peucker
        max_dist = 0
        abs_max_dist = 0
        stack = []
        if (len(points) > 2):
            stack.append((0, len(points) - 1))
            while len(stack):
                current = stack.pop()
                max_dist = 0

                for i in range(current[0] + 1, current[1]):
                    temp = self._distance(points[i], points[current[0]],
                                          points[current[1]])
                    if temp > max_dist:
                        max_dist = temp
                        max_loc = i
                        abs_max_dist = max(abs_max_dist, max_dist)

                if max_dist > self._threshold:
                    dists[max_loc] = max_dist
                    stack.append((current[0], max_loc))
                    stack.append((max_loc, current[1]))

        enc_points, enc_levels = self._encode(points, dists, abs_max_dist)
        r = {
            'points': enc_points,
            'levels': enc_levels,
            'zoomFactor': self._zoom_factor,
            'numLevels': self._num_levels,
        }
        return r

    def _encode(self, points, dists, abs_max_dist):
        encoded_levels = StringIO()
        encoded_points = StringIO()

        plat = 0
        plng = 0

        if (self._force_endpoints):
            encoded_levels.write(self._encode_number(self._num_levels - 1))
        else:
            encoded_levels.write(self._encode_number(
                self._num_levels - self._compute_level(abs_max_dist) - 1))

        n_points = len(points)
        for i, p in enumerate(points):
            if (i > 0) and (i < n_points - 1) and (i in dists):
                encoded_levels.write(self._encode_number(
                    self._num_levels - self._compute_level(dists[i]) - 1))

            if (i in dists) or (i == 0) or (i == n_points - 1):
                late5 = int(math.floor(p[1] * 1E5))
                lnge5 = int(math.floor(p[0] * 1E5))
                dlat = late5 - plat
                dlng = lnge5 - plng
                plat = late5
                plng = lnge5
                encoded_points.write(self._encode_signed_number(dlat))
                encoded_points.write(self._encode_signed_number(dlng))

        if (self._force_endpoints):
            encoded_levels.write(self._encode_number(self._num_levels - 1))
        else:
            encoded_levels.write(self._encode_number(
                self._num_levels - self._compute_level(abs_max_dist) - 1))

        return (
            encoded_points.getvalue(),  # .replace("\\", "\\\\"),
            encoded_levels.getvalue()
        )

    def _compute_level(self, abs_max_dist):
        lev = 0
        if abs_max_dist > self._threshold:
            while abs_max_dist < self._zoom_level_breaks[lev]:
                lev += 1
        return lev

    def _encode_signed_number(self, num):
        sgn_num = num << 1
        if num < 0:
            sgn_num = ~sgn_num
        return self._encode_number(sgn_num)

    def _encode_number(self, num):
        s = StringIO()
        while num >= 0x20:
            next_val = (0x20 | (num & 0x1f)) + 63
            s.write(chr(next_val))
            num >>= 5
        num += 63
        s.write(chr(num))
        return s.getvalue()

    def _distance(self, p0, p1, p2):
        out = 0.0

        if (p1[1] == p2[1] and p1[0] == p2[0]):
            out = math.sqrt((p2[1] - p0[1]) ** 2 + (p2[0] - p0[0]) ** 2)
        else:
            u = ((p0[1] - p1[1]) * (p2[1] - p1[1]) + (p0[0] - p1[0]) * (
                p2[0] - p1[0])) \
                / ((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)

            if u <= 0:
                out = math.sqrt((p0[1] - p1[1]) ** 2 + (p0[0] - p1[0]) ** 2)
            elif u >= 1:
                out = math.sqrt((p0[1] - p2[1]) ** 2 + (p0[0] - p2[0]) ** 2)
            elif (0 < u) and (u < 1):
                out = math.sqrt((p0[1] - p1[1] - u * (p2[1] - p1[1])) ** 2 \
                                + (p0[0] - p1[0] - u * (p2[0] - p1[0])) ** 2)
        return out


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
        if color and color not in Color.COLORS:
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
    MAX_URL_LEN = 2048
    MAPTYPES = ['roadmap', 'satellite', 'hybrid', 'terrain']
    FORMATS = ['png', 'png8', 'png32', 'gif', 'jpg', 'jpg-baseline']
    MAX_X = 640
    MAX_Y = 640
    ZOOM_RANGE = list(range(1, 21))
    SCALE_RANGE = list(range(1, 5))

    def __init__(self, size_x, size_y, maptype, zoom=None, scale=1, key=None, language='en', style=None):
        self.base_url = 'https://maps.google.com/maps/api/staticmap?'
        self.size_x = size_x
        self.size_y = size_y
        self.sensor = False
        self.format = 'png'
        self.maptype = maptype
        self.zoom = zoom
        self.scale = scale
        self.key = key
        self.language = language
        self.style = style

    def __str__(self):
        return self.generate_url()

    def check_parameters(self):
        if self.format not in Map.FORMATS:
            raise ValueError(
                "[%s] is not a valid file format. Valid formats include %s" %
                (self.format, Map.FORMATS))

        if self.maptype not in Map.MAPTYPES:
            raise ValueError(
                "[%s] is not a valid map type. Valid types include %s" %
                (self.maptype, Map.MAPTYPES))

        if self.size_x > Map.MAX_X or self.size_x < 1:
            raise ValueError(
                "[%s] is not a valid x-dimension. Must be between 1 and %s" %
                (self.size_x, Map.MAX_X))

        if self.size_y > Map.MAX_Y or self.size_y < 1:
            raise ValueError(
                "[%s] is not a valid y-dimension. Must be between 1 and %s" %
                (self.size_y, Map.MAX_Y))

        if self.zoom is not None and self.zoom not in Map.ZOOM_RANGE:
            raise ValueError(
                "[%s] is not a zoom setting. Must be between %s and %s" %
                (self.zoom, min(Map.ZOOM_RANGE), max(Map.ZOOM_RANGE)))

        if self.scale is not None and self.scale not in Map.SCALE_RANGE:
            raise ValueError(
                "[%s] is not a scale setting. Must be between %s and %s" %
                (self.scale, min(Map.SCALE_RANGE), max(Map.SCALE_RANGE)))

    def _get_sensor(self):
        if self.sensor:
            return 'true'
        else:
            return 'false'

    def _get_key(self):
        if self.key:
            return ''.join(['key=', self.key, '&'])
        else:
            return ''

    def _check_url(self, url):
        if len(url) > Map.MAX_URL_LEN:
            raise ValueError(
                "Generated URL is %s characters in length. Maximum is %s" %
                (len(url), Map.MAX_URL_LEN))


class CenterMap(Map):

    def __init__(self, address=None, lat=None, lon=None, zoom=17, size_x=400,
                 size_y=400, maptype='roadmap', scale=1, key=None, style=None):
        Map.__init__(self, size_x=size_x, size_y=size_y, maptype=maptype,
                     zoom=zoom, scale=scale, key=key, style=style)
        if address:
            self.center = quote(address)
        elif lat and lon:
            self.center = "%s,%s" % (lat, lon)
        else:
            self.center = "1600 Amphitheatre Parkway Mountain View, CA"

    def check_parameters(self):
        super(CenterMap, self).check_parameters()

    def generate_url(self):
        self.check_parameters()
        url = "%s%smaptype=%s&format=%s&scale=%s&center=%s&zoom=%s&size=%sx%s&sensor=%s&language=%s" % (
            self.base_url,
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

        self._check_url(url)
        return url


class VisibleMap(Map):

    def __init__(self, size_x=400, size_y=400, maptype='roadmap', scale=1, key=None, style=None):
        Map.__init__(self, size_x=size_x, size_y=size_y, maptype=maptype, scale=scale, key=key, style=style)
        self.locations = []

    def add_address(self, address):
        self.locations.append(quote(address))

    def add_latlon(self, lat, lon):
        self.locations.append("%s,%s" % (quote(lat), quote(lon)))

    def generate_url(self):
        self.check_parameters()
        url = "%s%smaptype=%s&format=%s&scale=%s&size=%sx%s&sensor=%s&visible=%s&language=%s" % (
            self.base_url,
            self._get_key(),
            self.maptype,
            self.format,
            self.scale,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            "|".join(self.locations),
            self.language)

        self._check_url(url)
        return url


class DecoratedMap(Map):

    def __init__(self, lat=None, lon=None, zoom=None, size_x=400, size_y=400,
                 maptype='roadmap', scale=1, region=False, fillcolor='green',
                 pathweight=None, pathcolor=None, key=None, style=None):
        Map.__init__(self, size_x=size_x, size_y=size_y, maptype=maptype,
                     zoom=zoom, scale=scale, key=key, style=style)
        self.markers = []
        self.fillcolor = fillcolor
        self.pathweight = pathweight
        self.pathcolor = pathcolor
        self.region = region
        self.path = []
        self.contains_addresses = False
        if lat and lon:
            self.center = "%s,%s" % (lat, lon)
        else:
            self.center = None

    def check_parameters(self):
        super(DecoratedMap, self).check_parameters()

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
        encoder = GPolyEncoder()
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
        url = "%s%smaptype=%s&format=%s&scale=%s&size=%sx%s&sensor=%s&language=%s" % (
            self.base_url,
            self._get_key(),
            self.maptype,
            self.format,
            self.scale,
            self.size_x,
            self.size_y,
            self._get_sensor(),
            self.language)

        if self.center:
            url = "%s&center=%s" % (url, self.center)

        if self.zoom:
            url = "%s&zoom=%s" % (url, self.zoom)

        if len(self.markers) > 0:
            url = "%s&%s" % (url, self._generate_markers())

        if len(self.path) > 0:
            url = "%s&path=" % url

            if self.pathcolor:
                url = "%scolor:%s|" % (url, self.pathcolor)

            if self.pathweight:
                url = "%sweight:%s|" % (url, self.pathweight)

            if self.region:
                url = "%sfillcolor:%s|" % (url, self.fillcolor)

            url = "%senc:%s" % (url, quote(self._polyencode()))

        if self.style:
            for style_map in self.style:
                url = "%s&style=feature:%s|element:%s|" % (
                    url,
                    (style_map['feature'] if 'feature' in style_map else 'all'),
                    (style_map['element'] if 'element' in style_map else 'all'))
                for prop, rule in style_map['rules'].items():
                    url = "%s%s:%s|" % (url, prop, str(rule).replace('#', '0x'))

        self._check_url(url)

        return url
