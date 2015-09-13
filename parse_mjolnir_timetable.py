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

for div in divs:
    parse_day_class(div)

for index in range(1,8):
    index_string = "day-%d" % index
    info = days[index_string]
    index_string = index_string.replace("-", "_")
    spans = info.findAll("span")
    timetable[index_string] = []
    for k in range(len(spans)):
        if k % 4 == 0:
            timetable[index_string].append({})
        key = spans[k].attrs[0][1]
        value = spans[k].string.replace("kl. ", "").replace("Kennari: ", "")
        timetable[index_string][-1][key] = value

print json.dumps(timetable, encoding='iso-8859-1')
