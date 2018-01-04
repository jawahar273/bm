
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from packages.models import ItemsList, Item

from packages.serializers_childs.filter_nested_items import FilterNestedItems


class ItemSerializer(serializers.ModelSerializer):

    amount = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        # list_serializer_class = FilterNestedItems
        model = Item
        fields = ('amount', 'name')


class ItemsListSerializer(WritableNestedModelSerializer):

    items = ItemSerializer(many=True, required=False)

    def NewObject(self):
        return "df"

    class Meta:
        model = ItemsList
        fields = ('id', 'name', 'place', 'group', 'date', 'items')
        
