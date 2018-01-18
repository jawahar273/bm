from django.conf.urls import url
from rest_framework import routers
# from rest_framework_swagger.views import get_swagger_view

from packages.views import (ItemsListCreateView,
                            ItemCreateView, MonthBudgetAmountView, get_months, get_range_mba)

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
   url(r'^mba/(?P<start>{})/(?P<end>{})/$'.format(regex_date_valid, regex_date_valid),get_range_mba, name="range_mba"),
 ]
urlpatterns.extend(router.urls)
# urlpatterns += router.urls