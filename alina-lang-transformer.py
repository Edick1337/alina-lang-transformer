import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import pytz

url = "https://translations.telegram.org/eliteng/android/export"
formatters = ["formatterMonthYear", "formatterStats12H", "formatterStats24H", "formatterBannedUntil12H",
              "formatterBannedUntil24H", "formatterBannedUntilThisYear12H", "formatterBannedUntilThisYear24H",
              "formatterMonthYear2", "formatterMonthName", "formatterMonth", "formatterYear", "formatterYearMax",
              "chatDate", "chatFullDate", "formatterWeek", "formatterWeekLong", "formatterDay24H", "formatterDay12H",
              "formatDateAtTime", "formatDateSchedule", "formatDateScheduleYear", "SendTodayAt", "SendDayAt",
              "SendDayYearAt", "StartTodayAt", "StartDayAt", "StartDayYearAt", "StartsTodayAt", "StartsDayAt",
              "StartsDayYearAt", "StartShortTodayAt", "StartShortDayAt", "StartShortDayYearAt", "RemindTodayAt",
              "RemindDayAt", "RemindDayYearAt"]

response = urllib.request.urlopen(url)
xml_data = response.read()

root = ET.fromstring(xml_data)

for elem in root.iter():
    if elem.attrib.get("name") in formatters:
        continue
    if elem.text:
        elem.text = ' '.join(elem.text.lower().strip(' "').split())

nameTemplate = "edited_strings"

for file in os.listdir():
    if nameTemplate in file:
        os.remove(file)

moscow_tz = pytz.timezone('Europe/Moscow')
now = datetime.now(moscow_tz).strftime("%d-%m-%Y_%H-%M-%S")
filename = f"{nameTemplate}_{now}.xml"
tree = ET.ElementTree(root)
tree.write(filename)
