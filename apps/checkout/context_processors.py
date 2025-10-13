from apps.checkout.models import Order

def last_order(request):
    """Make the user's latest pending order available in all templates."""
    if request.user.is_authenticated:
        order = (
            Order.objects.filter(user=request.user, status="pending")
            .order_by("-created_at")
            .first()
        )
    else:
        order = None

    return {"last_order": order}
