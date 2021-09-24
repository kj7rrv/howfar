from . import gpsd_api
from . import distance
import time


class Tracker:
    callbacks = {}
    total_distance = 0
    connection = False
    tracking = False
    acquired = False
    last_point = 0
    def __init__(self):
        try:
            self.connection = gpsd_api.Connection()
            connection.enabled = True
        except ConnectionRefusedError:
            print("Unable to connect to gpsd")

    def on_event(self, event_name, callback):
        if event_name not in self.callbacks:
            self.callbacks[event_name] = []
        self.callbacks[event_name].append(callback)

    def emit_event(self, event_name, data):
        if event_name in self.callbacks:
            for callback in self.callbacks[event_name]:
                callback(data)

    def poll(self):
        if not self.connection:
            self.emit_event("error", "Unable to connect to gpsd")
            return False
        if not self.acquired:
            tpvs = self.connection.get_messages(['TPV'], clear=True)
            if tpvs:
                self.connection.clear_queue()
                self.last_point = tpvs[-1]
                self.acquired = True
                self.emit_event("acquired", last_point)
        else:
            tpvs = self.connection.get_messages(['TPV'], clear=True)
            if tpvs:
                meters = distance.distance([self.last_point] + tpvs)[0]
                self.total_distance += meters
                self.last_point = tpvs[-1]
                self.emit_event("distance", self.total_distance)
        return self.tracking

def main():
    conn = gpsd_api.Connection()
    conn.enabled = True

    total_distance = 0

    while True:
        tpvs = conn.get_messages(['TPV'], clear=True)
        if tpvs:
            conn.clear_queue()
            last_point = tpvs[-1]
            print('Acquired location.')
            break

    while True:
        tpvs = conn.get_messages(['TPV'], clear=True)
        if not tpvs:
            continue
        meters = distance.distance([last_point] + tpvs)[0]
        total_distance += meters
        last_point = tpvs[-1]
        print(round(total_distance*1000)/1000)
        time.sleep(3)

if __name__ == "main":
    main()
