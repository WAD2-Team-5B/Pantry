from django import template

register = template.Library()

@register.filter(name='round_num')
def round_num(value):
    return "{:.2f}".format(round(value,2))  # Round to precisely 2 d.p.