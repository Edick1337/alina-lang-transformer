import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import pytz

language_name = "aboba13453"
url = f"https://translations.telegram.org/{language_name}/android/export"

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

for file in os.listdir():
    if language_name in file:
        os.remove(file)

moscow_tz = pytz.timezone("Europe/Moscow")
now = datetime.now(moscow_tz).strftime("%d-%m-%Y")
filename = f"{language_name}_{now}.xml"
tree = ET.ElementTree(root)
tree.write(filename)

env_file = os.getenv('GITHUB_ENV')
with open(env_file, "w") as myfile:
    myfile.write(f"LANGUAGE_NAME={language_name}\n")
    myfile.write(f"FILE_NAME={filename}")
