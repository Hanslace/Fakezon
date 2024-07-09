from django.db import models 
import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError



class Category(models.Model):
    categoryName = models.TextField(primary_key=True , unique=True)

    def __str__(self):
        return self.categoryName
    
class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    customerID = models.AutoField(primary_key=True )
    date_modified = models.DateTimeField(   CustomUser, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    @property
    def total_sales(self):
        return Product.objects.annotate(total_sales=models.F('price') * models.F('sales')).aggregate(total=models.Sum('total_sales'))['total']
    @property
    def seller_rating(self):
        return Product.objects.filter(seller = self.user).annotate(avg_rating=models.Avg('rating')).aggregate(overall_avg=models.Avg('avg_rating'))['overall_avg']
    @property
    def total_orders(self):
        return Product.objects.filter(seller = self.user).annotate(total_orders=models.Sum('sales')).aggregate(total=models.Sum('total_orders'))['total']
class Wishlist(models.Model):
    customer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Cart(models.Model):
    customer = models.OneToOneField(CustomUser , on_delete=models.CASCADE)

    
    @property
    def total_orders(self):
        return CartItem.objects.filter(cart = self).count()
    

def zero_check(val):
    if val < 0:
        raise ValidationError


class Product(models.Model):
    productID = models.AutoField(primary_key=True )
    seller =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category , on_delete=models.CASCADE , blank = True  )
    name  = models.CharField(max_length=100)
    price  = models.DecimalField(default=0 , decimal_places=2, max_digits= 6 )
    description  = models.CharField(max_length=250 , default= ' ' , blank= True , null=True)
    image  = models.ImageField(upload_to='uploads/product/',  blank = True)
    rating = models.IntegerField(choices= ((1, 'Poor') , (2, 'Bad') ,(3, 'OK') ,(4, 'Good') ,(5, 'Amazing') , (0 ,'Not Rated')  ) , default=0)
    stock =  models.PositiveIntegerField( default = 0)
    wishlisted = models.ManyToManyField(Wishlist , blank=True)
    sales =  models.PositiveIntegerField(default = 0 )

    
class CartItem(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity =  models.PositiveIntegerField(default = 1 )
    cart = models.ForeignKey(Cart , on_delete= models.CASCADE)

    @property
    def calc_cost(self):
        return self.product.price * self.quantity
    
class Order(models.Model):
    orderID = models.AutoField(primary_key=True )
    product = models.ForeignKey(Product , on_delete=models.DO_NOTHING)
    cost = models.PositiveIntegerField(default = 0 )
    customer = models.ForeignKey(  CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.today)
    address = models.CharField(max_length=100 , default= ' ' , blank = True)
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ( 'Debit Card' ,'Debit Card' ),
        ('Cash', 'Cash'),
    ]

    paymentMethod = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default='Credit Card',
    )
    quantity = models.PositiveIntegerField(default = 1 )

    