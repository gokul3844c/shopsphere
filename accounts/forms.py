from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile

class EmailOrUsernameLoginForm(forms.Form):
    username = forms.CharField(
        label="Email or mobile phone number / username",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Email or username",
            "autocomplete": "username",
            "autofocus": True,
            "id": "id_username"
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter password",
            "autocomplete": "current-password",
            "id": "id_password"
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={"id": "remember_me"})
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get("username", "").strip()
        password = cleaned_data.get("password")

        if username_or_email and password:
            # Check if username_or_email is an email
            user = None
            if "@" in username_or_email:
                user_match = User.objects.filter(email__iexact=username_or_email).first()
                if user_match:
                    user = authenticate(username=user_match.username, password=password)
            if not user:
                user = authenticate(username=username_or_email, password=password)

            if not user:
                raise forms.ValidationError("Invalid username/email or password. Please try again.")
            if not user.is_active:
                raise forms.ValidationError("This account has been deactivated.")
            self.user_cache = user
        return cleaned_data

    def get_user(self):
        return getattr(self, "user_cache", None)

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Your name",
        widget=forms.TextInput(attrs={"placeholder": "First and last name", "class": "form-control"})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Enter email address", "class": "form-control"})
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        label="Mobile number (optional)",
        widget=forms.TextInput(attrs={"placeholder": "e.g. 9876543210", "class": "form-control"})
    )
    password = forms.CharField(
        min_length=6,
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "At least 6 characters", "class": "form-control", "id": "id_reg_password"})
    )
    confirm_password = forms.CharField(
        required=True,
        label="Re-enter password",
        widget=forms.PasswordInput(attrs={"placeholder": "Re-enter password", "class": "form-control", "id": "id_confirm_password"})
    )

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "phone", "password", "confirm_password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["username"].help_text = "Choose a unique username"
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "e.g. rahul_sharma"})

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.first_name = self.cleaned_data.get("first_name", "")
        if commit:
            user.save()
            phone = self.cleaned_data.get("phone", "")
            if hasattr(user, "profile"):
                user.profile.phone = phone
                user.profile.save()
            else:
                UserProfile.objects.create(user=user, phone=phone)
        return user

class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email Address")
    phone = forms.CharField(max_length=20, required=False, label="Phone Number")

    class Meta:
        model = User
        fields = ("first_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "profile"):
            self.fields["phone"].initial = self.instance.profile.phone

    def save(self, commit=True):
        user = super().save(commit=commit)
        phone = self.cleaned_data.get("phone", "")
        if hasattr(user, "profile"):
            user.profile.phone = phone
            if commit:
                user.profile.save()
        return user
