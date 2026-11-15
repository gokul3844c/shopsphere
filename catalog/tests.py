from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from catalog.models import Category, Product, Review

class CatalogTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="buyer1",
            email="buyer1@example.com",
            password="Password123"
        )
        self.cat_elec = Category.objects.create(name="Electronics", slug="electronics")
        self.cat_books = Category.objects.create(name="Books", slug="books")

        self.p1 = Product.objects.create(
            category=self.cat_elec,
            name="Wireless Noise Cancelling Headphones",
            slug="wireless-noise-cancelling-headphones",
            sku="SP-ELE-0001",
            brand="SoundPeak",
            price=Decimal("4999.00"),
            original_price=Decimal("7999.00"),
            stock=15,
            rating=Decimal("4.5"),
            review_count=10,
            is_featured=True,
            is_active=True
        )
        self.p2 = Product.objects.create(
            category=self.cat_books,
            name="Clean Code Guide",
            slug="clean-code-guide",
            sku="SP-BOO-0002",
            brand="Pearson",
            price=Decimal("899.00"),
            original_price=Decimal("1299.00"),
            stock=5,
            rating=Decimal("4.8"),
            review_count=20,
            is_featured=False,
            is_active=True
        )

    def test_product_properties(self):
        self.assertEqual(self.p1.discount_percentage, 38)
        self.assertEqual(self.p1.savings_amount, Decimal("3000.00"))
        self.assertTrue(self.p1.in_stock)

    def test_search_by_name_and_brand(self):
        self.client.login(username="buyer1", password="Password123")
        res1 = self.client.get(reverse("product_list") + "?q=Headphones")
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, "Wireless Noise Cancelling Headphones")
        self.assertNotContains(res1, "Clean Code Guide")

        res2 = self.client.get(reverse("product_list") + "?q=Pearson")
        self.assertEqual(res2.status_code, 200)
        self.assertContains(res2, "Clean Code Guide")

    def test_filter_by_category(self):
        self.client.login(username="buyer1", password="Password123")
        res = self.client.get(reverse("product_list") + "?category=electronics")
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Wireless Noise Cancelling Headphones")
        self.assertNotContains(res, "Clean Code Guide")

    def test_sort_by_price(self):
        self.client.login(username="buyer1", password="Password123")
        res_low = self.client.get(reverse("product_list") + "?sort=price_low")
        self.assertEqual(res_low.status_code, 200)
        products = list(res_low.context["products"])
        self.assertEqual(products[0], self.p2)

        res_high = self.client.get(reverse("product_list") + "?sort=price_high")
        products_high = list(res_high.context["products"])
        self.assertEqual(products_high[0], self.p1)

    def test_add_customer_review(self):
        self.client.login(username="buyer1", password="Password123")
        res = self.client.post(self.p1.get_absolute_url(), {
            "submit_review": "1",
            "rating": 5,
            "title": "Amazing sound quality",
            "comment": "Bass is deep and ANC is superb."
        })
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Review.objects.filter(product=self.p1).count(), 1)
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.rating, Decimal("5.0"))
