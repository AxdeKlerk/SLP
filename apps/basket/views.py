from django.shortcuts import render, redirect, get_object_or_404
from apps.basket.models import Basket, BasketItem
from apps.products.models import Event

def basket_view(request):
    basket = None
    if request.user.is_authenticated:
        basket, created = Basket.objects.get_or_create(user=request.user)
    return render(request, 'basket/basket.html', {'basket': basket})

def add_to_basket(request, event_id):
    if not request.user.is_authenticated:
        return redirect('login')  # force login before adding

    basket, created = Basket.objects.get_or_create(user=request.user)
    event = get_object_or_404(Event, id=event_id)

    # Look for an existing BasketItem
    item, created = BasketItem.objects.get_or_create(
        basket=basket,
        event=event,
    )
    if not created:
        item.quantity += 1
        item.save()

    return redirect('basket:basket_view')
