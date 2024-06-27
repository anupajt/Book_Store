from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):

    c_name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='books_media')
    description=models.TextField()
    def __str__(self):
        return '{}'.format(self.c_name)



class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    description = models.TextField(max_length=800)
    image = models.ImageField(upload_to="book_media")
    out_of_stock = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)

    @staticmethod
    def get_products_by_id(ids):
        return Book.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Book.objects.all()


    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Book.objects.filter(category=category_id)
        else:
            return Book.get_all_products()

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.user)


