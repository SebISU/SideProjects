import json
import datetime
import random


with open("sample_correct_data.json", "w") as f:

    row = {}

    epoch = int(datetime.datetime.now().timestamp())

    for x in range(1000):

        curr_epoch = (epoch + x) * 10

        if x % 2 == 1:

            row["timestamp"] = curr_epoch * 100000000
            row["Signal_key"] = "MILEAGE"
            row["Signal_value"] = round(5233.0 + x * 0.015, 1)
            f.write(json.dumps(row) + "\n")

        row["timestamp"] = curr_epoch * 100000000
        row["Signal_key"] = "LATITUDE"
        row["Signal_value"] = round(41.1211 + x * 0.0006, 4)
        f.write(json.dumps(row) + "\n")

        row["timestamp"] = curr_epoch * 100000000
        row["Signal_key"] = "LONGITUDE"
        row["Signal_value"] = round(-92.2333 + x * 0.0006, 4)
        f.write(json.dumps(row) + "\n")

        for y in range(10):

            row["timestamp"] = (curr_epoch + y) * 100000000
            row["Signal_key"] = "SPEED"
            row["Signal_value"] = round(random.uniform((x / 100 + 1) * 10 - 3, (x / 100 + 1) * 10 + 3), 1)

            f.write(json.dumps(row) + "\n")

