from carts.utils import get_user_carts
from django import template

register = template.Library()


@register.simple_tag()
def user_carts(request):
    return get_user_carts(request)
