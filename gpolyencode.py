"""
= py-gpolyencode : python modules for Google Maps polyline encoding =

Python port of the Javascript Google Maps polyline encoder from Mark
McClure, released under a BSD license. Both a pure python (gpolyencode) and
a C++ extension (cgpolyencode) are implemented, with numerous unit tests.

  * Homepage:                   http://code.google.com/p/py-gpolyencode/
  * Google Maps documentation:  http://code.google.com/apis/maps/documentation/overlays.html#Encoded_Polylines
  * Additional information:     http://facstaff.unca.edu/mcmcclur/GoogleMaps/EncodePolyline/

Redistributed with permission (and slight modifications for py3 compatibility):

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
import math
from six import StringIO


class GPolyEncoder(object):

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
