class Metric:
    def __init__(self):
        self.names = {
            "distance": "km",
            "pace": "min/km"
        }

    def distance(self, meters):
        return meters / 1000.0 # to km

    def pace(self, speed): # speed in m/s
        return 16.66666 / speed # min/km
