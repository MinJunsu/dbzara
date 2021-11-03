from django.contrib import admin
from .models import Cinema, Theater, Seat


# Register your models here.
@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'main_region', 'sub_region', 'address', 'grade']


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['id', 'cinema', 'seat', 'category', 'name', 'floor']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'columns', 'rows']
