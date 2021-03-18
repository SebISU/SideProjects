import requests
import re
import os

url = "https://www.riela.pl/kontakt-6/"

website = requests.get(url)

html = website.text

links = re.findall('"((http|ftp)s?://.*?)"', html)
emails = re.findall('([\w\.,]+@[\w\.,]+\.\w+)', html)

for link in links:
    print(link[0])

for email in emails:
    print(email)
