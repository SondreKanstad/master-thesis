import json_stream
import json
f = open('dynamics.json')
data = json.load(f)
vehicles = data["time_s"]


def create_chunk(start, stop):
    chunk = {}
    for count, value in enumerate(vehicles):
        if count >= start and count < stop:
            chunk[value] = vehicles[value]
    out_file = open(f"dynamics_{start}_{stop}.json", "w")
    json.dump(chunk, out_file)
    out_file.close()

create_chunk(0,10000)
create_chunk(10000, 20000)
create_chunk(20000, 30000)
create_chunk(30000, 40000)
create_chunk(40000, 50000)