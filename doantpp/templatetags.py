# templatetags.py

from django import template

register = template.Library()

@register.filter
def get_previous_city(city_totals, index):
    if index > 0:
        return city_totals[index - 1]['user_details__city']
    else:
        return None
