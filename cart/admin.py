from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("product", "quantity", "line_total", "added_at")

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "session_key", "total_items", "subtotal", "updated_at")
    inlines = [CartItemInline]
