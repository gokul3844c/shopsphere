from django.contrib import admin
from .models import Category, Product, ProductImage, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ("user", "rating", "created_at")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "brand", "price", "original_price", "stock", "rating", "is_featured", "is_active")
    list_filter = ("category", "is_featured", "is_active", "brand")
    search_fields = ("name", "sku", "brand", "description")
    list_editable = ("price", "stock", "is_featured", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "title", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__username", "title", "comment")
