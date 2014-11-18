import datetime
import rsfhours
import scrape, others

class TimeBlock:
    
    # Takes in START and END which are datetime objects and an optional CLASSNAME string
    def __init__(self, start, end, classname = None):
        self.start = start
        self.end = end
        if self.start > self.end:
            self.end = self.end + datetime.timedelta(days = 1)
        self.reserved = False
        if classname != None and classname != "No reservation":
            self.reserved = True
        self.rsf_closed = False
        self.name = classname
        self.now = datetime.datetime.utcnow() - datetime.timedelta(hours = 8)
    # Returns the duration of this TimeBlock in minutes
    def duration(self):
        d = self.end - self.start
        minutes = d.seconds / 60 
        return minutes
    def time_til(self):
        time = self.now
        print(self.now)
        print(self.start)
        if self.start > time:
            t = self.start - time
            minutes = t.seconds / 60
            print(minutes)
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

    def __init__(self, classlist):
        self.classes = []
        for c in classlist:
            self.classes.append(c)
        self.sort()

    def add(self, block):
        if self.classes.count(block) == 0:
            self.classes.append(block)
            self.sort()
    
    def sort(self):
        self.classes.sort(cmp = TimeBlock.compare)

    def __str__(self, start = 0):
        string = ""
        for i, _class in enumerate(self.classes):
            if i >= start:
                string += _class.__str__()
                string += "\n"
        return string

    def web_str(self):
        return self.__str__()

    def get_earliest(self):
        return self.classes[0]

    def get_latest(self, pointer = None):
        return self.classes[-1]

    def get_current(self):
        for c in self.classes:
            if c.in_session():
                return c
        return None

    def curr_list(self):
        curr = self.get_current()
        c = self.classes
        return c[c.index(curr) + 1:]

    def start_blocks(self, openhours, day):
        rsf = openhours
        rsf_yest = others.Others([rsfhours], day - datetime.timedelta(days = 1))
        rsf_yest= rsf_yest.create_block(rsfhours)
        earliest = self.get_earliest()
        blocks = []
        if rsf.start < earliest.start:
            new = TimeBlock(rsf.start, earliest.start, "No reservation")
            blocks.append(new)
        twelve =  day.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        if rsf_yest.end > twelve:
            new = TimeBlock(twelve, rsf_yest.end, "No reservation")
            blocks.append(new)
            blocks.append(self.closed_block(rsf_yest, day - datetime.timedelta(days = 1)))
        return blocks

    def closed_block(self, openhours, day):
        rsf = openhours
        rsf_tom = others.Others([rsfhours], day + datetime.timedelta(days = 1))
        print(rsf_tom.day.weekday())
        rsf_tom = rsf_tom.create_block(rsfhours)
        print(rsf_tom.time_til())

        return TimeBlock(rsf.end, rsf_tom.start, "-- RSF CLOSED --")
    
    #Add other classes to Block Tree
    def others_blocks(self, day, class_list):
        _others = others.Others(class_list, day)
        others_list = _others.block_list()
        return others_list
    
    def get_free_blocks(self):
        L = self.classes
        blocks = []
        for i, item in enumerate(L):
            if (i+1) < len(L):
                if item.end < L[i+1].start:
                    blocks.append(TimeBlock(item.end, L[i+1].start, "No reservation"))
        return blocks
    


    def finalize(self, day, _others):
        rsf = others.Others([rsfhours], day)
        rsf = rsf.create_block(rsfhours)
        for b in self.others_blocks(day, _others):
            self.add(b)
        
        for b in self.start_blocks(rsf, day):
            self.add(b)
        
        self.add(self.closed_block(rsf, day))

        for b in self.get_free_blocks():
            self.add(b)
