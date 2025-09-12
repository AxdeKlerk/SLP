from django.shortcuts import render, redirect, get_object_or_404
from apps.basket.models import Basket, BasketItem
from apps.products.models import Event, Merch

def basket_view(request):
    basket = None
    subtotal = 0

    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
    
        # Calculate subtotal
        for item in basket.items.all():
            subtotal = sum(item.line_total for item in basket.items.all())

    return render(request, 'basket/basket.html', {
        'basket': basket,
        'subtotal': subtotal,
    })

def add_event_to_basket(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')  # force login before adding

    basket, created = Basket.objects.get_or_create(user=request.user)
    event = get_object_or_404(Event, id=event_id)

    # Look for an existing BasketItem with this event
    item, created = BasketItem.objects.get_or_create(
        basket=basket,
        event=event,
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('basket:basket_view')

def add_merch_to_basket(request, merch_id):
    if not request.user.is_authenticated:
        return redirect('login')  # force login before adding

    basket, created = Basket.objects.get_or_create(user=request.user)
    merch = get_object_or_404(Merch, id=merch_id)

    # Look for an existing BasketItem with this merch
    item, created = BasketItem.objects.get_or_create(
        basket=basket,
        merch=merch,
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('basket:basket_view')

def update_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(BasketItem, id=item_id)
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()  # safety – if they pick 0
    return redirect("basket:basket_view")

def delete_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(BasketItem, id=item_id)
        item.delete()
    return redirect("basket:basket_view")


