import uuid
from decimal import Decimal
from django.conf import settings
from django.db import models
from catalog.models import Product

class Address(models.Model):
    class AddressType(models.TextChoices):
        HOME = "home", "Home (7 AM - 9 PM delivery)"
        WORK = "work", "Office/Commercial (9 AM - 6 PM delivery)"
        OTHER = "other", "Other"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    recipient_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    landmark = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=12)
    address_type = models.CharField(max_length=20, choices=AddressType.choices, default=AddressType.HOME)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_default", "-created_at"]
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.recipient_name} - {self.street}, {self.city} ({self.postal_code})"

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    @property
    def formatted(self):
        parts = [self.street]
        if self.landmark:
            parts.append(f"Near {self.landmark}")
        parts.append(f"{self.city}, {self.state} - {self.postal_code}")
        parts.append(f"Phone: {self.phone}")
        return ", ".join(parts)

class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = "placed", "Order Placed"
        CONFIRMED = "confirmed", "Confirmed"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentMethod(models.TextChoices):
        COD = "cod", "Cash on Delivery (Pay upon delivery)"
        CARD = "card", "Credit / Debit Card (Simulated)"
        UPI = "upi", "UPI / QR Code (Simulated)"
        NETBANKING = "netbanking", "Net Banking (Simulated)"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Paid / Completed"
        FAILED = "failed", "Payment Failed"
        REFUNDED = "refunded", "Refunded"

    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    recipient_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    delivery_address = models.TextField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{str(self.order_number)[:8].upper()}"

    @property
    def short_order_number(self):
        return f"OD-{str(self.order_number)[:8].upper()}"

    @property
    def can_cancel(self):
        return self.status in [self.Status.PLACED, self.Status.CONFIRMED]

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    @property
    def line_total(self):
        return self.unit_price * Decimal(str(self.quantity))

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_method = models.CharField(max_length=30)
    transaction_id = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default="completed")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.short_order_number} ({self.status})"
