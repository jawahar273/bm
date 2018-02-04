from django.conf.urls import url
from rest_framework import routers
# from rest_framework_swagger.views import get_swagger_view

from packages.views import (ItemsListCreateView,
                            ItemCreateView, MonthBudgetAmountView, get_months,
                            get_range_mba, get_items_list_by_month,
                            get_all_group_in_itemslist)

router = routers.DefaultRouter()
router.register('itemslist', ItemsListCreateView, base_name='itemslist')
router.register('mba', MonthBudgetAmountView, base_name='mba')
# router.register('item',
#                 ItemCreateView)
regex_date_valid = r'[0-9\-]{10}'
# schema_view = get_swagger_view(title='Deliver API')
urlpatterns = [
   url(r'^get_months/(?P<start>{})/$'.format(regex_date_valid), get_months, name="get_month"),
   url(r'^get_months/(?P<start>{})/(?P<end>{})/$'.format(regex_date_valid, regex_date_valid), get_months, name="get_month"),
   url(r'^get_group_items/$', get_all_group_in_itemslist, name="get_group_list"),
   url(r'^get_items_list_by_month/(?P<start>{})/(?P<end>{})/$'.format(regex_date_valid, regex_date_valid), get_items_list_by_month, name="get_items_list_by_month"),
   url(r'^mba/(?P<start>{})/(?P<end>{})/$'.format(regex_date_valid, regex_date_valid),get_range_mba, name="range_mba"),
 ]
urlpatterns.extend(router.urls)
# urlpatterns += router.urls