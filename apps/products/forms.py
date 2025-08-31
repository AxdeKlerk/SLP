from django import forms
from .models import Merch

class MerchForm(forms.ModelForm):
    class Meta:
        model = Merch
        fields = [
            "product_name",
            "product_description",
            "product_category",
            "size",
            "quantity",
            "stock",
            "image",
        ]
