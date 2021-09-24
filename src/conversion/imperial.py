class Imperial:
    def __init__(self):
        self.names = {
            "distance": "mile",
            "pace": "min/mile"
        }


    def distance(self, meters):
        return meters * 0.000621371 # magic number converts to miles

    def pace(self, speed): # speed in m/s
        return 26.8224 / speed # min/mile
