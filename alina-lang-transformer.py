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
file_name = f"{language_name}.xml"
tree = ET.ElementTree(root)
tree.write(file_name)

env_file = os.getenv('GITHUB_ENV')
latest_link = f"https://github.com/Edick1337/alina-lang-transformer/releases/latest/download/{file_name}"
with open(env_file, "w") as myfile:
    myfile.write(f"DATE={now}\nLANGUAGE_NAME={language_name}\nFILE_NAME={file_name}\nLATEST_LINK={latest_link}")
