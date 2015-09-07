from django.test import TestCase
from django.db import IntegrityError
from scrape.models import Reservation, CombativesUser
from datetime import time


class TestReservation(TestCase):
    def setUp(self):
        self.start = time(5, 30)
        self.end = time(6, 30)
        self.user = CombativesUser.objects.create(is_scraped=False, name='Fencing', email='test@combatives.com')

    def test_fail_make_empty(self):
        self.assertRaises(IntegrityError, Reservation.objects.create)

    def test_fail_make_no_day_num(self):
        self.assertRaises(IntegrityError, Reservation.objects.create, start_at=self.start, end_at=self.end, user=self.user)

    def test_fail_make_no_start_at(self):
        self.assertRaises(IntegrityError, Reservation.objects.create, day_num=0, end_at=self.end, user=self.user)

    def test_fail_make_no_end_at(self):
        self.assertRaises(IntegrityError, Reservation.objects.create, day_num=0, start_at=self.start, user=self.user)

    def test_make(self):
        Reservation.objects.create(day_num=0, start_at=self.start, end_at=self.end, user=self.user)
        Reservation.objects.create(day_num=0, start_at=self.start, end_at=self.end)

    def test_get_reservation_from_user(self):
        self.assertEquals(self.user.reservation_set.count(), 0)
        Reservation.objects.create(day_num=0, start_at=self.start, end_at=self.end, user=self.user)
        self.assertEquals(self.user.reservation_set.count(), 1)
        Reservation.objects.create(day_num=1, start_at=self.start, end_at=self.end, user=self.user)
        Reservation.objects.create(day_num=2, start_at=self.start, end_at=self.end, user=self.user)
        self.assertEquals(self.user.reservation_set.count(), 3)


class TestCombativesUser(TestCase):
    def test_fail_make_empty(self):
        self.assertRaises(IntegrityError, CombativesUser.objects.create)

    def test_fail_make_no_name(self):
        self.assertRaises(IntegrityError, CombativesUser.objects.create, is_scraped=True)

    def test_make(self):
        CombativesUser.objects.create(name='Fencing')

    def test_unique(self):
        CombativesUser.objects.create(name='Fencing')
        self.assertRaises(IntegrityError, CombativesUser.objects.create, name='Fencing')
