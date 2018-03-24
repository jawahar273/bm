import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


from packages.config import (PaymentTypeNumber,
                             PackageSettingsGeoloc as Geoloc)


# https://www.cloudamqp.com/plans.html

@receiver(user_signed_up)
def after_user_signed_up(sender, request, user, **kwargs):
    '''
    Active when user register/sign up with creating a setting
    object
    '''

    temp = PackageSettings(user=user)
    temp.save()


USERMODEL = get_user_model()


class MonthBudgetAmount(models.Model):
    '''
    The budget amount of the  months with unique key constrain with
    `month_year`
    and `user` field. Parent Model
    :model: `auth.User`.

    '''

    start_date = datetime.date(year=datetime.date.today().year,
                               month=datetime.date.today().month,
                               day=1)

    budget_amount = models.DecimalField(max_digits=10,
                                        decimal_places=2, default=0)
    month_year = models.DateField(default=start_date,
                                  validators=[
                                     RegexValidator(settings.BM_STANDARD_DATEFORMAT)
                                    ]
                                 )
    user = models.ForeignKey(USERMODEL, blank=True,
                             related_name='mba_USERMODEL',
                             on_delete=models.CASCADE)

    class Meta:
        unique_together = ('month_year', 'user')

    def __str__(self):
        return '{}`s Time line: {}'.format(self.user, self.month_year)


class ItemsList(models.Model):
    '''
    The items list is cumlative list of spending amount on
    each item that has be purchased. By making higher step approch
    to keep track of purchased based on date help in maintaing the
    process. Parent Model
    :model: `auth.User`.
    '''

    user = models.ForeignKey(USERMODEL, blank=True,
                             related_name='itemlist_USERMODEL',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, )
    place = models.CharField(max_length=50)
    group = models.CharField(max_length=30, blank=True)
    date = models.DateField(default=datetime.date.today,
                            validators=[
                                RegexValidator(settings.BM_STANDARD_DATEFORMAT)
                                ]
                            )
    total_amount = models.DecimalField(max_digits=7,
                                       decimal_places=2,
                                       default=0)
    temp = PaymentTypeNumber.default_type()['id']
    entry_type = models.PositiveSmallIntegerField(default=temp)

    class Meta:
        ordering = ['-id']
        get_latest_by = ['-date']

    def __str__(self):
        return 'Unique ID-{}: {}, {}'.format(self.id, self.name, self.date)


class Item(models.Model):
    '''
    The small token of the purchased item are stored. Parent Model
    :model: `packages.ItemsList`.
    '''

    items_list = models.ForeignKey(ItemsList,
                                   related_name='items',
                                   on_delete=models.CASCADE)
    name = models.CharField(max_length=10, default='')
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    def __str__(self):
        return '{}, {}'.format(self.name, self.amount)


class PackageSettings(models.Model):
    '''
    This setting field may not stable until their is fixed ones.
    '''

    user = models.ForeignKey(USERMODEL, blank=True,
                             related_name='package_settings',
                             on_delete=models.CASCADE)
    currency_details = models.TextField(max_length=100, default='', blank=True)
    #  force ask about monthly budget model in client.
    force_mba_update = models.CharField(default='Y', max_length=1)

    active_paytm = models.CharField(default='N', max_length=1)

    #  get/set the interval to get the geolocation from the user.
    temp_geoloc = Geoloc.interval_time()
    geoloc_interval = models.PositiveSmallIntegerField(default=temp_geoloc)

    def __str__(self):
        return '{}`s package setting'.format(self.user.username)
