from django.contrib import admin

from packages.models import ItemsList, Item

# Register your models here.
admin.site.register([ItemsList, Item])
