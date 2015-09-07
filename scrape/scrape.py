import re
import calendar


class OrNahParser:
    """Scrape data from RSF Weekly Schedule website: http://recsports.berkeley.edu/fitness-wellness/group-exercise/weekly-schedule/ using this URL: https://www.healcode.com/widgets/mb/schedules/cp32621nhv.js <----credits to Kevin Lin"""

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

    # Returns new substring of _STR starting at INDEX
    # and increments COUNT
    def move_by(self, index):
        self.str = self.str[index:]
        self.count += index
        return self.str

    # Returns string indicating time of first instance of
    # either starttime or endtime -- use 0 or 1 to get those respectively
    def get_time(self, start=0):
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
        obj = obj.replace(hour=hr, minute=m, second=0, microsecond=0)
        return obj
