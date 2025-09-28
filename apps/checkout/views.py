from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.basket.models import Basket
from apps.checkout.models import Order, OrderItem

@login_required
def basket_checkout(request):
    # Get this user's basket
    basket = Basket.objects.filter(user=request.user).first()
    basket_items = basket.items.all() if basket else []

    # Validate ticket capacities
    checked_events = set()
    for item in basket_items:
        if item.event and item.event not in checked_events:
            checked_events.add(item.event)

            sold = item.event.tickets_sold
            capacity = item.event.effective_capacity
            remaining = capacity - sold
            requested_quantity = sum(i.quantity for i in basket_items if i.event == item.event)

            if requested_quantity > remaining:
                ticket_word = "ticket" if remaining == 1 else "tickets"
                messages.error(
                    request,
                    f"Not enough tickets available! Only {remaining} {ticket_word} left for {item.event}!"
                )
                return redirect("basket:basket_view")

    if not basket_items:
        messages.error(request, "Your basket is empty.")
        return redirect("basket:basket_view")

    # Create the pending order
    order = Order.objects.create(
        user=request.user,
        email=getattr(request.user, "email", None),
        status="pending",
        subtotal=0,
        total=0,
    )

    subtotal = 0
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

    # Update totals
    order.subtotal = subtotal
    order.total = subtotal
    order.save()

    # Clear basket
    basket.items.all().delete()

    # Redirect to checkout page
    return redirect("checkout:checkout_view", order_id=order.id)


def confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "checkout/confirmation.html", {"order": order})


@login_required
def checkout_view(request, order_id):
    # Find the order for this user
    order = get_object_or_404(Order, id=order_id, user=request.user, status="pending")
    return render(request, "checkout/checkout.html", {"order": order})
