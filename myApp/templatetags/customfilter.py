import datetime

from django import template

# 实例化自定义过滤器注册对象

register = template.Library()


# name代表在模板中使用的过滤器名称
@register.filter(name='sub1')
def sub(value, arg):  # 参数最多两个
    """
    :param value: 传给sub过滤的值
    :param arg: sub自带的参数
    """
    return value + str(arg)


@register.filter(name='time_ago')
def time_ago(value):
    '''
    1. 1分钟内，显示刚刚
    2. 1小时内，显示xx分钟前
    3. 24小时内，显示xx小时前
    4. 30天内，显示xx天前
    5. 大于30天，显示具体时间
    '''
    if not isinstance(value, datetime.datetime):
        return value
    now = datetime.datetime.now()
    timestamp = (now - value).total_seconds()
    if timestamp <= 60 and timestamp < 60 * 60:
        return '{}分钟前'.format(int(timestamp / 60))
    elif 60 * 60 <= timestamp < 60 * 60 * 24:
        return '{}小时前'.format(int(timestamp / 60 / 60))
    elif 60 * 60 * 24 < timestamp < 60 * 60 * 24 * 30:
        return '{}天前'.format(int(timestamp / 60 / 60 / 24))
    else:
        return value.strftime('%Y-%m-%d %H:%M')
