from django.shortcuts import render, redirect, get_object_or_404
from apps.basket.models import Basket, BasketItem
from apps.products.models import Event, Merch
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.checkout.models import Order
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def basket_view(request):
    # Clear any old Django messages from previous sessions
    storage = messages.get_messages(request)
    list(storage)

    basket = None
    subtotal = Decimal('0.00')
    items_with_fees = []  # List to store items + calculated fees
    delivery_charge = Decimal('0.00')

    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)

        for item in basket.items.all():
            item.booking_fee = Decimal('0.00')
            item.delivery_fee = Decimal('0.00')

            # Event items: booking fee
            if item.event:
                item.booking_fee = (item.event.price * Decimal('0.10')).quantize(Decimal('0.01'))

            # Merch items: delivery charge 
            if item.merch:
                base_fee = Decimal('5.00')
                extra_fee_per_item = (base_fee * Decimal('0.50')).quantize(Decimal('0.01'))

                if item.quantity == 1:
                    item.delivery_fee = base_fee
                else:
                    item.delivery_fee = base_fee + (extra_fee_per_item * (item.quantity - 1))

                item.delivery_fee = item.delivery_fee.quantize(Decimal('0.01'))

            line_total = item.line_total
            subtotal += line_total + (item.booking_fee * item.quantity) + item.delivery_fee

            # Store each item with its calculated fee
            items_with_fees.append(item)

        last_order = (
            Order.objects.filter(user=request.user, status="pending")
            .order_by("-created_at")
            .first()
        )

    # Add delivery charge to subtotal
    basket_total = subtotal 

    return render(request, 'basket/basket.html', {
        'basket': basket,
        'basket_items': items_with_fees,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge, 
        'basket_total': basket_total,       
        'quantity_options': range(1, 7),
        'page_title': "Basket",
        'last_order': last_order,
    })


def add_event_to_basket(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')

    basket, created = Basket.objects.get_or_create(user=request.user)
    event = get_object_or_404(Event, id=event_id)

    item, created = BasketItem.objects.get_or_create(basket=basket, event=event)
    if not created:
        item.quantity = min(item.quantity + 1, 6)  # Max 6 tickets
        item.save()

    return redirect('basket:basket_view')


def add_merch_to_basket(request, merch_id):
    if not request.user.is_authenticated:
        return redirect('login')

    basket, created = Basket.objects.get_or_create(user=request.user)
    merch = get_object_or_404(Merch, id=merch_id)

    quantity = int(request.POST.get("quantity", 1))
    if quantity < 1: quantity = 1
    elif quantity > 6: quantity = 6

    size = request.POST.get("size", "")

    item, created = BasketItem.objects.get_or_create(basket=basket, merch=merch, size=size)
    if created:
        item.quantity = quantity 
    else:
        item.quantity += quantity  
    item.save()

    return redirect('basket:basket_view')


def update_basket_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(BasketItem, id=item_id)
        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            quantity = 1
        elif quantity > 6:
            quantity = 6

        item.quantity = quantity
        item.save()
    else:
        item.delete()

    return redirect("basket:basket_view")


def delete_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(BasketItem, id=item_id)
        item.delete()
    return redirect("basket:basket_view")


def continue_shopping(request):
    print("Continue shopping view triggered")
    # Get previous URL from the HTTP header (safe fallback)
    previous_page = request.META.get('HTTP_REFERER')
    basket_url = request.build_absolute_uri(reverse('basket:basket_view'))
    merch_url = reverse('products:merch_list')

    if not previous_page or previous_page == basket_url:
        previous_page = merch_url

    print("Continue shopping view triggered")

    return HttpResponseRedirect(previous_page)