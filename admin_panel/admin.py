from django.contrib import admin

from user_panel.models import OrderItem
from .forms import OrderItemAdminForm
from .models import Category
# Register your models here.
admin.site.register(Category)
from .models import Notification

class OrderItemAdmin(admin.ModelAdmin):
   # Define the fields to display in the list view
 # Add search functionality

    form = OrderItemAdminForm
    list_display = ('order', 'product', 'quantity', 'price', 'status')
    list_filter = ('order__user', 'status')
    search_fields = ('product__name', 'order__user__username')

    actions = ['update_status']

    def update_status(self, request, queryset):
        new_status = request.POST.get('status')
        if new_status:
            queryset.update(status=new_status)

    update_status.short_description = 'Update selected items status'

admin.site.register(OrderItem, OrderItemAdmin)