from dataclasses import fields
from pyexpat import model
import django
from django import forms
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import ModelForm

from .models import *
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=Userreg
        fields=('username','email','phoneno','password1','password2')
    
class EditUserForm(forms.ModelForm):
    class Meta:
        model=Userreg
        fields=('username','email','phoneno')

class Productform(ModelForm):
    class Meta:
        model = Product
        fields = ('product_name','description','category','mrp_price','stocks','product_image1','product_image2','product_image3','product_image4','descriptionone','descriptiontwo','descriptionthree','descriptionfour')
        labels = {
            'product_name':'Product name',
            'description' : 'Description',
            'descriptionone' : 'Specification 1',
            'descriptiontwo' : 'Specification 2',
            'descriptionthree' : 'Specification 3',
            'descriptionfour' : 'Specification 4',

            'category' : 'Category',
            'mrp_price' : 'Price',
            'stocks' : 'InStock',
            'product_image1' : 'Cover Image 1',
            'product_image2' : 'Cover Image 2',
            'product_image3' : 'Cover Image 3',
            'product_image4' : 'Cover Image 4',
        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = '__all__'
class EditCategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = '__all__'


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('type','first_name','last_name','mobile','email','address_lane_1','address_lane_2','city','district','state','country','pincode')
        labels = {
            'type' : 'Address Type',
            'first_name':'First name',
            'last_name' : 'Last name',
            'mobile' : 'Mobile',
            'address_lane_1' : 'Address Lane 1',
            'address_lane_2' : 'Address Lane 1',
            'city' : 'City',
            'state' : 'State',
            'country' : 'Country',
            'pincode' : 'Pincode',
        }


class DateInput(forms.DateTimeInput):
    input_type = 'date'

# class CouponForm(ModelForm):
#     class Meta:
#         model=Coupon
#         fields = ('coupon_title','coupon_code','coupon_limit','coupn_offer')
#         labels = {
#             'coupon_title' : 'Coupon Title',
#             'coupon_code':'Coupon Code',
#             'coupon_limit' : 'Coupon Limit',
#             'coupn_offer' : 'Coupon Offer Price',
            
#         }


class CouponApplyForm(forms.ModelForm):
    class Meta:
        model = CouponCode
        fields = ['code','valid_from','valid_to','discount','active']
        widgets = {
            'valid_from': DateInput(),
            'valid_to':DateInput(),
        }    
        def __init__(self,*args,**kwargs):
            super(CouponApplyForm, self).__init__(*args, **kwargs)

class EditCouponForm(forms.ModelForm):
    class Meta:
        model=CouponCode
        fields=('code','valid_from','valid_to','discount','active')
        


class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['code','product_id', 'valid_from','valid_to','discount','is_active']
        widgets = {
            'valid_from': DateInput(),
            'valid_to':DateInput(),
        }
    
        def __init__(self,*args,**kwargs):
            super(ProductOfferForm, self).__init__(*args, **kwargs)

class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = ['code','category_id', 'valid_from','valid_to','discount','is_active']
        widgets = {
            'valid_from': DateInput(),
            'valid_to': DateInput(),
        }
    
        def __init__(self,*args,**kwargs):
            super(CategoryOfferForm, self).__init__(*args, **kwargs)        

class EditCouponCatForm(forms.ModelForm):
    class Meta:
        model=CategoryOffer
        fields=('code','category_id', 'valid_from','valid_to','discount','is_active')
class EditProductOffer(forms.ModelForm):
    class Meta:
        model=ProductOffer
        fields=('code','product_id', 'valid_from','valid_to','discount','is_active')