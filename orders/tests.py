from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category, Product
from cart.models import Cart
from orders.models import Address, Order, OrderItem, Payment

class OrdersTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="order_user", email="user@order.com", password="Password123")
        self.other_user = User.objects.create_user(username="other_user", email="other@order.com", password="Password123")
        
        cat = Category.objects.create(name="Gadgets", slug="gadgets")
        self.product = Product.objects.create(
            category=cat,
            name="Wireless Mouse",
            slug="wireless-mouse",
            sku="SKU-WM-01",
            price=Decimal("500.00"),
            original_price=Decimal("800.00"),
            stock=10,
            is_active=True
        )

        self.address = Address.objects.create(
            user=self.user,
            recipient_name="Order User",
            phone="9876543210",
            street="Flat 402, Skyline Towers",
            city="Mumbai",
            state="Maharashtra",
            postal_code="400001",
            is_default=True
        )

    def test_checkout_and_inventory_deduction(self):
        self.client.login(username="order_user", password="Password123")
        cart = Cart.objects.create(user=self.user)
        cart.add_item(self.product, 3)

        initial_stock = self.product.stock

        response = self.client.post(reverse("checkout"), {
            "address_id": self.address.pk,
            "payment_method": "cod"
        })
        self.assertEqual(response.status_code, 302)
        
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().quantity, 3)
        self.assertEqual(order.payment_method, "cod")
        
        # Verify inventory was deducted atomically
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, initial_stock - 3)

        # Verify cart was cleared
        cart.refresh_from_db()
        self.assertEqual(cart.total_items, 0)

    def test_order_access_restriction(self):
        # Create an order for self.user
        order = Order.objects.create(
            user=self.user,
            recipient_name="Order User",
            delivery_address="Address text",
            subtotal=Decimal("500.00"),
            delivery_fee=Decimal("0.00"),
            total=Decimal("500.00"),
            status=Order.Status.PLACED
        )

        # Log in as other_user and attempt to view order detail
        self.client.login(username="other_user", password="Password123")
        response = self.client.get(reverse("order_detail", args=[order.order_number]))
        self.assertEqual(response.status_code, 404)

        # Log in as owning user
        self.client.login(username="order_user", password="Password123")
        response2 = self.client.get(reverse("order_detail", args=[order.order_number]))
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, order.short_order_number)

    def test_order_cancellation_restores_inventory(self):
        self.client.login(username="order_user", password="Password123")
        cart = Cart.objects.create(user=self.user)
        cart.add_item(self.product, 2)
        self.client.post(reverse("checkout"), {"address_id": self.address.pk, "payment_method": "cod"})

        self.product.refresh_from_db()
        stock_after_order = self.product.stock
        order = Order.objects.filter(user=self.user).first()

        # Cancel the order
        cancel_res = self.client.post(reverse("cancel_order", args=[order.order_number]))
        self.assertEqual(cancel_res.status_code, 302)

        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.CANCELLED)

        # Verify stock was restored
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, stock_after_order + 2)
