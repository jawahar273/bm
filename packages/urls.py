from django.conf.urls import url
from rest_framework import routers

from packages.views import (ItemsListCreateView, ItemCreateView,
                            MonthBudgetAmountView, PackageSettingsView,
                            itemlist_get_by_months,
                            get_range_mba,
                            get_all_group_in_itemslist,
                            get_currency)

router = routers.DefaultRouter()
router.register('itemslist', ItemsListCreateView, base_name='itemslist')
router.register('mba', MonthBudgetAmountView, base_name='mba')
# router.register('settings', PackageSettingsView, base_name='package_settings')
regex_date_valid = r'[0-9\-]{10}'

urlpatterns = [
   url(r'^settings/', PackageSettingsView, name='package_settings'),
   # url(r'^get_months/(?P<start>{})/$'.format(regex_date_valid), get_months, name="get_month"),
   # url(r'^get_months/(?P<start>{})/(?P<end>{})/$'.format(regex_date_valid, regex_date_valid), get_months, name="get_month"),
   url(r'^itemslist/(?P<start>{})/(?P<end>{})/$'.format(regex_date_valid, regex_date_valid), itemlist_get_by_months, name="itemslist_get_by_month"),
   url(r'^get_group_items/$', get_all_group_in_itemslist, name="get_group_list"),
   url(r'^mba/(?P<start>{})/(?P<end>{})/$'.format(regex_date_valid, regex_date_valid),get_range_mba, name="range_mba"),
   url(r'currency', get_currency, name='currency' )
 ]
urlpatterns.extend(router.urls)
