from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value from a dictionary for the given key."""
    return dictionary.get(int(key), 0)

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    return float(value) * float(arg)

@register.filter
def filter_by_day(business_hours, day_num):
    """Filters business hours by day number."""
    try:
        day_num = int(day_num)
        for hours in business_hours:
            if hours.day == day_num:
                return hours
    except (ValueError, AttributeError):
        pass
    return None
