from decimal import Decimal
from django.conf import settings
from django.db import models
from catalog.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="carts")
    session_key = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        owner = self.user.username if self.user else f"Session {self.session_key}"
        return f"Cart ({owner})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.select_related("product"))

    @property
    def delivery_fee(self):
        if self.subtotal == Decimal("0.00") or self.subtotal >= Decimal("499.00"):
            return Decimal("0.00")
        return Decimal("49.00")

    @property
    def grand_total(self):
        return self.subtotal + self.delivery_fee

    def add_item(self, product, quantity=1):
        quantity = int(quantity)
        if quantity <= 0:
            return None
        item, created = self.items.get_or_create(product=product, defaults={"quantity": 0})
        new_quantity = item.quantity + quantity
        item.quantity = min(new_quantity, product.stock if product.stock > 0 else 1)
        item.save()
        return item

    def update_item(self, product, quantity):
        quantity = int(quantity)
        if quantity <= 0:
            self.items.filter(product=product).delete()
            return None
        try:
            item = self.items.get(product=product)
            item.quantity = min(quantity, product.stock if product.stock > 0 else 1)
            item.save()
            return item
        except CartItem.DoesNotExist:
            return None

    def remove_item(self, product):
        self.items.filter(product=product).delete()

    def clear(self):
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product")
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def line_total(self):
        return self.product.price * Decimal(str(self.quantity))
