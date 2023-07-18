from datetime import datetime

from django import template

register = template.Library()


@register.filter
def days_until(date):
    delta = datetime.date(date) - datetime.now().date()
    date_str = date.strftime("%H点%M分")
    day = abs(delta.days)
    if day == 0:
        return '今天 ' + date_str
    elif day == 1:
        return '昨天' + date_str
    elif (day / 365) >= 1:
        return str(int((day / 365))) + '年前'
    return str(day) + '天前'
