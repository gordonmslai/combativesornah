from __future__ import absolute_import
from scrape.models import Reservation, CombativesUser
from scrape.scrape import OrNahParser
from datetime import datetime
from lxml import html
from urllib2 import urlopen
import re


def clear_non_scraped():
    Reservation.objects.filter(user__is_scraped=False).delete()


def scrape():
    count = 0
    while (count < 3):
        P = get_parser()
        if P is not None:
            clear_reservations()
            get_reservations(P)
            break
        count += 1


def get_parser():
    url = urlopen("https://www.healcode.com/widgets/mb/schedules/cp32621nhv.js")
    tree = html.parse(url)
    root = tree.getroot()
    data_string = root.text_content()
    P = OrNahParser(data_string, datetime.today())
    try:
        assert P.str.count(P.today_str()) == 1
    except AssertionError:
        return None
    return P


def clear_reservations():
    print("CLEARING ALL SCRAPED RESERVATIONS")
    Reservation.objects.filter(user__is_scraped=True).delete()


def get_reservations(P):
    print("GETTING NEW RESERVATIONS")
    weekday = 6

    def get_next_day_loc():
        try:
            next_day = P.str.index("hc_date\\"[:])
        except ValueError:
            next_day = len(P.str)
        return next_day
    P.move_by(get_next_day_loc() + 1)

    while P.count < len(P.str):
        P.count = 0
        next_day = get_next_day_loc()
        # Check for Combatives
        a = str('combatives_rsf  \\')
        try:
            P.move_to(a)
        except ValueError:
            print("could not find 'combatives_rsf  \\'")
            break
        if P.count > next_day:  # ATTENTION If gone into the "next day" (NEEDS FIX/Test)
            weekday += 1
            continue

        # Find and go to class
        start = P.get_time(0)
        end = P.get_time(1)

        # Get name of class
        try:
            m = re.search('>(?!.*>.*\(Combatives, RSF\)).*(?=\(Combatives, RSF\))', P.str[:P.str.index(a)])  # Search for class before next instance of "combatives_rsf  \"
        except ValueError:
            m = re.search('>(?!.*>.*\(Combatives, RSF\)).*(?=\(Combatives, RSF\))', P.str[:len(P.str) - 1])
        name = m.group(0)[1:]

        # Get user object
        users = CombativesUser.objects.filter(name=name)
        if users.count() == 0:
            user = CombativesUser.objects.create(name=name, is_scraped=True)
        else:
            user = users[0]

        # Create Reservation
        Reservation.objects.create(day_num=weekday % 7, start_at=P.time_obj(start), end_at=P.time_obj(end), user=user)
