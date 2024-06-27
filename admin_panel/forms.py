from user_panel.models import OrderItem
from .models import Book,Category
from django import forms


class BookForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,)
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", 'placeholder': "Enter Book name"}),
            "author": forms.TextInput(attrs={"class": "form-control", 'placeholder': "Enter Author name"}),
            "description": forms.Textarea(attrs={"class": "form-control", 'placeholder': "Enter Book description"}),
            "price": forms.NumberInput(attrs={"class": "form-control", 'placeholder': "Enter Price"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", 'placeholder': "Enter Quantity"}),
            'out_of_stock':forms.CheckboxInput(attrs={'class':'form-control'}),

        }

class Categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            "c_name": forms.TextInput(attrs={"class": "form-control", 'placeholder': "Enter Book Category"}),
            'image': forms.FileInput(attrs={"class": "form-control-file"}),
            'description':forms.Textarea(attrs={"class": "form-control", 'placeholder': "Enter  Category Description"})

        }


class OrderItemAdminForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('dispatched', 'Dispatched'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=True)

    class Meta:
        model = OrderItem
        fields = '__all__'