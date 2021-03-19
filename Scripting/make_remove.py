#! usr/bin/python3

import os
import shutil
from datetime import datetime
import time

path = os.path.abspath(os.getcwd())

os.chdir("/home/sebastian")

for root, dirs, files in os.walk(".", topdown = True):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))

os.chdir(path)

nm = "temp_file_"
text = "Content of the file No. "


for x in range(100):
    with open(nm+str(x), "w") as f:
        f.write(text+str(x))

time.sleep(10)

for x in range(100):
    os.rename(nm+str(x), nm+"after_"+str(x))

time.sleep(10)

try:
    os.mkdir("temp")
except FileExistsError:
    print("Directory 'temp' already exists.")

with os.scandir(".") as it:
    for entry in it:
        if entry.is_file() and nm in entry.name:
            shutil.move(entry.name, "./temp")

time.sleep(20)
shutil.rmtree("temp")
