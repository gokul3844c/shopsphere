import uuid
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta

from cart.models import Cart
from catalog.models import Product
from .models import Address, Order, OrderItem, Payment
from .forms import AddressForm

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product").all()

    if not items.exists():
        messages.info(request, "Your cart is empty. Add items before checking out.")
        return redirect("product_list")

    # Verify initial stock
    for item in items:
        if item.quantity > item.product.stock:
            messages.error(request, f"Insufficient stock for {item.product.name} (Available: {item.product.stock}). Please adjust your cart.")
            return redirect("cart_detail")

    user_addresses = Address.objects.filter(user=request.user)
    default_address = user_addresses.filter(is_default=True).first() or user_addresses.first()
    subtotal = cart.subtotal
    delivery_fee = cart.delivery_fee
    grand_total = cart.grand_total

    new_address_form = AddressForm()

    if request.method == "POST":
        address_id = request.POST.get("address_id")
        payment_method = request.POST.get("payment_method", Order.PaymentMethod.COD)
        delivery_address_text = ""
        recipient_name = ""
        phone = ""

        # Check if user picked existing address or filled new one
        if address_id and address_id != "new":
            addr = get_object_or_404(Address, pk=address_id, user=request.user)
            recipient_name = addr.recipient_name
            phone = addr.phone
            delivery_address_text = addr.formatted
        else:
            new_address_form = AddressForm(request.POST)
            if new_address_form.is_valid():
                addr = new_address_form.save(commit=False)
                addr.user = request.user
                if not user_addresses.exists():
                    addr.is_default = True
                addr.save()
                recipient_name = addr.recipient_name
                phone = addr.phone
                delivery_address_text = addr.formatted
            else:
                messages.error(request, "Please fill in all required delivery address fields correctly.")
                return render(request, "orders/checkout.html", {
                    "cart": cart,
                    "items": items,
                    "user_addresses": user_addresses,
                    "default_address": default_address,
                    "subtotal": subtotal,
                    "delivery_fee": delivery_fee,
                    "grand_total": grand_total,
                    "new_address_form": new_address_form,
                })

        # Process order atomically under database row locks
        try:
            with transaction.atomic():
                locked_products = []
                for item in items:
                    p = Product.objects.select_for_update().get(pk=item.product.pk)
                    if p.stock < item.quantity:
                        messages.error(request, f"Sorry, {p.name} just went out of stock. Available: {p.stock}.")
                        return redirect("cart_detail")
                    locked_products.append((p, item.quantity))

                # Determine initial payment status
                payment_status = Order.PaymentStatus.PENDING
                if payment_method in [Order.PaymentMethod.CARD, Order.PaymentMethod.UPI, Order.PaymentMethod.NETBANKING]:
                    payment_status = Order.PaymentStatus.COMPLETED

                # Create Order
                order = Order.objects.create(
                    user=request.user,
                    recipient_name=recipient_name,
                    phone=phone,
                    delivery_address=delivery_address_text,
                    subtotal=subtotal,
                    delivery_fee=delivery_fee,
                    total=grand_total,
                    status=Order.Status.PLACED,
                    payment_method=payment_method,
                    payment_status=payment_status,
                )

                # Create OrderItems and deduct stock
                for p, qty in locked_products:
                    OrderItem.objects.create(
                        order=order,
                        product=p,
                        product_name=p.name,
                        unit_price=p.price,
                        quantity=qty,
                    )
                    p.stock -= qty
                    p.save(update_fields=["stock"])

                # Create Payment record
                txn_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
                Payment.objects.create(
                    order=order,
                    payment_method=payment_method,
                    transaction_id=txn_id,
                    amount=grand_total,
                    status="completed" if payment_status == Order.PaymentStatus.COMPLETED else "pending"
                )

                # Clear Cart
                cart.clear()

            messages.success(request, f"Order placed successfully! Order #{order.short_order_number}")
            return redirect("order_confirmation", order_number=order.order_number)

        except Exception as e:
            messages.error(request, f"An error occurred while placing your order: {str(e)}")
            return redirect("cart_detail")

    return render(request, "orders/checkout.html", {
        "cart": cart,
        "items": items,
        "user_addresses": user_addresses,
        "default_address": default_address,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "grand_total": grand_total,
        "new_address_form": new_address_form,
    })

@login_required
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    estimated_delivery = order.created_at + timedelta(days=2)
    return render(request, "orders/confirmation.html", {
        "order": order,
        "items": order.items.select_related("product").all(),
        "estimated_delivery": estimated_delivery,
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items", "items__product").order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})

@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    estimated_delivery = order.created_at + timedelta(days=2)
    return render(request, "orders/order_detail.html", {
        "order": order,
        "items": order.items.select_related("product").all(),
        "estimated_delivery": estimated_delivery,
    })

@login_required
def cancel_order(request, order_number):
    if request.method != "POST":
        return redirect("order_history")

    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if not order.can_cancel:
        messages.error(request, "This order cannot be cancelled because it has already been shipped or processed.")
        return redirect("order_detail", order_number=order.order_number)

    with transaction.atomic():
        # Restore inventory
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save(update_fields=["stock"])

        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])

        if hasattr(order, "payment") and order.payment.status == "completed":
            order.payment.status = "refunded"
            order.payment.save(update_fields=["status"])
            order.payment_status = Order.PaymentStatus.REFUNDED
            order.save(update_fields=["payment_status"])

    messages.success(request, f"Order #{order.short_order_number} has been cancelled. Inventory has been restored.")
    return redirect("order_detail", order_number=order.order_number)
