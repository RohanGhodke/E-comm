from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address_line_1 = models.TextField(max_length=40)
    address_line_2 = models.TextField(max_length=40)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=20)
    mobile = models.CharField(max_length=13)

    def __str__(self):
        return 'Address of: ' + self.user.first_name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    subcategory = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='myCart/images', default='')

    def __str__(self):
        return self.product_name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' cart'

    def get_total_price(self):
        return self.quantity * self.product.price
