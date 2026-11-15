from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category, Product
from cart.models import Cart, CartItem

class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="cart_user", password="Password123")
        self.client.login(username="cart_user", password="Password123")
        cat = Category.objects.create(name="Tech", slug="tech")
        self.p1 = Product.objects.create(
            category=cat,
            name="USB-C Hub",
            slug="usb-c-hub",
            sku="SKU-HUB-01",
            price=Decimal("1200.00"),
            original_price=Decimal("1500.00"),
            stock=10,
            is_active=True
        )
        self.p2 = Product.objects.create(
            category=cat,
            name="Screen Protector",
            slug="screen-protector",
            sku="SKU-PROT-02",
            price=Decimal("299.00"),
            original_price=Decimal("499.00"),
            stock=2,
            is_active=True
        )

    def test_add_to_cart(self):
        res = self.client.post(reverse("add_to_cart", args=[self.p1.pk]), {"quantity": 2})
        self.assertEqual(res.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.total_items, 2)
        self.assertEqual(cart.subtotal, Decimal("2400.00"))
        # Over ₹499 so delivery fee is 0
        self.assertEqual(cart.delivery_fee, Decimal("0.00"))

    def test_stock_limit_enforcement(self):
        # Product p2 has stock of 2, user requests 5
        res = self.client.post(reverse("add_to_cart", args=[self.p2.pk]), {"quantity": 5})
        cart = Cart.objects.get(user=self.user)
        # Should be capped at available stock (2)
        self.assertEqual(cart.total_items, 2)

    def test_update_and_remove_cart(self):
        cart = Cart.objects.create(user=self.user)
        cart.add_item(self.p1, 2)
        self.assertEqual(cart.total_items, 2)

        # Update to 4
        self.client.post(reverse("update_cart_item", args=[self.p1.pk]), {"quantity": 4})
        cart.refresh_from_db()
        self.assertEqual(cart.total_items, 4)

        # Remove
        self.client.post(reverse("remove_from_cart", args=[self.p1.pk]))
        cart.refresh_from_db()
        self.assertEqual(cart.total_items, 0)
