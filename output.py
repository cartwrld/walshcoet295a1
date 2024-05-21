from pathlib import Path
import random as randy

path = Path('eq_output.geojson')


# opens the file --> writes the text --> closes the file

def get_start_data():
    start_data = '{\n'
    start_data += '\t"type": "FeatureCollection",\n'
    start_data += '\t"metadata": {\n'
    start_data += '\t\t"generated": 1715221562000,\n'
    start_data += '\t\t"url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson",\n'
    start_data += '\t\t"title": "USGS All Earthquakes, Past Month",\n'
    start_data += '\t\t"status": 200,\n'
    start_data += '\t\t"api": "1.10.3",\n'
    start_data += '\t\t"count": 10823\n'
    start_data += '\t},\n'
    start_data += '\t"features": [\n'

    return start_data


def get_randy_feature():

    mag = round(randy.random() + randy.randint(0, 10), 2)

    if mag > 10:
        mag = 10


    text_to_write =  '        {\n'
    text_to_write += '\t\t\t"type": "Feature",\n'
    text_to_write += '\t\t\t"properties": {\n'
    text_to_write += f'\t\t\t\t"mag": {mag},\n'
    text_to_write += '\t\t\t\t"place": "87 km ESE of Red Dog Mine, Alaska",\n'
    text_to_write += '\t\t\t\t"time": 1715221312431,\n'
    text_to_write += '\t\t\t\t"updated": 1715221508073,\n'
    text_to_write += '\t\t\t\t"tz": null,\n'
    text_to_write += '\t\t\t\t"url": "https://earthquake.usgs.gov/earthquakes/eventpage/ak0245z16lhr",\n'
    text_to_write += '\t\t\t\t"detail": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/ak0245z16lhr.geojson",\n'
    text_to_write += f'\t\t\t\t"felt": {randy.randint(0, 10000)},\n'
    text_to_write += '\t\t\t\t"cdi": null,\n'
    text_to_write += '\t\t\t\t"mmi": null,\n'
    text_to_write += '\t\t\t\t"alert": null,\n'
    text_to_write += '\t\t\t\t"status": "automatic",\n'
    text_to_write += '\t\t\t\t"tsunami": 0,\n'
    text_to_write += f'\t\t\t\t"sig": {randy.randint(1, 5000)},\n'
    text_to_write += '\t\t\t\t"net": "ak",\n'
    text_to_write += '\t\t\t\t"code": "0245z16lhr",\n'
    text_to_write += '\t\t\t\t"ids": ",ak0245z16lhr,",\n'
    text_to_write += '\t\t\t\t"sources": ",ak,",\n'
    text_to_write += '\t\t\t\t"types": ",origin,phase-data,",\n'
    text_to_write += '\t\t\t\t"nst": null,\n'
    text_to_write += '\t\t\t\t"dmin": null,\n'
    text_to_write += '\t\t\t\t"rms": 0.86,\n'
    text_to_write += '\t\t\t\t"gap": null,\n'
    text_to_write += '\t\t\t\t"magType": "ml",\n'
    text_to_write += '\t\t\t\t"type": "earthquake",\n'
    text_to_write += '\t\t\t\t"title": "M 2.9 - 87 km ESE of Red Dog Mine, Alaska"\n'
    text_to_write += '\t\t\t},\n'
    text_to_write += '\t\t\t"geometry": {\n'
    text_to_write += '\t\t\t\t"type": "Point",\n'
    text_to_write += '\t\t\t\t"coordinates": [\n'
    text_to_write += f'\t\t\t\t\t{round(randy.randint(-90, 90) + randy.random(), randy.randint(3,6))},\n'
    text_to_write += f'\t\t\t\t\t{round(randy.randint(-180, 180) + randy.random(), randy.randint(3,6))},\n'
    text_to_write += '\t\t\t\t\t0.1\n'
    text_to_write += '\t\t\t\t]\n'
    text_to_write += '\t\t\t},\n'
    text_to_write += '\t\t\t"id": "ak0245z16lhr"\n'
    text_to_write += '\t\t},\n'

    return text_to_write


def get_finisher():
    finisher = '\t],\n'
    finisher += '\t"bbox": [\n'
    finisher += '\t\t-179.9934,\n'
    finisher += '\t\t-65.277,\n'
    finisher += '\t\t-3.43,\n'
    finisher += '\t\t179.9833,\n'
    finisher += '\t\t83.8816,\n'
    finisher += '\t\t634.645\n'
    finisher += '\t]\n'
    finisher += '}\n'

    return finisher


output = get_start_data()

for i in range(0, 1000):
    output += get_randy_feature()
output += get_finisher()

path.write_text(output)
