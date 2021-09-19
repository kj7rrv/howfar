import gpsd_api
import distance
import time

conn = gpsd_api.Connection()
conn.enabled = True

total_distance = 0

print('Waiting for location...')

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
    print(total_distance)
    time.sleep(1)
