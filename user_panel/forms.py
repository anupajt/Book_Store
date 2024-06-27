# from .models import User_Credentials
from django import forms
from admin_panel.models import Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from user_panel.models import Address


class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']




class CategorySelectForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        required=False  # Optional selection
    )
class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name','phone_number','street_address', 'apartment_suite', 'city', 'state', 'zip_code', 'country']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'apartment_suite': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }


        # Optional: Add custom validation methods
        def clean_zip_code(self):
            zip_code = self.cleaned_data['zip_code']
            # Add custom zip code validation logic here, e.g., check for valid format
            return zip_code
