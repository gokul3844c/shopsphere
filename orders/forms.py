from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "recipient_name",
            "phone",
            "street",
            "landmark",
            "city",
            "state",
            "postal_code",
            "address_type",
            "is_default",
        ]
        widgets = {
            "recipient_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "10-digit mobile number"}),
            "street": forms.TextInput(attrs={"class": "form-control", "placeholder": "Flat, House no., Building, Apartment, Street"}),
            "landmark": forms.TextInput(attrs={"class": "form-control", "placeholder": "Landmark (e.g. Near Metro Station)"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Town / City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "6-digit PIN code"}),
            "address_type": forms.Select(attrs={"class": "form-control"}),
            "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_postal_code(self):
        code = self.cleaned_data.get("postal_code", "").strip()
        if not code.isdigit() or len(code) not in [6, 7]:
            raise forms.ValidationError("Please enter a valid 6-digit postal PIN code.")
        return code

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        cleaned = "".join(filter(str.isdigit, phone))
        if len(cleaned) < 10:
            raise forms.ValidationError("Please enter a valid 10-digit mobile number.")
        return phone
