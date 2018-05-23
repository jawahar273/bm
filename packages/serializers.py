
# from django.db.models import Sum
from django.conf import settings

from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


from packages.models import ItemsList, Item, MonthBudgetAmount, PackageSettings


class MonthBudgetAmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonthBudgetAmount
        fields = ("budget_amount", "month_year", "user")

        def get_month(self, obj):
            return "user: {}-{}-{}".format(
                obj.user, obj.month_year.year, obj.month_year.month
            )


class ItemSerializer(serializers.ModelSerializer):

    amount = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = Item
        fields = ("amount", "name")


class ItemsListSerializer(WritableNestedModelSerializer):

    items = ItemSerializer(many=True, required=False)
    date = serializers.DateField(format=settings.BM_STANDARD_DATEFORMAT)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, object):

        def flat(e):

            return (i[0] for i in e)

        amount = sum(flat(object.items.values_list("amount")))
        object.total_amount = amount
        object.save()

        return amount

    class Meta:

        model = ItemsList
        fields = (
            "id",
            "name",
            "place",
            "group",
            "date",
            "items",
            "total_amount",
            "user",
        )

    def to_representation(self, instance):

        ret = super().to_representation(instance)
        ret.pop("user")

        return ret


class ItemsListSerializerOnlyForListFun(serializers.ModelSerializer):

    class Meta:

        model = ItemsList
        fields = ("id", "name", "place", "group", "date", "total_amount")


class ItemsGroupAndDate(serializers.ModelSerializer):

    class Meta:

        model = ItemsList
        fields = ("id", "group", "date")


class PackageSettingsSerializer(serializers.ModelSerializer):
    """
    The profile setting is not stable yet.
    """

    class Meta:

        model = PackageSettings
        fields = "__all__"
