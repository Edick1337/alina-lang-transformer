import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import pytz

url = "https://translations.telegram.org/eliteng/android/export"
exclusions = [
    "chatDate",
    "chatFullDate",
    "SendTodayAt",
    "SendDayAt",
    "SendDayYearAt",
    "StartTodayAt",
    "StartDayAt",
    "StartDayYearAt",
    "StartsTodayAt",
    "StartsDayAt",
    "StartsDayYearAt",
    "StartShortTodayAt",
    "StartShortDayAt",
    "StartShortDayYearAt",
    "RemindTodayAt",
    "RemindDayAt",
    "RemindDayYearAt"
]

response = urllib.request.urlopen(url)
xml_data = response.read()

root = ET.fromstring(xml_data)

for elem in root.iter():
    name_attr = elem.attrib.get("name")
    if name_attr is None:
        continue
    if name_attr in exclusions or name_attr.startswith("format"):
        continue
    if elem.text:
        elem.text = " ".join(elem.text.lower().strip(' "').split())

name_template = "eliteng"

for file in os.listdir():
    if name_template in file:
        os.remove(file)

moscow_tz = pytz.timezone("Europe/Moscow")
now = datetime.now(moscow_tz).strftime("%d-%m-%Y")
filename = f"{name_template}_{now}.xml"
tree = ET.ElementTree(root)
tree.write(filename)
