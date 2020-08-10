from django.db import models
from django.contrib.auth.models import User    

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length = 150)

    def __str__(self):
        return self.name


class Product(models.Model):

    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=150, choices=CATEGORY)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=250)
    date_created = models.DateField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, null = True, on_delete=models.SET_NULL) 
    product = models.ForeignKey(Product, null= True,  on_delete=models.SET_NULL)
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    date_created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length =200, choices=STATUS)






