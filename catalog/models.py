from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "/static/images/placeholder.svg"

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    sku = models.CharField(max_length=50, unique=True)
    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    specifications = models.JSONField(default=dict, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    original_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal("0.0"))
    review_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "-created_at", "name"]

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round((self.original_price - self.price) * Decimal("100") / self.original_price)
        return 0

    @property
    def savings_amount(self):
        if self.original_price and self.original_price > self.price:
            return self.original_price - self.price
        return Decimal("0.00")

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        first_img = self.images.first()
        if first_img:
            return first_img.display_image
        return "/static/images/placeholder.svg"

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def update_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg = reviews.aggregate(models.Avg("rating"))["rating__avg"]
            self.rating = Decimal(str(round(avg, 1)))
            self.review_count = reviews.count()
        else:
            self.rating = Decimal("0.0")
            self.review_count = 0
        self.save(update_fields=["rating", "review_count"])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    image_url = models.URLField(blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"Image for {self.product.name} (#{self.display_order})"

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "/static/images/placeholder.svg"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=150, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name} ({self.rating}★)"
