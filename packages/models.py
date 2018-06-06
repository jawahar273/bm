import datetime
import os
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.account.signals import user_signed_up

from packages.config import PaymentTypeNumber, PackageSettingsGeoloc as Geoloc


@receiver(user_signed_up)
def after_user_signed_up(sender, request, user, **kwargs):
    """
    Active when user register/sign up with creating a setting
    object
    """

    temp = PackageSettings(user=user)
    temp.save()


USERMODEL = get_user_model()


class TimeStrampModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MonthBudgetAmount(models.Model):
    """
    The budget amount of the  months with unique key constrain with
    `month_year`
    and `user` field. Parent Model
    :model: `auth.User`.

    """

    start_date = datetime.date(
        year=datetime.date.today().year, month=datetime.date.today().month, day=1
    )

    budget_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    month_year = models.DateField(
        default=start_date, validators=[RegexValidator(settings.BM_REGEX_DATE_FORMAT)]
    )

    user = models.ForeignKey(
        USERMODEL, blank=True, related_name="mba_USERMODEL", on_delete=models.CASCADE
    )

    class Meta:

        unique_together = ("month_year", "user")

    def __str__(self):

        return "{}`s Time line: {}".format(self.user, self.month_year)


class ItemsList(models.Model):
    """
    The items list is cumlative list of spending amount on
    each item that has be purchased. By making higher step approch
    to keep track of purchased based on date help in maintaing the
    process. Parent Model
    :model: `auth.User`.
    """

    user = models.ForeignKey(
        USERMODEL,
        blank=True,
        related_name="itemlist_USERMODEL",
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=50, unique=True)

    place = models.CharField(max_length=50)

    group = models.CharField(max_length=30, blank=True)

    date = models.DateField(
        default=datetime.date.today,
        validators=[RegexValidator(settings.BM_STANDARD_DATEFORMAT)],
    )

    total_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    temp = PaymentTypeNumber.default_type()
    entry_type = models.PositiveSmallIntegerField(default=temp)

    class Meta:

        ordering = ["-id"]
        get_latest_by = ["-date"]

    def __str__(self):

        return "Unique ID-{}: {}, {}, Group: {}".format(
            self.id, self.name, self.date, self.group
        )


@receiver(post_save, sender=ItemsList)
def post_save_items_list(sender, instance, **kwargs):
    pass


class Item(models.Model):
    """
    The small token of the purchased item are stored. Parent Model
    :model: `packages.ItemsList`.
    """

    items_list = models.ForeignKey(
        ItemsList, related_name="items", on_delete=models.CASCADE
    )

    name = models.CharField(max_length=10, default="")

    amount = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    def __str__(self):
        return "{}, {}".format(self.name, self.amount)


def validate_country_code_(value):
    file_location = os.path.join(settings.STATIC_ROOT, "js", "")
    file_location += settings.BM_CURRENCY_DETAIL_JSON_FILE

    with open(file_location) as file:
        content = file.read()
        content = json.dumps(content)
        if not content.get(value):
            temp = (
                "Contry code is not a valid one. Please" " choose a valid contry code"
            )
            return ValidationError(temp)


def validate_max_time_interval(value):
    """This method is used as validator
    to check range of times.
    """
    if value < Geoloc.min_interval_time() and value > Geoloc.max_interval_time():
        return ValidationError(
            "Can not Exceed the max or"
            "min of interval of 10 mins 8 hours"
            "repecatively" % (Geoloc.max_interval_time, Geoloc.min_interval_time)
        )


class PackageSettings(models.Model):
    """
    This setting field may not stable until their is fixed ones.
    """

    user = models.ForeignKey(
        USERMODEL, blank=True, related_name="package_settings", on_delete=models.CASCADE
    )

    currency_details = models.CharField(max_length=3, default="USD", blank=True)

    #  force ask about monthly budget model in client.
    force_mba_update = models.CharField(default="Y", max_length=1)

    active_paytm = models.CharField(default="N", max_length=1)

    #  get/set the interval to get the geolocation from the user.
    #  getting the config.
    temp_geoloc = Geoloc.interval_time()
    #  Value must be stored as minutes.
    geoloc_interval = models.PositiveSmallIntegerField(
        default=temp_geoloc, validators=[validate_max_time_interval]
    )

    def __str__(self):

        return "{}`s package setting".format(self.user.username)


class ItemsGroupLog(TimeStrampModel):

    group = models.CharField(max_length=30, blank=True, unique=True)


# class UploadKeyList(models.Model):

#     user = models.ForeignKey(
#         USERMODEL, blank=True, related_name="upload_key_list", on_delete=models.CASCADE
#     )
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return "ID: {}, User: {}".format(self.id, self.user.id)


# class UploadKey(models.Model):

#     content_key = models.IntegerField()
#     upload_key_list = models.ForeignKey(
#         UploadKeyList, related_name="upload_keys", on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return "ID: {}, content key:".format(self.id, self.content_key)
