import numpy as np


def calc_distance(lat1, long1, lat2, long2):
    pass


def has_invalid_props(qp):
    flag = False

    if qp['mag'] == None:
        flag = True
    elif qp['time'] == None:
        flag = True
    elif qp['felt'] == None:
        flag = True
    elif qp['sig'] == None:
        flag = True
    elif qp['type'] == None:
        flag = True
    return flag


class QuakeData:
    """"""

    location_filter = (0, 0, 0)
    property_filter = (9, 0, 0)

    def __init__(self, geojson):

        valid_quakes = []

        for quake in geojson['features']:

            qp = quake['properties']

            if quake['type'] != 'Feature':
                continue
            if has_invalid_props(qp):
                continue
            if quake['geometry']['type'] != "Point":
                continue
            if not isinstance(quake['geometry']['coordinates'], list):
                continue
            if len(quake['geometry']['coordinates']) != 3:
                continue

            # add a check to make sure they're all numbers

            else:
                valid_quakes.append(
                    Quake(qp['mag'], qp['time'], qp['felt'], qp['sig'], qp['types'],
                          (quake['geometry']['coordinates'][0], quake['geometry']['coordinates'][1])
                          ))

        self.quake_array = valid_quakes

    def set_location_filter(self, latitude, longitude, distance):
        QuakeData.location_filter = (latitude, longitude, distance)

    def set_property_filter(self, magnitude, felt, significance):
        QuakeData.property_filter = (magnitude, felt, significance)

    def clear_filters(self):
        QuakeData.location_filter = (0.0, 0.0, 0.0)
        QuakeData.property_filter = (0.0, 0.0, 0.0)

    def get_filtered_array(self):

        filtered_quakes = []

        for quake in self.quake_array:

            lat_f = self.location_filter[0]
            long_f = self.location_filter[1]
            dist_f = self.location_filter[2]

            mag_f = self.property_filter[0]
            felt_f = self.property_filter[1]
            sig_f = self.property_filter[2]

            if quake.mag >= mag_f:
                if quake.sig >= sig_f:
                    if quake.felt >= felt_f:
                        filtered_quakes.append(quake)

        return filtered_quakes

    def get_filtered_list(self):
        pass


class Quake:
    """"""

    def __init__(self, magnitude, time, felt, sig, q_type, coords):
        self.mag = magnitude
        self.time = time
        self.felt = felt
        self.sig = sig
        self.q_type = q_type
        self.lat = coords[0]
        self.long = coords[1]

    def __str__(self):
        return f"{self.mag} Magnitude Earthquake, {self.sig} Significance, felt by {self.felt} people in ({self.lat}, {self.long})"

    def get_distance_from(self, latitude, longitude, distance):
        pass
