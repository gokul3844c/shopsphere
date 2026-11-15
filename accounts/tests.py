from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile
from orders.models import Address

class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="priya_sharma",
            email="priya@example.com",
            password="StrongPassword123",
            first_name="Priya"
        )

    def test_user_profile_signal_creation(self):
        self.assertTrue(hasattr(self.user, "profile"))
        self.assertEqual(UserProfile.objects.filter(user=self.user).count(), 1)

    def test_unauthenticated_redirect(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_login_with_username(self):
        response = self.client.post(reverse("login"), {
            "username": "priya_sharma",
            "password": "StrongPassword123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_login_with_email(self):
        response = self.client.post(reverse("login"), {
            "username": "priya@example.com",
            "password": "StrongPassword123"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_registration_flow(self):
        response = self.client.post(reverse("register"), {
            "first_name": "Rohan Verma",
            "username": "rohan_verma",
            "email": "rohan@example.com",
            "phone": "9876543210",
            "password": "Password123!",
            "confirm_password": "Password123!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        user = User.objects.get(username="rohan_verma")
        self.assertEqual(user.first_name, "Rohan Verma")
        self.assertEqual(user.profile.phone, "9876543210")

    def test_logout_flow(self):
        self.client.login(username="priya_sharma", password="StrongPassword123")
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_address_management(self):
        self.client.login(username="priya_sharma", password="StrongPassword123")
        response = self.client.post(reverse("address_create"), {
            "recipient_name": "Priya Sharma",
            "phone": "9876543210",
            "street": "101 Lotus Enclave, MG Road",
            "landmark": "Near Metro",
            "city": "Bengaluru",
            "state": "Karnataka",
            "postal_code": "560001",
            "address_type": "home",
            "is_default": "on"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Address.objects.filter(user=self.user).count(), 1)
        addr = Address.objects.get(user=self.user)
        self.assertTrue(addr.is_default)
