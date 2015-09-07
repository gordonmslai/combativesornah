from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, timedelta
import timeblock
from models import Reservation


def index(request, _day=0, ref=0):
    print "DAY: " + str(_day)
    context = RequestContext(request)
    data = {}

    today = datetime.now()
    if int(_day) != 0:
        today = today + timedelta(days=int(_day))

    classes = Reservation.objects.filter(day_num=today.date().weekday(), user__isnull=False)
    Blocks = []
    for c in classes:
        start = c.get_start_dt(today.date())
        end = c.get_end_dt(today.date())
        new_block = timeblock.TimeBlock(start, end, c.user.name)
        Blocks.append(new_block)

    # DATA
    SortedBlocks = timeblock.BlockList(Blocks, today)
    SortedBlocks.finalize()
    data["SortedBlocks"] = SortedBlocks
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

    data["date"] = today.strftime("%a %b %d %Y")

    data["dayspast"] = int(_day) + 1

    data["daysprev"] = int(_day) - 1

    return render_to_response('index.jade', data, context)


def loading(request):
    context = RequestContext(request)
    data = {}

    return render_to_response('loading.jade', data, context)
