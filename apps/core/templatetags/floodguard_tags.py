from django import template

register = template.Library()


@register.filter(name='split')
def split_filter(value, delimiter=','):
    """Split a string by delimiter. Usage: "a,b,c"|split:"," """
    return str(value).split(delimiter)


@register.filter(name='get_item')
def get_item(lst, index):
    """Safe list index access. Usage: mylist|get_item:0 """
    try:
        return lst[int(index)]
    except (IndexError, TypeError, ValueError):
        return ''
