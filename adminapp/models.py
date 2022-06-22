
# Create your models here.
from ast import Try
from distutils.command.upload import upload
import email
from email.policy import default
from itertools import product
from telnetlib import STATUS
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import BooleanField, DateTimeField
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.urls.converters import SlugConverter
from django.conf import settings
# Create your models here.
class Userreg(AbstractUser):
    phoneno=models.CharField(max_length=11,null=True)
    adminstatus=models.BooleanField(blank=True,default=False)



class Category(models.Model):
    category_name= models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=100,unique=True, blank=True,null=True)
    def __str__(self):
        return self.category_name
# class Subcategory(models.Model):
#     subcategory_name = models.CharField(max_length=100)
#     category_id = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True)



class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    description = models.TextField(blank=True)
    price = models.FloatField(null=True,blank=True)
    stocks = models.IntegerField()
    product_image1 = models.ImageField(upload_to='images',blank=True,null=True)
    product_image2 = models.ImageField(upload_to='images',blank=True,null=True)
    product_image3 = models.ImageField(upload_to='images',blank=True,null=True)
    product_image4 = models.ImageField(upload_to='images',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    discount_type       = models.CharField(max_length=50, null=True,blank=True)
    descriptionone = models.TextField(blank=True,null=True)
    descriptiontwo = models.TextField(blank=True,null=True)
    descriptionthree = models.TextField(blank=True,null=True)
    descriptionfour = models.TextField(blank=True,null=True)
    mrp_price           = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    is_available        = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now_add=True,null=True)
    modiified_date      = models.DateTimeField(auto_now=True,null=True)
    users_wishlist=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='user_wishlist',blank=True)
    # sub_category = models.ForeignKey(Subcategory,on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return str(self.id)
   
class ProductOffer(models.Model):
    product_id      = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True, blank=True)
    code            = models.CharField(max_length=50, unique=True)
    valid_from      = models.DateTimeField()
    valid_to        = models.DateTimeField()
    discount        = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    is_active       = models.BooleanField()

    def __str__(self):
        return str(self.product_id)
    
    def disc_product_price(self):
        original_price = self.product_id.price
        disc_price = original_price - (original_price*(self.discount/100))
        return disc_price
   

# class PostImage(models.Model):
#     post = models.ForeignKey(Product,on_delete=models.CASCADE)
#     product_images= models.FileField(upload_to='media/')
#     def __str__(self):
#         return self.product_name

class Address(models.Model):
    user = models.ForeignKey(Userreg,on_delete=models.SET_NULL,null=True,blank=True)
    type = models.CharField(max_length=50,blank=True,null=True)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile= models.CharField(max_length=11,blank=True,null=True)
    email = models.EmailField(max_length=50,blank=True,null=True)
    address_lane_1 = models.CharField(max_length=100,blank=True,null=True)
    address_lane_2 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50,blank=True,null=True)
    pincode = models.CharField(max_length=10,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name



class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return str(self.id)

class Cart_Item(models.Model):
    user = models.ForeignKey(Userreg,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    def sub_total(self):
        return self.product.price*self.quantity
    def __str__(self):
        return self.product.product_name

class Customer(models.Model):
    user = models.ForeignKey(Userreg,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.name
        
# class Order(models.Model):
#     customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True,blank=True)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False,null=True,blank=False)
#     transaction_id = models.CharField(max_length=200,null=True)
#     def __str__(self):
#         return str(self.id)
# class OrderItem(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,blank=True)
#     order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True,blank=True)
#     quantity = models.IntegerField(default=0,null=True,blank=True)
#     date_added = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Paid','Paid'),
        ('Refund','Refund'),
        
    )
    user = models.ForeignKey(Userreg,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=50,null=True,blank=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField(null=True,blank=True)
    status = models.CharField(max_length=50, choices=STATUS, default='Pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True,blank=True,null=True)

    def __str__(self):
        return self.payment_method


class CouponCode(models.Model):
    code = models.CharField(max_length=50,unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    active= models.BooleanField()

    def __str__(self):
        return self.code


class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(Userreg,on_delete=models.SET_NULL,null=True)
    payment = models.OneToOneField(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20,blank=True,null=True)
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(max_length=50,blank=True,null=True)
    address_lane_1 = models.CharField(max_length=100,blank=True,null=True)
    address_lane_2 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    order_note = models.CharField(max_length=50,blank=True)
    order_total = models.FloatField(blank=True,null=True)
    # payment_method      = models.CharField(max_length = 50, blank = True)
    tax = models.FloatField(blank=True,null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='New')
    ip = models.CharField(max_length=20,blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now = True,blank=True,null=True)
    coupon_use_status     = models.BooleanField(default=False)
    coupon = models.ForeignKey(CouponCode,null=True,on_delete=models.SET_NULL, blank=True)
    discount_amount = models.FloatField(null=True,blank=True)
    nett_paid       = models.FloatField(null=True,blank=True)
    discount        = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_items(self):        
        items = self.orderproduct_set.all()
        for i in items :
            print(i,',')
        total = sum([i.quantity for i in items])
        return total







class OrderProduct(models.Model):
    STATUS = (
        ('Ordered','Ordered'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
        ('Return collected','Return collected'),
       
    )
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user = models.ForeignKey(Userreg,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='Ordered',blank=False,null=False)
    # coupon_used=models.BooleanField(default=False, null=True , blank=True )
    # orderded = models.BooleanField(default=False)
    user_cancelled=models.CharField(default=False,max_length=20,null=True)
    user_returned=models.CharField(default=False,max_length=20,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.product_name

   

# class Coupon(models.Model):
#     code        = models.CharField(max_length=50,unique=True,)
#     valid_from  = models.DateTimeField()
#     valid_to    = models.DateTimeField()
#     discount    = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
#     active      = models.BooleanField()

    

#     def __str__(self):
#         return self.code
# class Coupon(models.Model):
#     coupon_title = models.CharField(max_length=30,unique=True)
#     coupon_code = models.CharField(max_length=30,unique=True,null=True)
#     coupon_limit = models.IntegerField(blank=False,null=True)
#     coupn_offer = models.FloatField(blank=False)
#     coupon_start = models.DateField(blank=False)
#     coupon_end = models.DateField(blank=False)
#     is_available = models.BooleanField(default=True)
    

#     def check_expired(self):
#         today = date.today()
#         today1 = today.strftime("%Y-%m-%d")
#         if str(self.coupon_end) > today1 and self.is_available == True:
#             return False
#         else:
#             return True
    
#     def check_expired_date_only(self):
#         today = date.today()
#         today1 = today.strftime("%Y-%m-%d")

#         return str(self.coupon_end) <= today1
#     def __str__(self):
#         return self.coupon_title
    
# class Couponused(models.Model):
#     user = models.ForeignKey(Userreg,on_delete=models.CASCADE)
#     coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE)
#     order = models.OneToOneField(Order,on_delete=models.SET_NULL,null=True)

#     order_number = models.CharField(max_length=100,null=True)
#     is_ordered = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now_add=True)
#     used = models.BooleanField(default=False,null=True,blank=True)
#     loss = models.FloatField(max_length=30,default=0,null=True,blank=True)
#     applied = models.BooleanField(default=False,null=True,blank=True)

class WishCart(models.Model):
    wishcart_id     = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)     

    def __str__(self):
        return self.cart_id   

class Wishlist(models.Model):
    wishcart        = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Userreg,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.id)



class CategoryOffer(models.Model):
    category_id     = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True, blank=True)
    code            = models.CharField(max_length=50, unique=True)
    valid_from      = models.DateTimeField()
    
    valid_to        = models.DateTimeField()
    discount        = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(75)])
    is_active       = models.BooleanField()

    def __str__(self):
        return self.code
    
    def disc_product_price(self):
        original_price = self.category_id.product.price
        disc_price = original_price - (original_price*(self.discount/100))
        return disc_price


class BannerUpdate(models.Model):
    banner_image    = models.ImageField(blank = True,upload_to = 'banner_images')
   
    valid_from      = models.DateTimeField()
    valid_to        = models.DateTimeField()
    is_active       = models.BooleanField()
    created_at      = models.DateTimeField(auto_now_add=True)
 

  