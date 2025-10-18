from django.shortcuts import render, redirect, get_object_or_404
from apps.basket.models import Basket, BasketItem
from apps.products.models import Event, Merch
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.checkout.models import Order
from decimal import Decimal
from django.http import HttpResponseRedirect
from django.urls import reverse


def calculate_fees(items):
    subtotal = Decimal('0.00')
    delivery_charge = Decimal('0.00')
    order_items = []

    for item in items:
        # Base total for this item
        line_total = item.price * item.quantity

        # Default values
        item.booking_fee = Decimal('0.00')
        item.delivery_fee = Decimal('0.00')

        # --- Booking fee (10% of total ticket value) ---
        if getattr(item, 'event', None):
            item.booking_fee = (line_total * Decimal('0.10')).quantize(Decimal('0.01'))
            item.total_with_fees = (line_total + item.booking_fee).quantize(Decimal('0.01'))

        # --- Delivery fee for merch ---
        elif getattr(item, 'merch', None):
            base_fee = Decimal('5.00')
            extra_fee_per_item = (base_fee * Decimal('0.50')).quantize(Decimal('0.01'))

            if item.quantity == 1:
                item.delivery_fee = base_fee
            else:
                item.delivery_fee = base_fee + (extra_fee_per_item * (item.quantity - 1))

            item.delivery_fee = item.delivery_fee.quantize(Decimal('0.01'))
            item.total_with_fees = (line_total + item.delivery_fee).quantize(Decimal('0.01'))
            delivery_charge += item.delivery_fee

        # --- Add to subtotal ---
        subtotal += item.total_with_fees
        order_items.append(item)

    # Final totals
    basket_total = subtotal
    return order_items, subtotal, delivery_charge, basket_total


@login_required
def basket_view(request):
    # Clear old messages
    storage = messages.get_messages(request)
    list(storage)

    basket = None
    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
        items_with_fees, subtotal, delivery_charge, basket_total = calculate_fees(basket.items.all())

        last_order = (
            Order.objects.filter(user=request.user, status="pending")
            .order_by("-created_at")
            .first()
        )

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
    """
    Acts like the standard back button:
    - If there's a valid referrer, go there.
    - If not, use the last recorded shop type (events or merch).
    """
    previous_page = request.META.get('HTTP_REFERER')
    basket_url = request.build_absolute_uri(reverse('basket:basket_view'))

    # Default fallback URLs
    merch_url = reverse('products:merch_list')
    events_url = reverse('products:events')

    # Step 1: Use the referrer if it's valid
    if previous_page and previous_page != basket_url:
        return HttpResponseRedirect(previous_page)

    # Step 2: Try the session
    last_shop_type = request.session.get('last_shop_type')
    if last_shop_type == 'events':
        return HttpResponseRedirect(events_url)
    elif last_shop_type == 'merch':
        return HttpResponseRedirect(merch_url)

    # Step 3: Session missing — inspect basket contents
    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
        if basket.items.filter(event__isnull=False).exists():
            return HttpResponseRedirect(events_url)
        elif basket.items.filter(merch__isnull=False).exists():
            return HttpResponseRedirect(merch_url)

    # Step 4: Fallback
    return HttpResponseRedirect(merch_url)
