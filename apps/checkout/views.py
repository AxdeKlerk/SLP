from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from apps.basket.models import Basket, BasketItem
from apps.checkout.models import Order, OrderItem

def checkout_view(request):
    # Get this user's basket
    basket = Basket.objects.filter(user=request.user).first()
    basket_items = basket.items.all() if basket else []

    # Track which events we've validated
    checked_events = set()

    for item in basket_items:
        if item.event and item.event not in checked_events:
            checked_events.add(item.event)

            sold = item.event.tickets_sold
            capacity = item.event.effective_capacity
            remaining = capacity - sold

            # How many tickets are being requested in this basket for this event
            requested_quantity = sum(i.quantity for i in basket_items if i.event == item.event)

            print(
                f"DEBUG: event={item.event}, sold={sold}, capacity={capacity}, remaining={remaining}, requested={requested_quantity}"
            )

            # If too many tickets requested
            if requested_quantity > remaining:
                ticket_word = "ticket" if remaining == 1 else "tickets"
                messages.error(
                    request,
                    f"Not enough tickets available!"
                    f"Only {remaining} {ticket_word} left for {item.event}!"
                )
                return redirect("basket:basket_view")

    #If we reach here, all ticket checks passed
    if request.method == "POST":
        subtotal = 0

        # 1. Create the order
        order = Order.objects.create(
            email=request.POST.get("email"),
            subtotal=0,
            total=0,
        )

        # 2. Add items
        for item in basket_items:
            line_total = item.line_total
            subtotal += line_total

            OrderItem.objects.create(
                order=order,
                event=item.event if item.event else None,
                merch=item.merch if item.merch else None,
                quantity=item.quantity,
                price=(line_total / item.quantity) if item.quantity else 0,
            )

        # 3. Update totals
        order.subtotal = subtotal
        order.total = subtotal
        order.save()

        # 4. Clear basket
        basket_items.delete()

        # 5. Redirect to confirmation
        return redirect("checkout:confirmation", order_id=order.id)

    return render(request, "checkout/checkout.html", {"basket_items": basket_items})


def confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "checkout/confirmation.html", {"order": order})

