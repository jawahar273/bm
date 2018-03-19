from django.contrib import admin


from packages.models import ItemsList, Item, PackageSettings, MonthBudgetAmount

# Register your models here.
admin.site.register([ItemsList, Item, PackageSettings, MonthBudgetAmount])
