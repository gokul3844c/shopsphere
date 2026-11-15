from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from catalog.models import Product
from .models import Cart, CartItem

def get_or_create_user_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # Merge session cart if exists
        session_cart = request.session.get("cart", {})
        if session_cart:
            for pid, qty in list(session_cart.items()):
                try:
                    product = Product.objects.get(pk=int(pid), is_active=True)
                    cart.add_item(product, qty)
                except Exception:
                    pass
            request.session["cart"] = {}
        return cart
    else:
        # Session based cart
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart

@login_required
def cart_detail(request):
    cart = get_or_create_user_cart(request)
    items = cart.items.select_related("product", "product__category").all()
    subtotal = cart.subtotal
    delivery_fee = cart.delivery_fee
    grand_total = cart.grand_total

    # Calculate total savings compared to original MRP
    total_savings = Decimal("0.00")
    for item in items:
        if item.product.original_price and item.product.original_price > item.product.price:
            total_savings += (item.product.original_price - item.product.price) * Decimal(str(item.quantity))

    free_delivery_threshold = Decimal("499.00")
    amount_needed_for_free_delivery = Decimal("0.00")
    if subtotal > 0 and subtotal < free_delivery_threshold:
        amount_needed_for_free_delivery = free_delivery_threshold - subtotal

    return render(request, "cart/cart.html", {
        "cart": cart,
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "grand_total": grand_total,
        "total_savings": total_savings,
        "amount_needed_for_free_delivery": amount_needed_for_free_delivery,
    })

@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("product_list")

    product = get_object_or_404(Product, pk=product_id, is_active=True)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    if quantity < 1:
        quantity = 1

    if product.stock <= 0:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "message": "This product is currently out of stock."}, status=400)
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect(product.get_absolute_url())

    cart = get_or_create_user_cart(request)
    current_item = cart.items.filter(product=product).first()
    current_qty = current_item.quantity if current_item else 0
    requested_total = current_qty + quantity

    if requested_total > product.stock:
        # Cap to available stock
        added_qty = max(0, product.stock - current_qty)
        if added_qty > 0:
            cart.add_item(product, added_qty)
            msg = f"Only {product.stock} items in stock. We added {added_qty} to your cart."
            messages.warning(request, msg)
        else:
            msg = f"You already have all {product.stock} available units in your cart."
            messages.info(request, msg)
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "message": msg, "cart_count": cart.total_items})
            return redirect("cart_detail")
    else:
        cart.add_item(product, quantity)
        messages.success(request, f"Added {quantity} x {product.name} to your cart.")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "message": f"Added {product.name} to cart.",
            "cart_count": cart.total_items,
            "subtotal": f"{cart.subtotal:.2f}"
        })

    next_url = request.POST.get("next") or "cart_detail"
    return redirect(next_url)

@login_required
def update_cart_item(request, product_id):
    if request.method != "POST":
        return redirect("cart_detail")

    product = get_object_or_404(Product, pk=product_id)
    cart = get_or_create_user_cart(request)

    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1

    if quantity <= 0:
        cart.remove_item(product)
        messages.info(request, f"Removed {product.name} from your cart.")
    else:
        if quantity > product.stock:
            quantity = product.stock
            messages.warning(request, f"Maximum available quantity is {product.stock}.")
        cart.update_item(product, quantity)
        messages.success(request, f"Updated quantity for {product.name}.")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        item = cart.items.filter(product=product).first()
        line_total = f"{item.line_total:.2f}" if item else "0.00"
        return JsonResponse({
            "success": True,
            "cart_count": cart.total_items,
            "item_quantity": item.quantity if item else 0,
            "line_total": line_total,
            "subtotal": f"{cart.subtotal:.2f}",
            "delivery_fee": f"{cart.delivery_fee:.2f}",
            "grand_total": f"{cart.grand_total:.2f}"
        })

    return redirect("cart_detail")

@login_required
def remove_from_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        cart = get_or_create_user_cart(request)
        cart.remove_item(product)
        messages.info(request, f"Removed {product.name} from your cart.")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "cart_count": cart.total_items,
                "subtotal": f"{cart.subtotal:.2f}",
                "delivery_fee": f"{cart.delivery_fee:.2f}",
                "grand_total": f"{cart.grand_total:.2f}"
            })

    return redirect("cart_detail")

@login_required
def clear_cart(request):
    if request.method == "POST":
        cart = get_or_create_user_cart(request)
        cart.clear()
        messages.info(request, "Your cart has been cleared.")
    return redirect("cart_detail")
