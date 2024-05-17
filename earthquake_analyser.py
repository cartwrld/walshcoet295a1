import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path
from earthquakes import QuakeData, Quake


def print_menu():
    menu = "\n==================================================================\n"
    menu += "|\t\t           Earthquake Analyser Menu\t\t\t             |\n"
    menu += "==================================================================\n"
    menu += "|                                                                |\n"
    menu += "|\t1)\tSet Location Filter\t\t5)\tDisplay Exceptional Quakes\t |\n"
    menu += "|\t2)\tSet Property Filter\t\t6)\tDisplay Magnitude Stats\t\t |\n"
    menu += "|\t3)\tClear Filters\t\t\t7)\tPlot Quake Map\t\t\t\t |\n"
    menu += "|\t4)\tDisplay Quakes\t\t\t8)\tPlot Magnitude Chart\t\t |\n"
    menu += "|                                                                |\n"
    menu += "|\t\t\t\t\t\t9)\tQuit                                 |\n"
    menu += "==================================================================\n"

    print(menu)


def set_location_filter(qd):
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


def set_property_filter(qd):
    mag = input("Please enter the Magnitude:\t")
    felt = input("Please enter the Felt value:\t")
    sig = input("Please enter the Significance:\t")

    if mag == "":
        mag = 0
    if felt == "":
        felt = 0
    if sig == "":
        sig = 0

    qd.set_property_filter(mag, felt, sig)


def clear_filters(qd):
    qd.location_filter = (0.0, 0.0, 0.0)
    qd.property_filter = (0.0, 0.0, 0.0)


def display_quakes(qd):
    for quake in qd.get_filtered_array():
        print(quake)


def display_exceptional_quakes(qd):
    mags = [quake.mag for quake in qd.quake_array]

    median = np.median(mags)
    std_dev = np.std(mags)
    threshold = median + std_dev

    exceptional_quakes = [quake for quake in qd.quake_array if quake.mag >= threshold]

    for eq in exceptional_quakes:
        print(eq)


def display_magnitude_stats(qd):
    mags = [quake.mag for quake in qd.quake_array]

    mean_val = np.mean(mags)
    median_val = np.median(mags)
    std_dev = np.std(mags)

    stats_header = "\n---------------------------------------\n"
    stats_header += "|\tEarthquake Magnitude Statistics\t  |\n"
    stats_header += "|-------------------------------------|\n"
    stats_header += "|\tMean\t|\tMedian\t|\tStd.Dev\t  |\n"
    stats_header += "|-------------------------------------|\n"
    stats_header += "|\t%.2f\t|\t%.2f\t|\t%.2f\t  |\n" % (mean_val, median_val, std_dev)
    stats_header += "---------------------------------------"

    print(stats_header)


def plot_quake_map(qd):
    lats = [quake.lat for quake in qd.quake_array]
    longs = [quake.long for quake in qd.quake_array]
    magnitudes = [quake.mag for quake in qd.quake_array]

    plt.scatter(x=lats, y=longs, c=magnitudes)

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Earthquake Map')
    plt.show()

    plt.figure(figsize=(10, 8))
    plt.scatter(longs, lats, s=[mag ** 3.5 for mag in magnitudes], alpha=0.5)
    plt.show()


def plot_magnitude_chart(qd):
    magnitudes = [quake.mag for quake in qd.get_filtered_array()]

    whole_num_mags = []

    for mag in magnitudes:
        if mag == int(mag):
            whole_num_mags.append(mag)

    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple', 'tab:pink', 'tab:gray']

    bins = np.arange(1, 12)

    counts, _ = np.histogram(whole_num_mags, bins=bins)

    x_positions = np.arange(1, 11)

    plt.xticks(x_positions)
    plt.yticks(np.arange(15))

    plt.ylabel('Frequency')
    plt.xlabel('Magnitude')
    plt.title('Magnitude Analysis')

    plt.bar(x_positions, counts, width=0.8, edgecolor='black', color=bar_colors)

    plt.show()


def get_menu_input(qd):
    option = input("Please select an option from the menu. (1-9)\n")
    if option == '1':
        set_location_filter(qd)

    elif option == '2':
        set_property_filter(qd)

    elif option == '3':
        clear_filters(qd)

    elif option == '4':
        display_quakes(qd)

    elif option == '5':
        display_exceptional_quakes(qd)

    elif option == '6':
        display_magnitude_stats(qd)

    elif option == '7':
        plot_quake_map(qd)

    elif option == '8':
        plot_magnitude_chart(qd)

    elif option == '9':
        quit()


def analyse_earthquakes():
    path = Path("./earthquakes.geojson")

    with open(path, 'r') as file:
        data = json.load(file)

    quake_data = QuakeData(data)
    quake_data.get_filtered_array()

    while True:
        print_menu()
        get_menu_input(quake_data)


analyse_earthquakes()
