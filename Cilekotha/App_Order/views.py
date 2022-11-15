from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from App_Shop.models import Product
from .models import Cart, Order

# Create your views here.
@login_required
def add_to_cart(request,pk):
    items = get_object_or_404(Product, pk=pk)
    check_cart = Cart.objects.get_or_create(item=items, user=request.user, purchased=False)
    check_user_order = Order.objects.filter(user=request.user, ordered=False)
    add_cart = check_cart[0]
    if check_user_order.exists():
        order = check_user_order[0]
        if order.order_items.filter(item=items).exists():
            add_cart.quantity += 1
            add_cart.save()
            messages.info(request, "This item quantity was update.")
            return redirect('App_Shop:home')
        else:
            order.order_items.add(add_cart)
            messages.info(request, "This item was added to the cart.")
            return redirect('App_Shop:home')
    else:
        add_order = Order(user=request.user, ordered=False)
        add_order.save()
        add_order.order_items.add(add_cart)
        messages.info(request, "Order updated.")
        return redirect('App_Shop:home')

@login_required
def view_cart(request):
    see_cart = Cart.objects.filter(user=request.user, purchased=False)
    see_order =  Order.objects.filter(user=request.user, ordered=False)
    if see_order.exists() and see_cart.exists():
        return render(request, 'App_Order/cart.html', {'see_cart':see_cart, 'see_order':see_order[0]})
    else:
        messages.warning(request, "Your cart is empty.")
        return redirect('App_Shop:home')

@login_required
def remove_from_cart(request,pk):
    item = get_object_or_404(Product, pk=pk)
    remove_cart = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
    remove_order = Order.objects.filter(user=request.user, ordered=False)
    if remove_order.exists():
        r_order = remove_order[0]
        if r_order.order_items.filter(item=item).exists():
            r_order.order_items.remove(remove_cart)
            remove_cart.delete()
            messages.warning(request, f"{item.name} was remove from your cart.")
            return redirect("App_Order:view_cart")
        else:
            messages.info(request, "This item is not in your cart.")
            return redirect("App_Shop:home")
    else:
        messages.info(request, "You didn't do any order yet.")
        return redirect("App_Shop:home")

@login_required
def increase_quantity(request,pk):
    item = get_object_or_404(Product, pk=pk)
    inc_cart = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
    inc_order = Order.objects.filter(user=request.user, ordered=False)

    if inc_order.exists():
        increase_order = inc_order[0]
        if increase_order.order_items.filter(item=item).exists():
            inc_cart.quantity += 1
            inc_cart.save()
            return redirect('App_Order:view_cart')
        else:
            messages.info(request, "This item is not in your cart")
            return redirect('App_Shop:home')
    else:
        messages.warning("You didn't do any order yet.")
        return redirect('App_Shop:home')

@login_required
def decrease_quanity(request,pk):
    item = get_object_or_404(Product, pk=pk)
    dec_cart = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
    dec_order = Order.objects.filter(user=request.user, ordered=False)

    if dec_order.exists():
        decrease_order = dec_order[0]
        if decrease_order.order_items.filter(item=item).exists():
            if dec_cart.quantity > 1:
                dec_cart.quantity -= 1
                dec_cart.save()
                return redirect('App_Order:view_cart')
            else:
                decrease_order.order_items.remove(dec_cart)
                dec_cart.delete()
                return redirect('App_Order:view_cart')
        else:
            messages.info(request, "This item is not in your cart")
            return redirect('App_Shop:home')
    else:
        messages.warning("You didn't do any order yet.")
        return redirect('App_Shop:home')