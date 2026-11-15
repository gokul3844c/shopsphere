from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import EmailOrUsernameLoginForm, RegistrationForm, UserProfileUpdateForm
from orders.models import Address, Order
from orders.forms import AddressForm

class ShopLoginView(FormView):
    template_name = "accounts/login.html"
    form_class = EmailOrUsernameLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if form.cleaned_data.get("remember_me"):
            # 2 weeks
            self.request.session.set_expiry(1209600)
        else:
            # Browser close
            self.request.session.set_expiry(0)

        # Merge session cart into database cart if any
        session_cart = self.request.session.get("cart", {})
        if session_cart:
            from cart.models import Cart
            from catalog.models import Product
            cart_obj, _ = Cart.objects.get_or_create(user=user)
            for pid, qty in session_cart.items():
                try:
                    product = Product.objects.get(pk=int(pid), is_active=True)
                    cart_obj.add_item(product, qty)
                except Exception:
                    pass

        messages.success(self.request, f"Welcome back, {user.first_name or user.username}!")
        next_url = self.request.GET.get("next") or self.request.POST.get("next") or "home"
        return redirect(next_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["next"] = self.request.GET.get("next", "")
        return ctx

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, "Account created successfully! Please sign in with your credentials.")
        return redirect("login")
    return render(request, "accounts/register.html", {"form": form})

def shop_logout(request):
    logout(request)
    messages.info(request, "You have been logged out securely.")
    return redirect("login")

@login_required
def account_dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]
    addresses = Address.objects.filter(user=request.user)
    profile_form = UserProfileUpdateForm(instance=request.user)

    if request.method == "POST":
        profile_form = UserProfileUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile details have been updated.")
            return redirect("account_dashboard")

    return render(request, "accounts/dashboard.html", {
        "orders": orders,
        "addresses": addresses,
        "profile_form": profile_form,
    })

@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "accounts/address_list.html", {"addresses": addresses})

@login_required
def address_create(request):
    form = AddressForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        # If this is the only address, make it default
        if not Address.objects.filter(user=request.user).exists():
            address.is_default = True
        address.save()
        messages.success(request, "New delivery address added.")
        next_url = request.GET.get("next") or "address_list"
        return redirect(next_url)
    return render(request, "accounts/address_form.html", {"form": form, "action": "Add New"})

@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    form = AddressForm(request.POST or None, instance=address)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Address updated successfully.")
        return redirect("address_list")
    return render(request, "accounts/address_form.html", {"form": form, "action": "Edit", "address": address})

@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == "POST":
        address.delete()
        messages.success(request, "Address removed.")
    return redirect("address_list")

@login_required
def address_set_default(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == "POST":
        address.is_default = True
        address.save()
        messages.success(request, "Default delivery address updated.")
    return redirect("address_list")

# Password Reset Views with custom Amazon-like templates
class ShopPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")

class ShopPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"

class ShopPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")

class ShopPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
