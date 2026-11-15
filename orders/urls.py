from django.urls import path
from .views import checkout, order_confirmation, order_history, order_detail, cancel_order

urlpatterns = [
    path("checkout/", checkout, name="checkout"),
    path("history/", order_history, name="order_history"),
    path("confirmation/<uuid:order_number>/", order_confirmation, name="order_confirmation"),
    path("detail/<uuid:order_number>/", order_detail, name="order_detail"),
    path("cancel/<uuid:order_number>/", cancel_order, name="cancel_order"),
]
