from django.shortcuts import render, redirect, get_object_or_404
from apps.basket.models import Basket, BasketItem
from apps.products.models import Event, Merch
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def basket_view(request):
     # Clear any old Django messages from previous sessions
    storage = messages.get_messages(request)
    list(storage)
    
    basket = None
    subtotal = 0

    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
        subtotal = sum(item.line_total for item in basket.items.all())

    return render(request, 'basket/basket.html', {
        'basket': basket,
        'subtotal': subtotal,
        'quantity_options': range(1, 11),
        'page_title': "Basket",
    })


def add_event_to_basket(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')

    basket, created = Basket.objects.get_or_create(user=request.user)
    event = get_object_or_404(Event, id=event_id)

    item, created = BasketItem.objects.get_or_create(basket=basket, event=event)
    if not created:
        item.quantity = min(item.quantity + 1, 9)
        item.save()

    return redirect('basket:basket_view')


def add_merch_to_basket(request, merch_id):
    if not request.user.is_authenticated:
        return redirect('login')

    basket, created = Basket.objects.get_or_create(user=request.user)
    merch = get_object_or_404(Merch, id=merch_id)

    quantity = int(request.POST.get("quantity", 1))
    if quantity < 1: quantity = 1
    elif quantity > 9: quantity = 9

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
        elif quantity > 9:
            quantity = 9

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
