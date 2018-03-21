from rest_framework import serializers


class FilterNestedItems(serializers.ListSerializer):

    def to_representation(self, data):
        return super().to_representation(data)
