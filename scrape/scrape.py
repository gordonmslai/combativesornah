#Scrape data from RSF Weekly Schedule website: http://recsports.berkeley.edu/fitness-wellness/group-exercise/weekly-schedule/
# https://www.healcode.com/widgets/mb/schedules/cp32621nhv.js <----credit to kevin

from lxml import etree, html
from urllib2 import urlopen

import re
import timeblock
import datetime, calendar
from classes import fencing, calstaryoga, archery
import rsfhours
import others
import sys



class OrNahParser:

    def __init__(self, string, day):
        self.str = string
        self.count = 0
        self.day = day

    def today_str(self):
        month = calendar.month_name[self.day.month]
        day = self.day.day
        string = str(month + ' ' + str(day))
        return string

    # Returns new substring of _STR starting at first instance of SUB
    # and increments COUNT by index
    def move_to(self, sub):
        index = self.str.index(sub[:])
        self.str = self.str[index:]
        self.count += index
        return self.str

    # Returns string indicating time of first instance of 
    # either starttime or endtime -- use 0 or 1 to get those respectively
    def get_time(self, start = 0):
        if start == 0:
            self.move_to("hc_starttime")
        else:
            self.move_to("hc_endtime")
        m = re.search('\d\d?:\d\d [AP]M', self.str[:26])
        return m.group(0)

    # Construct Timeblock using _STR times
    def time_obj(self, _str):
        hr = _str[:2]
        if hr[1] == ':':
            hr = hr[0]
        hr = int(hr)
        if _str[-2:] == "PM" and hr != 12:
            hr += 12
        m = int(_str[-5:-3])
        obj = self.day
        obj = obj.replace(hour = hr, minute = m, second = 0, microsecond = 0)
        return obj
# if curr.reserved:
#     print("Nah...")
# elif curr.reserved == False:
#     print("YAS")
# print(" ")
# print("-- Currently --")
# print(" ")
# print(curr.name)
# print("Time remaining: " + curr.to_str(curr.time_left()))
# print(" ") 
# print("-- Upcoming --")
# print(" ")

# print(SortedBlocks.__str__(index + 1))