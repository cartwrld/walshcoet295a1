import numpy as np
# import matplotlib.pyplot as plt
import json
from pathlib import Path
from earthquakes import QuakeData, Quake

quakes = {}

path = Path("./earthquakes_copy.geojson")

with open(path, 'r') as file:
    data = json.load(file)

ex1 = QuakeData(data)


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
    pass


def clear_filters():
    pass


def display_quakes():
    pass


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
        print(QuakeData.location_filter)
    elif option == '2':
        set_property_filter()
    elif option == '3':
        clear_filters()
    elif option == '4':
        display_quakes()
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


print_menu()
get_menu_input()


# print(f"{ex1.quake_array[0]}")