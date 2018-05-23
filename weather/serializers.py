
from rest_framework import serializers

from weather.models import GAS_TYPE_CHOICES, AirPollution, AirPollutionData


class AirPollutionDataSerializer(serializers.ModelSerializer):

    gas_type = serializers.ChoiceField(choices=GAS_TYPE_CHOICES)

    class Meta:

        model = AirPollutionData
        fields = (
            "data_base",
            "precision",
            "pressure",
            "value",
            "weather_date",
            "gas_type",
        )


class AirPollutionSerializer(serializers.ModelSerializer):

    data = AirPollutionDataSerializer(many=True, required=False)

    class Meta:

        model = AirPollution
        fields = ("data", "last_update", "location_lat", "location_lon")
