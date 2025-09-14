from django.shortcuts import render, redirect, get_object_or_404
from apps.basket.models import BasketItem
from .models import Order, OrderItem

def checkout_view(request):
    # Get all basket items (for now, no user filter)
    basket_items = BasketItem.objects.all()

    if request.method == "POST":
        # 1. Create the order
        order = Order.objects.create(
            email=request.POST.get("email"),  # keep it simple first
            subtotal=0,
            total=0,
        )

        subtotal = 0

        # 2. Add items
        for item in basket_items:
            line_total = item.quantity * item.price
            subtotal += line_total

            OrderItem.objects.create(
                order=order,
                product_name=str(item),  # str() picks up basket item __str__
                quantity=item.quantity,
                price=item.price,
            )

        # 3. Update totals
        order.subtotal = subtotal
        order.total = subtotal  # add shipping/vat later
        order.save()

        # 4. Clear basket
        basket_items.delete()

        # 5. Redirect to confirmation
        return redirect("checkout:confirmation", order_id=order.id)

    return render(request, "checkout/checkout.html", {"basket_items": basket_items})

def confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "checkout/confirmation.html", {"order": order})


