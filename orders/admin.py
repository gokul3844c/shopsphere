from django.contrib import admin
from .models import Address, Order, OrderItem, Payment

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("recipient_name", "user", "city", "state", "postal_code", "phone", "is_default")
    list_filter = ("state", "address_type", "is_default")
    search_fields = ("recipient_name", "user__username", "city", "phone", "postal_code")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "unit_price", "quantity", "line_total")

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 0
    readonly_fields = ("transaction_id", "amount", "status", "created_at")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("short_order_number", "user", "recipient_name", "total", "status", "payment_method", "payment_status", "created_at")
    list_filter = ("status", "payment_method", "payment_status", "created_at")
    search_fields = ("order_number", "user__username", "recipient_name", "phone", "delivery_address")
    readonly_fields = ("order_number", "created_at", "updated_at")
    inlines = [OrderItemInline, PaymentInline]
    actions = ["mark_as_confirmed", "mark_as_shipped", "mark_as_delivered", "mark_as_cancelled"]

    @admin.action(description="Mark selected orders as Confirmed")
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status=Order.Status.CONFIRMED)

    @admin.action(description="Mark selected orders as Shipped")
    def mark_as_shipped(self, request, queryset):
        queryset.update(status=Order.Status.SHIPPED)

    @admin.action(description="Mark selected orders as Delivered")
    def mark_as_delivered(self, request, queryset):
        queryset.update(status=Order.Status.DELIVERED)

    @admin.action(description="Mark selected orders as Cancelled")
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status=Order.Status.CANCELLED)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "order", "payment_method", "amount", "status", "created_at")
    list_filter = ("status", "payment_method")
    search_fields = ("transaction_id", "order__order_number")
