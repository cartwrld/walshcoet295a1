import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import json
import math
import sys  # used for reading the args
from earthquakes import QuakeData


# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#   Name:            Carter Walsh (walsh0715)       #
#   Class:           COET295 - Assignment 1         #
#   Instructor:      Wade Lahoda & Bryce Barrie     #
#   Date:            Tuesday, May 21st, 2024        #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #


def print_menu():
    """This function is responsible for printing the menu for the user"""

    menu = "\n==================================================================\n"
    menu += "|                    Earthquake Analyser Menu                    |\n"
    menu += "==================================================================\n"
    menu += "|                                                                |\n"
    menu += "|   1)  Set Location Filter    5)  Display Exceptional Quakes    |\n"
    menu += "|   2)  Set Property Filter    6)  Display Magnitude Stats       |\n"
    menu += "|   3)  Clear Filters          7)  Plot Quake Map                |\n"
    menu += "|   4)  Display Quakes         8)  Plot Magnitude Chart          |\n"
    menu += "|                                                                |\n"
    menu += "|                      9)  Quit                                  |\n"
    menu += "==================================================================\n"

    print(menu)


def set_location_filter(qd):
    """This function is responsible for prompting the user to enter their desired values for the Location Filter"""

    lat = input("Please enter the Latitude:\t")
    lon = input("Please enter the Longitude:\t")
    dist = input("Please enter the Distance:\t")

    # set the empty values to 0
    if lat == "":
        lat = 0.0
    if lon == "":
        lon = 0.0
    if dist == "":
        dist = 0

    qd.set_location_filter(float(lat), float(lon), int(dist))


def set_property_filter(qd):
    """This function is responsible for prompting the user to enter their desired values for the Property Filter"""

    mag = input("Please enter the Magnitude:\t")
    felt = input("Please enter the Felt value:\t")
    sig = input("Please enter the Significance:\t")

    # set the empty values to 0
    if mag == "":
        mag = 0.0
    if felt == "":
        felt = 0
    if sig == "":
        sig = 0

    qd.set_property_filter(float(mag), int(felt), int(sig))


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

    # calculate the mode by getting counts of the unique values, then
    vals, counts = np.unique(rounded_down_mags, return_counts=True)
    index = np.argmax(counts)

    mode = vals[index]

    # building the output to be displayed to the user
    stats = "\n----------------------------------------------\n"
    stats += "|       Earthquake Magnitude Statistics      |\n"
    stats += "----------------------------------------------\n"
    stats += "|   Mean   |  Median  |  Std.Dev  |   Mode   |\n"
    stats += "|--------------------------------------------|\n"
    stats += "|   %.2f   |   %.2f   |    %.2f   |     %d    |\n" % (mean, median, std_dev, mode)
    stats += "----------------------------------------------\n"

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
                     edgecolor='black', alpha=0.55)  # couldn't choose a color, so I chose a gradient

    # set the title and horizontal/vertical labels for the scatter map
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Earthquake Map')

    # set the colorbar to be based on the values in the scatter
    cbar = plt.colorbar(sc)
    cbar.set_label('Magnitude')

    plt.show()


def plot_magnitude_chart(qd):
    """This function is used to calculate and display the frequency of whole-number magnitude earthquakes

        Numpy Histogram info - https://www.geeksforgeeks.org/numpy-histogram-method-in-python/
                             - https://stackoverflow.com/questions/9141732/how-does-numpy-histogram-work
    """
    # list of magnitudes
    magnitudes = [quake.mag for quake in qd.get_filtered_list()]
    # list of whole number magnitudes from magnitudes
    whole_num_mags = [mag for mag in magnitudes if type(mag) is int]
    # list of colors to set the bar colors
    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:purple',
                  'tab:pink', 'tab:gray', 'tab:cyan', 'tab:brown', 'tab:olive']

    # create a histogram using numpy to calculate the counts of each magnitude
    counts, _ = np.histogram(whole_num_mags, np.arange(1, 12))

    # to display 1 to 10 magnitudes
    x_ticks = np.arange(1, 11)
    plt.xticks(x_ticks)

    # to display 0 to the highest frequency (1000 for breathing room, base data only goes up to 11)
    plt.yticks(np.arange(1000))

    # bar chart using the histogram counts with magnitudes at the bottom, and frequency on the left
    plt.figure(figsize=(10, 8))
    plt.bar(x_ticks, counts, width=0.8, edgecolor='black', color=bar_colors)

    # set the title and horizontal/vertical labels for the bar chart map
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
        print("\nThanks for analyzing!\n\nGoodbye :)\n")
        quit()


def analyse_earthquakes():
    """This function is used to start begin this Earthquakes Analysis

        sys.argv - https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    """

    path = "earthquakes.geojson"

    # check for passed in arg for filename
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])

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
