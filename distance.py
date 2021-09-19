from vincenty import vincenty

def _distance(a, b):
    kilometers = vincenty((a['lat'], a['lon']), (b['lat'], b['lon']))
    miles = vincenty((a['lat'], a['lon']), (b['lat'], b['lon']), miles=True)

    return kilometers*1000, miles*5280


def distance(points):
    '''
    returns distance between any number of points specified as an iterable
    of dicts from gpsd_api.py as a tuple (meters, feet)
    '''

    if len(points) >= 2:
        last_point = points[0]
        meters = 0
        feet = 0

        for point in points[1:]:
            new_meters, new_feet = _distance(last_point, point)
            meters += new_meters
            feet += new_feet
            last_point = point

        return meters, feet
    else:
        return 0, 0
