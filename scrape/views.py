from django.shortcuts import render, render_to_response
from django.template import RequestContext


from lxml import etree, html
from urllib2 import urlopen
import re, sys, inspect
import datetime, calendar
import classes
import rsfhours, others, timeblock
from scrape import OrNahParser



# Create your views here.
def index(request, _day = 0, ref = 0):
    print("started...")
    context = RequestContext(request)
    data = {}
    

    today = datetime.datetime.utcnow() - datetime.timedelta(hours = 8)
    
    if int(_day) != 0:
        today = today + datetime.timedelta(days = int(_day))

    f = open("string.db")
    P = OrNahParser(f.read(), today)
    print(today.weekday())

    if today.weekday() == 6:
        f.seek(0,0)
        _date = f.readline()[:len(P.today_str())]
        if _date != P.today_str():
            print("openurl")
            url = urlopen("https://www.healcode.com/widgets/mb/schedules/cp32621nhv.js")
            
            tree = html.parse(url)
            root = tree.getroot()

            for child in root:
                if child.tag == "body":
                    pointer = child
                    break

            data_string = root.text_content()
            P = OrNahParser(data_string, today)
            try:
                assert P.str.count(P.today_str()) == 1
            except AssertionError:
                if ref > 2:
                    print("failed.")
                    return fail(request)
                else:
                    print("retrying...")
                    return fail1(request)            
            f = open("string.db", "w")
            f.write(P.today_str() + "\n")
            f.write(data_string)
            f.flush()
            f.close()
            print("written")

    print("loaded string")
    try:
        print(P.str)
        assert P.str.count(P.today_str()) == 1
    except AssertionError:
        print("openurl")
        url = urlopen("https://www.healcode.com/widgets/mb/schedules/cp32621nhv.js")
        
        tree = html.parse(url)
        root = tree.getroot()

        for child in root:
            if child.tag == "body":
                pointer = child
                break

        data_string = root.text_content()
        P = OrNahParser(data_string, today)
        try:
            assert P.str.count(P.today_str()) == 1
        except AssertionError:
            if ref > 2:
                print("failed.")
                return fail(request)
            else:
                print("retrying...")
                return fail1(request)            
        f = open("string.db", "w")
        f.write(P.today_str() + "\n")
        f.write(data_string)
        f.flush()
        f.close()
        print("written")
    # Find and go to today's date in schedule
    P.str = P.str[1:]
    P.move_to(P.today_str())
    P.count = 0    
    Blocks = []
    
    other_classes = []
    for name, value in inspect.getmembers(classes):
        if inspect.ismodule(value):
            other_classes.append(value)


    # Get index for tomorrow schedule
    try:
        next_day = P.str.index("hc_date\\"[:])
    except ValueError:
        next_day = len(P.str)

    while P.count < next_day:
        # Check for Combatives
        a = str('combatives_rsf\\" s')
        try:
            P.move_to(a)
        except ValueError:
            break
        if P.count > next_day:
            break
        # Find and go to class
        start = P.get_time(0)
        end = P.get_time(1)

        # Get name of class
        try:
            m = re.search('>(?!.*>.*\(Combatives, RSF\)).*(?=\(Combatives, RSF\))', P.str[:P.str.index(a[:])])
        except ValueError:
            m = re.search('>(?!.*>.*\(Combatives, RSF\)).*(?=\(Combatives, RSF\))', P.str[:len(P.str)-1])
        name = m.group(0)[1:]

        # Add block to BlockTree
        new_block = timeblock.TimeBlock(P.time_obj(start), P.time_obj(end), name)
        Blocks.append(new_block)


    #DATA
    SortedBlocks = timeblock.BlockList(Blocks)
    SortedBlocks.finalize(today, other_classes)
    data["SortedBlocks"] = SortedBlocks

    for b in SortedBlocks.classes:
        print(b.name)

    curr = SortedBlocks.get_current()

    data["curr"] = curr
    if int(_day) != 0:
        data["curr"] = None    
        curr_list = SortedBlocks.classes
    else:
        curr_list = SortedBlocks.curr_list()
    data["curr_list"] = curr_list
    for b in curr_list:
        print(b.name)

    data["date"] = calendar.day_name[today.weekday()] + ", " + P.today_str()

    data["dayspast"] = int(_day) + 1

    data["daysprev"] = int(_day) - 1

    return render_to_response('index.jade', data, context)

def refresh(request):
    context = RequestContext(request)
    data = {}

    # url = urlopen("https://www.healcode.com/widgets/mb/schedules/cp32621nhv.js")

    # tree = html.parse(url)
    # root = tree.getroot()

    # for child in root:
    #     if child.tag == "body":
    #         pointer = child
    #         break

    # data_string = root.text_content()
    # Blocks = []
    # today = datetime.datetime.today()
    # other_classes = [fencing, calstaryoga]
    
    # P = OrNahParser(data_string)


    return render_to_response('refresh.jade', data, context)

def fail1(request):
    context = RequestContext(request)
    data = {}

    return render_to_response('fail1.jade', data, context)

def fail(request):
    context = RequestContext(request)
    data = {}

    return render_to_response('fail.jade', data, context)

def index2(request, _ref):
    return index(request, ref = _ref)

def loading(request):
    context = RequestContext(request)
    data = {}

    return render_to_response('loading.jade', data, context)
