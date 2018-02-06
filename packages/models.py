import datetime
from django.contrib.auth import get_user_model
#from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from django.db import models

USERMODEL = get_user_model()

def onlyFiveRangeValidator(val):
    '''
    .. deprecated::
       The functioncality of this function has been removed.
    '''
    if(val % 1 == 0 or val % 1 == 0.5):
        ValidationError('given value "{}" is not multiple of 5'.format(val))

class MonthBudgetAmount(models.Model):
    '''
    The budget amount of the  months with unique key constrain with `month_year`
    and `user` field. Parent Model
    :model: `auth.User`.

    '''
    start_date = datetime.date(year=datetime.date.today().year, month=datetime.date.today().month, day=1) 
    
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month_year = models.DateField(default=start_date)
    user = models.ForeignKey(USERMODEL, blank=True, related_name='mba_USERMODEL',
              on_delete=models.CASCADE)

    class Meta:
        unique_together = ('month_year', 'user')

    def __str__(self):
        return 'Time line: {}- Budget Amount {} user {}'.format(self.month_year, self.budget_amount, self.user)        


class ItemsList(models.Model):
    '''
    The items list is cumlative list of spending amount on 
    each item that has be purchased. By making higher step approch
    to keep track of purchased based on date help in maintaing the 
    process. Parent Model
    :model: `auth.User`.
    '''
    name = models.CharField(max_length=20, unique=True, )
    place = models.CharField(max_length=20)
    group = models.CharField(max_length=10, blank=True)
    date = models.DateField(default=datetime.date.today)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    user = models.ForeignKey(USERMODEL, blank=True, related_name='itemlist_USERMODEL',
              on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        get_latest_by = ['-date']

    def __str__(self):
        return 'Group ID-{}: {}, {}'.format(self.id, self.name, self.date)

    def save(self, *args, **kwargs):
        self.group = self.group.lower()
        super().save(args, kwargs)




class Item(models.Model):
    '''
    The small token of the purchased item are stored. Parent Model
    :model: `packages.ItemsList`.  
    '''
    items_list = models.ForeignKey(ItemsList, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=10, default='')
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    def __str__(self):
        return '{}, {}'.format(self.name, self.amount)

    