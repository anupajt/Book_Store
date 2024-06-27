from django.contrib import admin


# Register your models here.
from .models import Cart, CartItem, User_Credentials,Address





admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(User_Credentials)
