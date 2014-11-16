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
def index(request, _day = '0', ref = 0):
    print("started...")
    context = RequestContext(request)
    data = {}
    
    today = datetime.datetime.today() - datetime.timedelta(hours = 8)

    print(today.time())
    
    if int(_day) != 0:
        today = today + datetime.timedelta(days = int(_day))
    
    url = urlopen("https://www.healcode.com/widgets/mb/schedules/cp32621nhv.js")

    tree = html.parse(url)
    root = tree.getroot()

    for child in root:
        if child.tag == "body":
            pointer = child
            break

    data_string = root.text_content()
    Blocks = []
    
    other_classes = []
    for name, value in inspect.getmembers(classes):
        if inspect.ismodule(value):
            other_classes.append(value)

    P = OrNahParser(data_string, today)
    print("loaded string")
    # Find and go to today's date in schedule
    try:
        assert P.str.count(P.today_str()) == 1
        # assert 0 == 1
    except AssertionError:
        if ref > 0:
            return fail(request)
        else:
            print("Schedule could not be accessed at this time. Please check again in 10 minutes.")
            # return refresh(request)
            return index2(request)

    P.move_to(P.today_str())
    P.count = 0

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

    curr = SortedBlocks.get_current()
    data["curr"] = curr

    curr_list = SortedBlocks.curr_list()
    data["curr_list"] = curr_list

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

def fail(request):
    context = RequestContext(request)
    data = {}

    return render_to_response('fail.jade', data, context)

def index2(request):
    return index(request, ref = 1)

def loading(request):
    context = RequestContext(request)
    data = {}

    return render_to_response('loading.jade', data, context)
