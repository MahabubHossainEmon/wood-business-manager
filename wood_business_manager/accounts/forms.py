from django import forms
from .models import Customer, Sale, Payment, WoodType

class StyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class CustomerForm(StyledForm):
    class Meta:
        model = Customer
        fields = ["name", "phone", "address", "notes"]

class SaleForm(StyledForm):
    class Meta:
        model = Sale
        fields = ["customer", "wood_type", "quantity", "unit", "total_amount", "date", "details"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

class PaymentForm(StyledForm):
    class Meta:
        model = Payment
        fields = ["customer", "amount", "date", "method", "note"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

class WoodTypeForm(StyledForm):
    class Meta:
        model = WoodType
        fields = ["name", "unit", "quantity", "purchase_rate"]
