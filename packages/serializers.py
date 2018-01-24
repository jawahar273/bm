
from django.db.models import Sum
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from packages.models import ItemsList, Item, MonthBudgetAmount

from packages.serializers_childs.filter_nested_items import FilterNestedItems

from IPython import embed

class MonthBudgetAmountSerializer(serializers.ModelSerializer):

    class Meta:
        # list_serializer_class = FilterNestedItems
        model = MonthBudgetAmount
        fields = ('budget_amount', 'month_year','user_id', )
        def get_month(self, obj):
            embed()
            return '{0}-{1}'.format(obj.month_year.year, obj.month_year.month)

class ItemSerializer(serializers.ModelSerializer):

    amount = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        # list_serializer_class = FilterNestedItems
        model = Item
        fields = ('amount', 'name')

class ItemsListSerializer(WritableNestedModelSerializer):

    items = ItemSerializer(many=True, required=False)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, object):

        # if (object.items.total_amount == 0):
        # embed()

        def flat(e): 
            return (i[0] for i in e)
        amount = sum(flat(object.items.values_list('amount')))
        object.total_amount = amount
        object.save()
        return amount

    class Meta:
        model = ItemsList
        fields = ('id', 'name', 'place', 'group', 'date', 'items', 'total_amount', 'user_id', )
        # fields = ('__all__')
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('user_id')
        return ret
        

class ItemsListSerializerOnlyForListFun(serializers.ModelSerializer):
    # entry_link_item = serializers.SerializerMethodField('geli')

    # def geli(self, object):
    #     return 'entry/{}'.format(object.id)
    class Meta:
        model = ItemsList
        fields =  ('id', 'name', 'place', 'group', 'date', 'total_amount')