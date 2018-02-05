from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.

    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    profile_url = models.URLField(default="")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

USERMODEL = get_user_model()
class UserProfileSettings(models.Model):
    """
       this setting field may not stable until their is fixed ones.
    """
    user = models.ForeignKey(USERMODEL, blank=True, related_name='user_profile_setting',
              on_delete=models.CASCADE)
    first_name = models.CharField(_('First Name'), blank=True, max_length=40)
    last_name = models.CharField(_('Last Name'), blank=True, max_length=40)
    gender = models.CharField(_('Gender'), max_length=7)
    email = models.EmailField()
    currency_details = models.TextField(_('Currency Details'), max_length=100, default='')

