from django.conf.urls import url
from rest_framework import routers
# from rest_framework_swagger.views import get_swagger_view

from packages.views import (ItemsListCreateView,
                            ItemCreateView)

router = routers.DefaultRouter()
router.register('itemslist', ItemsListCreateView, base_name='itemslist')
# router.register('item',
#                 ItemCreateView)

# schema_view = get_swagger_view(title='Deliver API')
urlpatterns = [
   # url(r'^$', schema_view)
 ]
urlpatterns.extend(router.urls)
# urlpatterns += router.urls