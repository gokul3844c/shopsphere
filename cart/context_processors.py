from .models import Cart

def cart_context(request):
    total_items = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            total_items = cart.total_items
        else:
            # Fallback to session cart count if any
            session_cart = request.session.get("cart", {})
            total_items = sum(int(q) for q in session_cart.values() if str(q).isdigit())
    else:
        session_cart = request.session.get("cart", {})
        total_items = sum(int(q) for q in session_cart.values() if str(q).isdigit())
    return {"cart_item_count": total_items}
