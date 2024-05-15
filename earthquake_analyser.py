import numpy as np
# import matplotlib.pyplot as plt
import json
from pathlib import Path
from earthquakes import QuakeData, Quake

quakes = {}

path = Path("./earthquakes.geojson")

with open(path, 'r') as file:
    data = json.load(file)

ex1 = QuakeData(data)
ex1.get_filtered_array()


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

    QuakeData.location_filter = (lat, lon, dist)


def set_property_filter():
    mag = float(input("Please enter the Magnitude:\t"))
    felt = float(input("Please enter the Felt value:\t"))
    sig = float(input("Please enter the Significance:\t"))

    QuakeData.property_filter = (mag, felt, sig)


def clear_filters():
    QuakeData.location_filter = (0.0, 0.0, 0.0)
    QuakeData.property_filter = (0.0, 0.0, 0.0)


def display_quakes(qd):
    for quake in qd.quake_array:
        print(quake)


def display_exceptional_quakes():
    pass


def display_magnitude_stats():
    pass


def plot_quake_map():
    pass


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
        display_quakes(ex1)
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
