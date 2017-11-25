import datetime


from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.db import models


def onlyFiveRangeValidator(value):
    val = value
    if(val % 1 == 0 or val % 1 == 0.5):
        ValidationError('given value "{}" is not multiple of 5'.format(value))


# Create your models here.
class ItemsList(models.Model):
    name = models.CharField(max_length=20)
    place = models.CharField(max_length=20)
    group = models.CharField(max_length=10, blank=True)
    date = models.DateField(default=datetime.date.today)
    # items = models.ForeignKey(Item, blank=True, null=True)

    def __str__(self):
        return 'Bill-{}: {}, {}'.format(self.id, self.name, self.date)


class Item(models.Model):

    items_list = models.ForeignKey(ItemsList, related_name='items')
    name = models.CharField(max_length=20)
    kg = models.FloatField(default=0,
                           validators=[MinValueValidator(0),
                                       MaxValueValidator(100),
                                       onlyFiveRangeValidator]
                           )
    quanity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return '{}, {} x {}'.format(self.name, self.quanity,
                                    self.kg)
