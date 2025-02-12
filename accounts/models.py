from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
from django.core.validators import MaxValueValidator,MinValueValidator
import datetime
from phone_field import PhoneField
# Create your models here.
class UserManager(BaseUserManager):
    """user model base user manager"""
    def create_user(self,email,password,**kwargs):
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """user model"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    adress = models.CharField(max_length=400,default='Bengaluru 560094')
    phone = models.CharField(max_length=12,blank=True, help_text='Contact phone number')

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

class Category(models.Model):

    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    description = models.CharField(max_length=500)
    image = models.ImageField(blank=True,upload_to='products')
    quantity = models.PositiveIntegerField(default=10)
    avg_rating = models.DecimalField(default=0,max_digits=3,decimal_places=2)

    def __str__(self):
        return self.name


class Orders(models.Model):
    PAYMENT_CHOICES = {
        "COD": "Cash on delivery",
        "UPI": "UPI payment",
        "CARD": "debit card,credit card",
    }
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True)
    payment_method = models.CharField(max_length=30,choices=PAYMENT_CHOICES,default='COD')
    quantity = models.PositiveIntegerField(default=1)
    return_status = models.CharField(max_length=30,default='not returned')

    def __str__(self):
        return self.user.name + self.product.name


class Review(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='review_user')
    review_product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='review_product')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.CharField(max_length=500,blank=True)

    def __str__(self):
        return f'{str(self.rating)} | {self.review_product.name}'


class ReturnOrders(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    return_status = models.CharField(max_length=30,default='pending')
    def __str__(self):
        return self.user.name