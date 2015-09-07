from datetime import datetime, timedelta, time
from models import OpenHours


class TimeBlock:
    # Takes in START and END which are datetime objects and an optional CLASSNAME string
    def __init__(self, start, end, classname=None):
        self.start = start
        self.end = end
        self.reserved = False
        if classname and classname != "No reservation":
            self.reserved = True
        self.rsf_closed = False
        self.name = classname
        self.now = datetime.now()

    # Returns the duration of this TimeBlock in minutes
    def duration(self):
        d = self.end - self.start
        minutes = d.seconds / 60
        return minutes

    def time_til(self):
        time = self.now
        if self.start > time:
            t = self.start - time
            minutes = t.seconds / 60
            return minutes
        return 0

    def time_left(self):
        time = self.now
        if self.end > time:
            t = self.end - time
            minutes = t.seconds / 60 + 1
            return minutes
        return 0

    def time_left_sec(self):
        time = self.now
        if self.end > time:
            t = self.end - time
            return t.seconds
        return 0

    def to_str(self, minutes):
        string = ""
        if minutes > 60:
            string += str(minutes / 60) + " hours"
            rem = minutes - (minutes / 60) * 60
            if rem != 0:
                string += " " + str(rem) + " minutes"
        else:
            string += str(minutes) + " minutes"
        return string

    def time_left_str(self):
        minutes = self.time_left()
        return self.to_str(minutes)

    def dur_str(self):
        minutes = self.duration()
        return self.to_str(minutes)

    def in_session(self):
        time = self.now
        if self.start < time and time < self.end:
            return True
        return False

    def twelve_str(self, time_obj):
        string = time_obj.strftime("%I:%M %p")
        if string[0] == '0':
            return string[1:]
        return string

    def __str__(self):
        string = ""
        string += self.name
        string += str(self.start)
        string += str(self.end)
        return string

    def start_str(self):
        return self.twelve_str(self.start.time())

    def end_str(self):
        return self.twelve_str(self.end.time())

    def startend_str(self):
        return self.start_str() + " - " + self.end_str()

    def web_str(self):
        return self.__str__()

    @staticmethod
    def compare(block1, block2):
        if block1.start > block2.start:
            return 1
        if block1.start == block2.start:
            if block1.end > block2.end:
                return 1
            if block1.end == block2.end:
                return 0
        return -1


class BlockList:
    def __init__(self, classlist, day):
        self.classes = []
        for c in classlist:
            self.classes.append(c)
        self.sort()
        self.today = day.date()
        self.tom = self.today + timedelta(days=1)
        self.yest = self.today - timedelta(days=1)
        self.hours = OpenHours.objects.get(pk=1).reservation_set

    def add(self, block):
        if self.classes.count(block) == 0:
            self.classes.append(block)
            self.sort()

    def sort(self):
        self.classes.sort(cmp=TimeBlock.compare)

    def __str__(self, start=0):
        string = ""
        for i, _class in enumerate(self.classes):
            if i >= start:
                string += _class.__str__()
                string += "\n"
        return string

    def web_str(self):
        return self.__str__()

    def get_earliest(self):
        if len(self.classes) != 0:
            return self.classes[0]
        return None

    def get_latest(self, pointer=None):
        if len(self.classes) != 0:
            return self.classes[-1]
        return None

    def get_current(self):
        for c in self.classes:
            if c.in_session():
                return c
        return None

    def curr_list(self):
        curr = self.get_current()
        c = self.classes
        return c[c.index(curr) + 1:]

    def start_blocks(self):
        day_num = self.today.weekday()
        rsf = self.hours.get(day_num=day_num)
        rsf_yest = self.hours.get(day_num=(day_num - 1) % 7)
        earliest = self.get_earliest()
        blocks = []
        if earliest:
            start = earliest.start
        else:
            start = rsf.get_end_dt(self.today)
        rsf_start = rsf.get_start_dt(self.today)
        if rsf_start < start:
            new = TimeBlock(rsf_start, start, "No reservation")
            blocks.append(new)
        twelve = datetime.combine(self.today, time())
        rsf_yest_end = rsf_yest.get_end_dt(self.yest)
        if rsf_yest_end > twelve:
            new = TimeBlock(twelve, rsf_yest_end, "No reservation")
            blocks.append(new)
            blocks.append(self.closed_block(yest=True))
        if rsf_yest_end < twelve:
            new = TimeBlock(rsf_yest_end, rsf_start, "-- RSF CLOSED --")
            blocks.append(new)
        return blocks

    def closed_block(self, yest=False):
        if yest:
            today = self.yest
            tom = self.today
            day_num = self.yest.weekday()
        else:
            today = self.today
            tom = self.tom
            day_num = self.today.weekday()
        rsf = self.hours.get(day_num=day_num)
        rsf_tom = self.hours.get(day_num=(day_num + 1) % 7)

        return TimeBlock(rsf.get_end_dt(today), rsf_tom.get_start_dt(tom), "-- RSF CLOSED --")

    def get_free_blocks(self):
        L = self.classes
        blocks = []
        for i, item in enumerate(L):
            if (i + 1) < len(L):
                if item.end < L[i + 1].start:
                    blocks.append(TimeBlock(item.end, L[i + 1].start, "No reservation"))
        return blocks

    def finalize(self):
        for b in self.start_blocks():
            self.add(b)
        self.add(self.closed_block())
        for b in self.get_free_blocks():
            self.add(b)
