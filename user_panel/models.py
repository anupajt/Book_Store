import datetime

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from admin_panel.models import Book
from django.contrib.auth.models import User

phone_validator = RegexValidator(
    regex=r'^\+\d{9}$',  # Adjust the regex pattern as needed
    message="Phone number must be entered in the format: +999999999")


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Book, through='CartItem')



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)

class User_Credentials(models.Model):

    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email=models.EmailField()
    phone_number=models.CharField(validators=[phone_validator],max_length=10)

    password=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.first_name)

STATE_CHOICES = (
        ('', 'Select a State'),  # Empty choice for the default placeholder
        ('ap', 'Andhra Pradesh'),
        ('ar', 'Arunachal Pradesh'),
        ('as', 'Assam'),
        ('br', 'Bihar'),
        ('ch', 'Chhattisgarh'),
        ('ga', 'Goa'),
        ('gj', 'Gujarat'),
        ('hr', 'Haryana'),
        ('hp', 'Himachal Pradesh'),
        ('jh', 'Jharkhand'),
        ('ka', 'Karnataka'),
        ('kl', 'Kerala'),
        ('mp', 'Madhya Pradesh'),
        ('mh', 'Maharashtra'),
        ('mn', 'Manipur'),
        ('ml', 'Meghalaya'),
        ('mz', 'Mizoram'),
        ('nl', 'Nagaland'),
        ('or', 'Odisha'),
        ('pb', 'Punjab'),
        ('rj', 'Rajasthan'),
        ('sk', 'Sikkim'),
        ('tn', 'Tamil Nadu'),
        ('tg', 'Telangana'),
        ('tr', 'Tripura'),
        ('up', 'Uttar Pradesh'),
        ('uk', 'Uttarakhand'),
        ('wb', 'West Bengal'),
        ('an', 'Andaman and Nicobar Islands'),
        ('chd', 'Chandigarh'),
        ('dnh', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('dl', 'Delhi'),
        ('ld', 'Lakshadweep'),
        ('py', 'Puducherry'),
        # Add more states as needed
    )
PAYMENT_CHOICES = (
    ('S', 'Stripe'),

)

class Address(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255,validators=[phone_validator])
    street_address = models.CharField(max_length=255)
    apartment_suite = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.zip_code}, {self.country}"

class UserProfile(models.Model):
    user = models.OneToOneField(User_Credentials, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)

    # Other fields specific to the user profile

    def __str__(self):
        return self.user


class Order(models.Model):
    product = models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    image = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User_Credentials,on_delete=models.CASCADE,null=True,blank=True)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

class Order_confirm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return '{}'.format(self.user)
STATUS_CHOICES = (
        ('confirmed', 'Confirmed'),
        ('dispatched', 'Dispatched'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
class OrderItem(models.Model):
    order = models.ForeignKey(Order_confirm, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class UserLoginLog(models.Model):
    user = models.ForeignKey(User_Credentials, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.login_time}'