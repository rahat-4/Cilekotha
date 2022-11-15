from django import template

from App_Order.models import Cart

register = template.Library()

@register.filter
def cart_count(user):
    cart_total = Cart.objects.filter(user=user, purchased=False)

    if cart_total.exists():
        return cart_total.count()
    else:
        return 0
