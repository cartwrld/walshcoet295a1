import numpy as np


def calc_distance(lat1, long1, lat2, long2):
    pass


def has_invalid_props(qp):
    flag = False

    if qp['mag'] == None:
        print('failed on mag')
        flag = True
    elif qp['time'] == None:
        flag = True
        print('failed on time')
    elif qp['felt'] == None:
        flag = True
        # print('failed on felt')
    elif qp['sig'] == None:
        flag = True
        print('failed on sig')
    elif qp['type'] == None:
        flag = True
        print('failed on type')
    return flag


class QuakeData:
    """"""

    location_filter = (0, 0, 0)
    property_filter = (0, 0, 0)

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
        print(f"len of valid quakes: {len(valid_quakes)}")
        # self.get_filtered_array()
        ###################################

    def set_location_filter(self, latitude, longitude, distance):
        QuakeData.location_filter = (latitude, longitude, distance)

    def set_property_filter(self, magnitude, felt, significance):

        if magnitude == "":
            magnitude = 0
        if felt == "":
            felt = 0
        if significance == "":
            significance = 0

        QuakeData.property_filter = (magnitude, felt, significance)
        # print(QuakeData.property_filter)

    def clear_filters(self):
        QuakeData.location_filter = (0.0, 0.0, 0.0)
        QuakeData.property_filter = (0.0, 0.0, 0.0)

    def get_filtered_array(self):

        filtered_quakes = []

        for quake in self.quake_array:

            mag_f = self.property_filter[0]
            felt_f = self.property_filter[1]
            sig_f = self.property_filter[2]

            if quake.mag >= mag_f:
                if quake.sig >= sig_f:
                    if quake.felt >= felt_f:
                        print(quake)
                        filtered_quakes.append(quake)

        print(f"len of filtered: {len(filtered_quakes)}")

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
