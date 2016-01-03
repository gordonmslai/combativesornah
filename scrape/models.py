from django.db import models
from datetime import datetime, timedelta


class Reservation(models.Model):
    day_num = models.IntegerField(choices=[(i, i) for i in range(7)], help_text='0-Monday, 6-Sunday')
    start_at = models.TimeField()
    end_at = models.TimeField()
    user = models.ForeignKey('CombativesUser', null=True, default=None)
    open_hours = models.ForeignKey('OpenHours', null=True, default=None)

    def __unicode__(self):
        return 'Day:{}, {}-{}'.format(self.day_num, self.start_at, self.end_at)

    def get_start_dt(self, date):
        return datetime.combine(date, self.start_at)

    def get_end_dt(self, date):
        if self.start_at > self.end_at:
            return datetime.combine(date + timedelta(days=1), self.end_at)
        return datetime.combine(date, self.end_at)


class CombativesUser(models.Model):
    name = models.CharField(max_length=50, default=None, unique=True)
    description = models.CharField(max_length=140, blank=True)
    is_scraped = models.BooleanField(default=False, verbose_name='Auto Generated')
    email = models.EmailField()
    website = models.URLField(blank=True)

    def __unicode__(self):
        return self.name


class OpenHours(models.Model):
    pass


class Update(models.Model):
    date_updated = models.DateField()
    updates = models.TextField()

class WeeklyDatabaseUpdate(models.Model):
    last_updated = models.DateField()

