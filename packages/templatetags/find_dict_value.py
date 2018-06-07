from django import template

from packages.utils import find_dict_value as find_value
from packages.config import PAYMENTTYPE


register = template.Library()


@register.simple_tag
def find_dict_value_payment(key_word):

    return find_value(key_word, PAYMENTTYPE)
