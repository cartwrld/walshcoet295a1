import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import json
import math
import sys

from earthquakes import QuakeData


def print_menu():
    """This function is responsible for printing the menu for the user"""

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
    """This function is responsible for prompting the user to enter their desired values for the Location Filter"""

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
    """This function is responsible for prompting the user to enter their desired values for the Property Filter"""

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
    """This function is responsible for resetting the Location Filter and Property Filter."""
    qd.clear_filters()


def display_quakes(qd):
    """This function is responsible for displaying the filtered quakes"""
    for quake in qd.get_filtered_array():
        print(quake)


def display_exceptional_quakes(qd):
    """This function is responsible for displaying exceptional quakes, which are quakes that have a
    magnitude greater than or equal to one standard deviation above the median magnitude"""

    # list of all magnitudes
    quakes = [quake for quake in qd.get_filtered_list()]
    magnitudes = [q.mag for q in quakes]

    # calculate the median, std. dev, and threshold of the magnitudes
    median = np.median(magnitudes)
    std_dev = np.std(magnitudes)
    threshold = median + std_dev

    # filter for quakes that are greater than or equal to one std.dev above median
    exceptional_quakes = [quake for quake in quakes if quake.mag >= threshold]

    # print out the exceptional quakes
    for quake in exceptional_quakes:
        print(quake)


def display_magnitude_stats(qd):
    """This function is responsible for displaying the Mean, Median, and Standard Deviation of the
        magnitude values of the filtered quakes """

    # list of all magnitudes
    magnitudes = [entry[1] for entry in qd.quake_array]
    rounded_down_mags = [math.floor(mag) for mag in magnitudes]

    # calculate the mean, median, and std. dev of the magnitudes
    mean = np.mean(magnitudes)
    median = np.median(magnitudes)
    std_dev = np.std(magnitudes)

    mean_rounded = np.mean(rounded_down_mags)
    median_rounded = np.median(rounded_down_mags)
    std_dev_rounded = np.std(rounded_down_mags)

    # building the output to be displayed to the user
    stats = "\n-------------------------------------------------------\n"
    stats += "|\t\t\tEarthquake Magnitude Statistics\t          |\n"
    stats += "-------------------------------------------------------\n"
    stats += "|\t             |\t Mean\t|\tMedian\t|\tStd.Dev\t  |\n"
    stats += "|\tOriginal     |------------------------------------|\n"
    stats += "|\t             |\t %.2f\t|\t %.2f\t|\t %.2f\t  |\n" % (mean, median, std_dev)
    stats += "-------------------------------------------------------\n"
    stats += "|\t             |\t Mean\t|\tMedian\t|\tStd.Dev\t  |\n"
    stats += "|  Rounded Down  |------------------------------------|\n"
    stats += "|\t             |\t %.2f\t|\t %.2f\t|\t %.2f\t  |\n" % (mean_rounded, median_rounded, std_dev_rounded)
    stats += "-------------------------------------------------------\n"

    # print stats
    print(stats)


def plot_quake_map(qd):
    """
        This function is responsible for calculating and plotting the quakes on a flattened world map, distinguishing
        quakes by size and by color.

        Colorbar/cmap: https://matplotlib.org/stable/users/explain/colors/colormaps.html
    """

    # list of all latitudes
    latitudes = [quake.lat for quake in qd.get_filtered_array()]
    # list of all longitudes
    longitudes = [quake.long for quake in qd.get_filtered_array()]
    # list of all magnitudes
    magnitudes = [quake.mag for quake in qd.get_filtered_array()]

    # plotting the magnitudes on a flattened world map, using colors and size for the magnitude
    plt.figure(figsize=(10, 8))
    sc = plt.scatter(x=latitudes, y=longitudes, s=[mag ** 4.0 for mag in magnitudes], c=magnitudes, cmap='viridis',
                     alpha=0.55)

    # set the title and horizonal/vertical labels for the scatter map
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Earthquake Map')

    # set the colorbar to be based on the values in the scatter
    cbar = plt.colorbar(sc)
    cbar.set_label('Magnitude')

    plt.show()


def plot_magnitude_chart(qd):
    """This function is used to calculate and display the frequency of whole-number magnitude earthquakes"""

    # list of magnitudes
    magnitudes = [quake.mag for quake in qd.get_filtered_list()]

    print(magnitudes)

    # list of whole number magnitudes from magnitudes
    whole_num_mags = [mag for mag in magnitudes if type(mag) is int]

    print(whole_num_mags)

    # list of colors to set the bar colors
    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple',
                  'tab:pink', 'tab:gray', 'tab:cyan', 'tab:brown']

    # create a histogram using numpy to calculate the counts of each magnitude
    counts, _ = np.histogram(whole_num_mags, np.arange(1, 12))

    # to display 0 to 10 magnitudes
    x_ticks = np.arange(1, 11)
    plt.xticks(x_ticks)
    # to display 0 to the highest frequency (20 for breathing room, only goes up to 11)
    plt.yticks(np.arange(20))

    # bar chart using the histogram counts with magnitudes at the bottom, and frequency on the left
    plt.bar(x_ticks, counts, width=0.8, edgecolor='black', color=bar_colors)

    # set the title and horizonal/vertical labels for the bar chart map
    plt.title('Earthquake Magnitude Analysis')
    plt.ylabel('Frequency')
    plt.xlabel('Magnitude')

    plt.show()


def get_menu_input(qd):
    """This function is used to handle the user input from the console"""

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
    """This function is used to start begin this Earthquakes Analysis

        sys.argv - https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    """

    path = None

    # check for passed in arg for filename
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    else:
        path = Path("earthquakes.geojson")

    # read json file
    with open(path, 'r') as file:
        data = json.load(file)

    # create QuakeData obj
    quake_data = QuakeData(data)

    # start session
    while True:
        print_menu()
        get_menu_input(quake_data)


analyse_earthquakes()
