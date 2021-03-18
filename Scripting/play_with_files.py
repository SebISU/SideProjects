#! /usr/bin/python3

import os
import time
from datetime import datetime
import json
import requests
import re


os.system("mkdir -p riela_dir")

url = "https://www.riela.pl/kontakt-6/"

website  = requests.get(url)

html = website.text

links = re.findall('"((http|ftp)s?://.*?)"', html)
emails = re.findall('([\w\.,]+@[\w.,]+\.\w+)', html)

x = "riela_dir/" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

with open(x, "w") as f:

    row  = {}

    for link in links:

        row['type'] = "link"
        row['value'] = link[0]

        f.write(json.dumps(row) + "\n")

    for email in emails:

        row['type'] = "email"
        row['value'] = email

        f.write(json.dumps(row) + "\n")
