from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from .models import BillingAddress
from .forms import AddressForm
from App_Order.models import Order, Cart

#payment
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import requests
import socket

# Create your views here.
@login_required
def checkout(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    form = AddressForm(instance=saved_address)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            messages.success(request, "Shipping address saved.")
            return redirect('App_Payment:checkout')
    view_order = Order.objects.filter(user=request.user, ordered=False)
    total = view_order[0].total_order()
    if view_order.exists():
        orders = view_order[0].order_items.all()
    dict = {'form':form, 'orders':orders, 'total':total, 'saved_address':saved_address}
    return render(request, 'App_Payment/checkout.html', dict)


@login_required
def status(request):
    saved_address = BillingAddress.objects.get_or_create(user=request.user)[0]
    
    if not saved_address.is_fully_filled():
        messages.warning(request, "Please fill up your shipping address.")
        return redirect('App_Payment:checkout')
    
    if not request.user.profile.is_fully_filled():
        messages.warning(request, "Please fill up your profile address.")
        return redirect('App_Login:change_profile')

    store_id = "abc63037a6d8fcc3"
    api_key = "abc63037a6d8fcc3@ssl"
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=api_key)

    status_url = request.build_absolute_uri(reverse("App_Payment:payment_status"))
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)

    order = Order.objects.filter(user=request.user, ordered=False)[0].order_items.all()
    order_qs = Order.objects.filter(user=request.user, ordered=False)[0]
    # cart = Cart.objects.filter(user=request.user, purchased=False)
    category = order[0].item.category.title
    name = order[0].item.name 

    mypayment.set_product_integration(total_amount=Decimal(order_qs.total_order()), currency='BDT', product_category=category, product_name=name, num_of_item=order.count(), shipping_method='Courier', product_profile='None')

    current_user = request.user.profile
    mypayment.set_customer_info(name=current_user.full_name, email=request.user.email, address1=current_user.address_1, address2=current_user.address_1, city=current_user.city, postcode=current_user.zip_code, country=current_user.country, phone=current_user.phone)

    mypayment.set_shipping_info(shipping_to=current_user.username, address=saved_address.address, city=saved_address.city, postcode=saved_address.zipcode, country=saved_address.country)

    # # If you want to post some additional values
    # mypayment.set_additional_values(value_a=request.user.email, value_b='portalcustomerid', value_c='1234', value_d='uuid')

    response_data = mypayment.init_payment()
    return redirect(response_data['GatewayPageURL'])


@csrf_exempt
def payment_status(request):
    
    if request.method == 'POST' or request.method == 'post':
        payment_state = request.POST

        if payment_state['status'] == 'VALID':
            tran_id = payment_state['tran_id']
            val_id = payment_state['val_id']

            messages.success(request, "Payment successfully completed.")
            return HttpResponseRedirect(reverse('App_Payment:purchased_order', kwargs=({'val_id':val_id, 'tran_id':tran_id})))
        elif payment_state['status'] == 'FAILED':
            messages.warning(request, "Payment not completed successfully. Try again. Note: AUTO REDIRECT AFTER 5 SECONDS.")
        else:
            messages.warning(request, "Payment Cancelled. Try again. Note: AUTO REDIRECT AFTER 5 SECONDS.")

    return render(request, 'App_Payment/payment_status.html')

@login_required
def purchased_order(request,val_id,tran_id):
    order = Order.objects.filter(user=request.user, ordered=False)[0]
    order.order_id = tran_id
    order.payment_id = val_id
    order.ordered = True
    order.save()

    cart = Cart.objects.filter(user=request.user, purchased=False)

    for item in cart:
        item.purchased = True
        item.save()
    
    return redirect('App_Shop:home')

@login_required
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        dict = {'orders':orders}
    except:
        messages.warning(request, "You don't have an active order.")
    return render(request, 'App_Payment/order.html', dict)