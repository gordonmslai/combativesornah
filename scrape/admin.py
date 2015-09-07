from django.contrib import admin
from .models import Reservation, CombativesUser, OpenHours, Update


class ReservationInline(admin.TabularInline):
    model = Reservation
    exclude = ('open_hours',)


@admin.register(CombativesUser)
class CombativesUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_scraped')
    ordering = ('is_scraped',)
    list_filter = ('is_scraped',)
    inlines = [ReservationInline]
    exclude = ('is_scraped',)


class OpenHoursInline(admin.TabularInline):
    model = Reservation
    exclude = ('user',)


@admin.register(OpenHours)
class OpenHoursAdmin(admin.ModelAdmin):
    inlines = [OpenHoursInline]


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    ordering = ('-date_updated',)
    list_display = ('date_updated',)
