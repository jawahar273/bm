
from rest_framework import serializers

from weather.models import GAS_TYPE_CHOICES, AirPollution, AirPollutionData


class AirPollutionDataSerializer(serializers.ModelSerializer):

    class Meta:

        model = AirPollutionData
        fields = '__all__'


class AirPollutionSerializer(serializers.ModelSerializer):

    gas_type = serializers.ChoiceField(choices=GAS_TYPE_CHOICES)
    data = AirPollutionDataSerializer(many=True, required=False)

    class Meta:

        model = AirPollution
        fields = ('gas_type', 'data', 'last_update',
                  'location_lat', 'location_lon')
