import numpy as np
import math


def calc_distance(lat1, long1, lat2, long2):
    """
        This function is responsible for calculating the distance between two points based
        on their latitudes and longitudes

        Caclulation formula -
           https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    """



    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    long_delta_rad = math.radians(long2 - long1)

    earth_rad = 6371

    distance = math.acos(math.sin(lat1_rad) * math.sin(lat2_rad) +
                         math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(long_delta_rad)) * earth_rad
    return distance


def has_invalid_props(qp):
    """This function is a helper function for checking the properties of the features from the geojson to
        determine if all the necessary properties exist"""

    # flag starts out as false
    flag = False

    # if any of the if statements hit, flag will be true
    if qp['mag'] is None:
        flag = True
    elif qp['time'] is None:
        flag = True
    elif qp['felt'] is None:
        flag = True
    elif qp['sig'] is None:
        flag = True
    elif qp['type'] is None:
        flag = True

    return flag


class QuakeData:
    """This class respresents the data from the geojson file given as a param. """

    def __init__(self, geojson):

        valid_quakes = []

        # loop through features
        for quake in geojson['features']:

            # isolate quake properties
            qp = quake['properties']

            # skip if not a features
            if quake['type'] != 'Feature':
                continue
            # skip if there are missing props
            if has_invalid_props(qp):
                continue
            # skip if geomerty type does not equal point
            if quake['geometry']['type'] != "Point":
                continue
            # skip if geometry coordinates are not a list
            if not isinstance(quake['geometry']['coordinates'], list):
                continue
            # skip if geometry coordinates list is not of length 3
            if len(quake['geometry']['coordinates']) != 3:
                continue
            coords = quake['geometry']['coordinates']
            for coord in coords:
                # for each coord, skip if it is not a number
                if type(coord) is not int or type(coord) is not float:
                    continue

            # create quake obj
            valid_quake = Quake(
                qp['mag'], qp['time'], int(qp['felt']), int(qp['sig']), qp['type'],
                (coords[0], coords[1]))

            # quake is valid, add to list
            valid_quakes.append(
                (valid_quake, float(qp['mag']), int(qp['felt']), int(qp['sig']), float(coords[0]), float(coords[1])))

        # create structured array
        self.quake_array = np.array(valid_quakes, dtype=[
            ('quake', 'O'),
            ('magnitude', 'float64'),
            ('felt', 'int32'),
            ('significance', 'int32'),
            ('lat', 'float64'),
            ('long', 'float64')
        ])
        # set filters to 0 as default
        self.location_filter = (0.0, 0.0, 0)
        self.property_filter = (0.0, 0, 0)

    def set_location_filter(self, latitude=0.0, longitude=0.0, distance=0):
        """This function is responsible for setting the Location Filter for the Quake Data obj"""

        self.location_filter = (latitude, longitude, distance)

        msg = "Location filter has been updated --> "
        msg += f"(Latitude: {latitude}, Longitude: {longitude}, Distance: {distance})"
        print(msg)

    def set_property_filter(self, magnitude=0.0, felt=0, significance=0):
        """This function is responsible for setting the Property Filter for the Quake Data obj"""

        if magnitude == 0.0 and felt == 0 and significance == 0:
            raise ValueError("At least one parameter must be supplied")

        self.property_filter = (magnitude, felt, significance)

        msg = "Property filter has been updated -->  "
        msg += f"(Magnitude: {magnitude}, Felt: {felt}, Significance: {significance})"
        print(msg)

    def clear_filters(self):
        """This function is responsible for resetting the Location Filter and Property Filter for the Quake Data obj"""

        self.location_filter = (0.0, 0.0, 0)
        self.property_filter = (0.0, 0, 0)

        # printout to display that filter reset was successful
        msg = "Location filter has been reset -->  "
        msg += f"(Latitude: {self.location_filter[0]}, "
        msg += f"Longitude: {self.location_filter[1]}, "
        msg += f"Distance: {self.location_filter[2]})\n"
        msg += "Property filter has been reset -->  "
        msg += f"(Magnitude: {self.property_filter[0]}, "
        msg += f"Felt: {self.property_filter[1]}, "
        msg += f"Significance: {self.property_filter[2]})\n"
        print(msg)

    def get_filtered_array(self):
        """This function is responsible for applying the Location/Property filters, and filtering the quakes
            based on which quakes meet the specified criteria"""

        filtered_quakes = []

        for quake in self.quake_array:

            # isolate the Quake obj
            q = quake[0]

            mag = float(q.mag)
            sig = int(q.sig)
            felt = int(q.felt)

            # variables for filter values
            lat_f, long_f, dist_f = self.location_filter
            mag_f, felt_f, sig_f = self.property_filter

            # ensure each property is valid
            if q.get_distance_from(float(lat_f), float(long_f)) >= int(dist_f):
                if mag >= mag_f:
                    if sig >= sig_f:
                        if felt >= felt_f:
                            filtered_quakes.append(q)

        return filtered_quakes

    def get_filtered_list(self):
        """This function is responsible for returning a list of the filtered Quake objects"""

        quake_list = [quake for quake in self.get_filtered_array()]
        return quake_list


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

    def get_distance_from(self, latitude, longitude):
        return calc_distance(self.lat, self.long, latitude, longitude)
