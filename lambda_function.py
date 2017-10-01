"""Bart Helper lambda function code, which is triggered by HTTPS calls from Api.ai to the Api gateway."""
import json
from utils import get_station_name, get_direction
from stations import stations
import urllib.request
# import os

def lambda_handler(event, context):
    """Takes in an event from Api.ai, through Api Gateway.
    Returns a dict with keys "speech", "displayText", and "Source".
    Source is always the "BART API"    """
    station = get_station_name(event)
    direction = get_direction(event)

    def find_abbr_station(stations=stations, station=station):
        for i in range(0, len(stations)):
            if stations[i]['api_ai_value'] == station:
                return stations[i]['abbr']
    abbr_station = find_abbr_station()

    if direction == "north":
        abbr_direction = "n"
    elif direction == "south":
        abbr_direction = "s"

    # key = os.environ.get(BART_API_KEY)

    url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=" + abbr_station + "&dir=" + abbr_direction + "&key=" + 'MW9S-E7SL-26DU-VV8V' + "&json=y"
    url_request = urllib.request.urlopen(url)
    url_loaded = json.load(url_request)
    time = url_loaded['root']['station'][0]['etd'][0]['estimate'][0]['minutes']

    display_station = station.title()
    display_direction = direction.capitalize()

    speech = "The next " + direction + " bound train leaves " + station + " in " + time +" minutes."
    displayText = "The next " + display_direction + "-bound train leaves " + display_station + " in " + time +" minutes."
    Source = "BART API"

    dictionary = {
    'speech': speech,
    'displayText': displayText,
    'Source': Source
    }
    return dict(dictionary)


def test_lambda_handler():
    """This may be helpful when testing your function"""
    with open('sample_event.json', 'r') as f:
        sample_event = json.load(f)

    response = lambda_handler(sample_event, None)
    print(json.dumps(response, indent=4))

# if __name__ == '__main__':
#     test_lambda_handler()
