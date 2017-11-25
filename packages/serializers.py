
from rest_framework import serializers

from packages.models import ItemsList, Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('name', 'kg', 'quanity', 'items_list')


class ItemsListSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True, required=False)

    class Meta:
        model = ItemsList
        fields = ('name', 'place', 'group', 'date', 'items')
