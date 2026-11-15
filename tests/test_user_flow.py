from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category, Product
from orders.models import Order

class UserJourneyFlowTest(TestCase):
    """
    End-to-end user flow test:
    Success criteria: A new user can register, log in, browse products with images,
    search and filter the catalogue, add products to the cart, check out, place an order,
    and view their own order history.
    """
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Wireless Noise-Cancelling Headphones",
            slug="wireless-noise-cancelling-headphones",
            sku="SP-ELE-0001",
            brand="SoundPeak",
            description="Ultra-comfortable Bluetooth over-ear headphones.",
            price=Decimal("4999.00"),
            original_price=Decimal("7999.00"),
            stock=20,
            rating=Decimal("4.6"),
            review_count=15,
            is_featured=True,
            is_active=True
        )

    def test_complete_user_journey(self):
        # 1. Unauthenticated user visits site -> redirected to login
        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 302)
        self.assertIn(reverse("login"), res.url)

        # 2. User registers for a new account
        reg_res = self.client.post(reverse("register"), {
            "first_name": "Aarav Patel",
            "username": "aarav_patel",
            "email": "aarav@example.com",
            "phone": "9876543210",
            "password": "SecurePassword123!",
            "confirm_password": "SecurePassword123!"
        })
        self.assertEqual(reg_res.status_code, 302)
        self.assertRedirects(reg_res, reverse("login"))

        # 3. User logs in with email or username
        login_res = self.client.post(reverse("login"), {
            "username": "aarav@example.com",
            "password": "SecurePassword123!",
            "remember_me": "on"
        })
        self.assertEqual(login_res.status_code, 302)
        self.assertRedirects(login_res, reverse("home"))

        # 4. User views homepage
        home_res = self.client.get(reverse("home"))
        self.assertEqual(home_res.status_code, 200)
        self.assertContains(home_res, "ShopSphere")
        self.assertContains(home_res, "Wireless Noise-Cancelling Headphones")

        # 5. User searches the catalogue
        search_res = self.client.get(reverse("product_list") + "?q=Noise-Cancelling")
        self.assertEqual(search_res.status_code, 200)
        self.assertContains(search_res, "Wireless Noise-Cancelling Headphones")

        # 6. User views product details
        detail_res = self.client.get(self.product.get_absolute_url())
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, "In Stock")
        self.assertContains(detail_res, "SoundPeak")

        # 7. User adds product to cart
        add_cart_res = self.client.post(
            reverse("add_to_cart", args=[self.product.pk]),
            {"quantity": 2}
        )
        self.assertEqual(add_cart_res.status_code, 302)

        # 8. User views cart
        cart_res = self.client.get(reverse("cart_detail"))
        self.assertEqual(cart_res.status_code, 200)
        self.assertContains(cart_res, "9998.00")

        # 9. User proceeds to checkout and places order
        checkout_res = self.client.post(reverse("checkout"), {
            "recipient_name": "Aarav Patel",
            "phone": "9876543210",
            "street": "Flat 304, Green Heights",
            "landmark": "Near IT Park",
            "city": "Pune",
            "state": "Maharashtra",
            "postal_code": "411001",
            "address_type": "home",
            "payment_method": "cod"
        })
        self.assertEqual(checkout_res.status_code, 302)

        # 10. Verify order created and inventory deducted
        order = Order.objects.filter(user__username="aarav_patel").first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().quantity, 2)
        self.assertEqual(order.total, Decimal("9998.00"))

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 18)

        # 11. User views confirmation page
        conf_res = self.client.get(reverse("order_confirmation", args=[order.order_number]))
        self.assertEqual(conf_res.status_code, 200)
        self.assertContains(conf_res, "Order placed, thank you!")
        self.assertContains(conf_res, order.short_order_number)

        # 12. User views order history
        history_res = self.client.get(reverse("order_history"))
        self.assertEqual(history_res.status_code, 200)
        self.assertContains(history_res, order.short_order_number)

        # 13. User views specific order details
        order_detail_res = self.client.get(reverse("order_detail", args=[order.order_number]))
        self.assertEqual(order_detail_res.status_code, 200)
        self.assertContains(order_detail_res, "Shipment Status:")
