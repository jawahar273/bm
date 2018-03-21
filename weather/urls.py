from rest_framework import routers


from weather.views import AirPollutionView


router = routers.DefaultRouter()
router.register('air-pollution', AirPollutionView, base_name='air-pollution')

urlpatterns = router.urls
