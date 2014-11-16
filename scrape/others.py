import timeblock
import datetime, calendar
import rsfhours

class Others:
    def __init__(self, classes, day):
        self.classes = classes
        self.day = day

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

    def class_today(self, _class):
        key = calendar.day_name[self.day.weekday()]
        if key in _class.start.keys():
            return True
        return False
        
    def create_block(self, _class):
        key = calendar.day_name[self.day.weekday()]
        start_str = _class.start[key]
        end_str = _class.end[key]
        start = self.time_obj(start_str)
        end = self.time_obj(end_str)
        return timeblock.TimeBlock(start, end, _class.name)

    def block_list(self):
        Blocks = []
        key = calendar.day_name[self.day.weekday()]
        for c in self.classes:
            if self.class_today(c):
                Blocks.append(self.create_block(c))
        return Blocks


