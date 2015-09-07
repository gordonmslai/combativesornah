from django.test import TestCase
from scrape import tasks
from datetime import time
from scrape.models import Reservation, CombativesUser


class TestScrape(TestCase):
    def setUp(self):
        self.start = time(5, 30)
        self.end = time(6, 30)
        self.user = CombativesUser.objects.create(is_scraped=False, name='Fencing', email='test@combatives.com')
        self.user2 = CombativesUser.objects.create(is_scraped=True, name='Zumba', email='test@combatives.com')
        for x in range(4):
            Reservation.objects.create(day_num=x, start_at=self.start, end_at=self.end, user=self.user)
            Reservation.objects.create(day_num=x, start_at=self.start, end_at=self.end, user=self.user2)
            Reservation.objects.create(day_num=x, start_at=self.start, end_at=self.end, user=self.user2)
            Reservation.objects.create(day_num=x, start_at=self.start, end_at=self.end)

    def test_get_parser(self):
        P = tasks.get_parser()
        self.assertTrue(P is not None)

    def test_clear_reservations(self):
        self.assertEquals(Reservation.objects.count(), 16)
        tasks.clear_reservations()
        self.assertEquals(Reservation.objects.count(), 8)

    def test_get_reservations(self):
        P = tasks.get_parser()
        tasks.clear_reservations()
        self.assertEquals(Reservation.objects.count(), 8)
        tasks.get_reservations(P)
        self.assertTrue(Reservation.objects.count() > 8)

    def test_clear_non_scraped(self):
        self.assertEquals(Reservation.objects.count(), 16)
        tasks.clear_non_scraped()
        self.assertEquals(Reservation.objects.count(), 12)
