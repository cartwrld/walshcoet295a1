import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
from earthquakes import QuakeData, Quake

quakes = {}

path = Path("./earthquakes.geojson")
# path = Path("./earthquakes_copy.geojson")

with open(path, 'r') as file:
    data = json.load(file)

qd = QuakeData(data)
qd.get_filtered_array()


def print_menu():
    menu = "\n================================================\n"
    menu += "|           Earthquake Analyser Menu           |\n"
    menu += "================================================\n"
    menu += "|                                              |\n"
    menu += "|\t\t1)\tSet Location Filter                |\n"
    menu += "|\t\t2)\tSet Property Filter                |\n"
    menu += "|\t\t3)\tClear Filters                      |\n"
    menu += "|\t\t4)\tDisplay Quakes                     |\n"
    menu += "|\t\t5)\tDisplay Exceptional Quakes         |\n"
    menu += "|\t\t6)\tDisplay Magnitude Stats            |\n"
    menu += "|\t\t7)\tPlot Quake Map                     |\n"
    menu += "|\t\t8)\tPlot Magnitude Chart               |\n"
    menu += "|\t\t9)\tQuit                               |\n"
    menu += "|                                              |\n"
    menu += "================================================\n"

    print(menu)


def set_location_filter():
    lat = input("Please enter the Latitude:\t")
    lon = input("Please enter the Longitude:\t")
    dist = input("Please enter the Distance:\t")

    if lat == "":
        lat = 0
    if lon == "":
        lon = 0
    if dist == "":
        dist = 0

    qd.set_location_filter(lat, lon, dist)


def set_property_filter():
    mag = input("Please enter the Magnitude:\t")
    felt = input("Please enter the Felt value:\t")
    sig = input("Please enter the Significance:\t")

    if mag == "":
        lat = 0
    if felt == "":
        lon = 0
    if sig == "":
        dist = 0

    qd.set_property_filter(mag, felt, sig)


def clear_filters():
    QuakeData.location_filter = (0.0, 0.0, 0.0)
    QuakeData.property_filter = (0.0, 0.0, 0.0)


def display_quakes(q_data):
    for quake in q_data:
        print(quake)


def display_exceptional_quakes():
    pass


def display_magnitude_stats():
    pass


def plot_quake_map():
    # magnitudes_list = [quake.mag for quake in qd.quake_array]
    # latitudes_list = [quake.lat for quake in qd.quake_array]
    # longitudes_list = [quake.long for quake in qd.quake_array]
    #
    # lat_range = np.atleast_2d(np.arange(-150, 150)).transpose()
    # long_range = np.atleast_2d(np.arange(-150, 150)).transpose()
    #
    #
    # print(magnitudes_list)
    # print(latitudes_list)
    # print(longitudes_list)
    #
    #
    # plt.plot(long_range, lat_range, "bo", markersize=latitudes_list[, mew=2, label='Average Transistor Count')
    # plt.show()
    # Extract latitude, longitude, and magnitude for each filtered quake
    lats = [quake.lat for quake in qd.quake_array]
    longs = [quake.long for quake in qd.quake_array]
    magnitudes = [quake.mag for quake in qd.quake_array]

    plt.scatter(x=lats, y=longs, c=magnitudes)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Earthquake Map')
    plt.show()

    # Create scatter plot
    plt.figure(figsize=(10, 8))
    plt.scatter(longs, lats, s=[mag ** 3.5 for mag in magnitudes], alpha=0.5)


    # plt.show()


    #
    # plt.semilogy(a_years, a_trans, 'bo', label="Transistor Count", alpha=0.2)
    # plt.plot(year_range, mean_trans_for_each_year, "bo", markersize=14, mew=2, label='Average Transistor Count')
    # plt.show()


def plot_magnitude_chart():
    pass


def get_menu_input():
    option = input("Please select an option from the menu. (1-9)\n")
    if option == '1':
        set_location_filter()
        print("Location filter has been updated.")
    elif option == '2':
        set_property_filter()
        print("Property filter has been updated.")
    elif option == '3':
        clear_filters()
        print("Filters have been cleared.")
    elif option == '4':
        display_quakes(qd.quake_array)
    elif option == '5':
        display_exceptional_quakes()
    elif option == '6':
        display_magnitude_stats()
    elif option == '7':
        plot_quake_map()
    elif option == '8':
        plot_magnitude_chart()
    elif option == '9':
        quit()

while True:
    print_menu()
    get_menu_input()
