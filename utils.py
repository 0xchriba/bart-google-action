"""Optional helper function """


def get_station_name(event):
    """get the station name from the event"""
    return event['result']['parameters']['station']


def get_direction(event):
    """get the direction from the event"""
    return event['result']['parameters']['direction']
