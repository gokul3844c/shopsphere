from django.urls import path
from .views import (
    ShopLoginView,
    shop_logout,
    register,
    account_dashboard,
    address_list,
    address_create,
    address_edit,
    address_delete,
    address_set_default,
    ShopPasswordResetView,
    ShopPasswordResetDoneView,
    ShopPasswordResetConfirmView,
    ShopPasswordResetCompleteView,
)

urlpatterns = [
    path("login/", ShopLoginView.as_view(), name="login"),
    path("logout/", shop_logout, name="logout"),
    path("register/", register, name="register"),
    path("dashboard/", account_dashboard, name="account_dashboard"),
    path("addresses/", address_list, name="address_list"),
    path("addresses/add/", address_create, name="address_create"),
    path("addresses/<int:pk>/edit/", address_edit, name="address_edit"),
    path("addresses/<int:pk>/delete/", address_delete, name="address_delete"),
    path("addresses/<int:pk>/set-default/", address_set_default, name="address_set_default"),
    
    # Password Reset
    path("password-reset/", ShopPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", ShopPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", ShopPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password-reset-complete/", ShopPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
