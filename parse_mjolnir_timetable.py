#! -*- coding: utf-8 -*-
import json
import urllib2
import re
import requests
from BeautifulSoup import BeautifulSoup
days = {}
timetable = {}
def parse_day_class(div):
    for attr in div.attrs:
        if attr[0] == "class" and attr[1].find("day-") >= 0:
            days[attr[1].replace(" current", "").replace("day ", "")] = div
page = requests.get('http://www.mjolnir.is')
parsed_html = BeautifulSoup(page.text)
divs = parsed_html.body.findAll('div')

index_map = {
    "day_1": "mon",
    "day_2": "tue",
    "day_3": "wed",
    "day_4": "thu",
    "day_5": "fri",
    "day_6": "sat",
    "day_7": "sun",
}

for div in divs:
    parse_day_class(div)

for index in range(1,8):
    index_string = "day-%d" % index
    info = days[index_string]
    index_string = index_string.replace("-", "_")
    spans = info.findAll("span")
    timetable[index_map[index_string]] = [{}]
    seen_keys = {}
    for k in range(len(spans)):
        key = spans[k].attrs[0][1]
        if key in seen_keys:
            timetable[index_map[index_string]].append({})
            seen_keys = {}
        seen_keys[key] = 1
        value = spans[k].string.replace("kl. ", "").replace("Kennari: ", "")
        timetable[index_map[index_string]][-1][key] = value


print json.dumps(timetable, encoding='iso-8859-1')
