from django.contrib import admin

from .models import Pizza, Burger, Restaurant

admin.site.register(Pizza)
admin.site.register(Burger)
admin.site.register(Restaurant)