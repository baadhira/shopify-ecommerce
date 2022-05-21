from datetime import date
# import datetime
from email import message
from django.shortcuts import get_object_or_404, render
# from datetime import timezone
import email
from multiprocessing import context
from django.contrib import messages,auth
from django.shortcuts import redirect, render
from adminapp.forms import *
from adminapp.models import *
import os
from twilio.rest import Client

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import razorpay
from datetime import timezone
from datetime import date
from datetime import datetime
from django.shortcuts import render
import razorpay
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings
from django.views.decorators.cache import never_cache
''' logger module'''
import logging
from django.core.mail import BadHeaderError,send_mail
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
logger = logging.getLogger(__name__)
from decouple import config
# Create your views here.
client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@never_cache
def userpage(request):
    now=datetime.now()
    products = Product.objects.all()
    banners = BannerUpdate.objects.filter(valid_from__lte=now, valid_to__gte=now, is_active = True)
    catogeries = Category.objects.all().annotate(numpro=Count('product'))
    for product in products:
        p_offer = 0
        c_offer=0
        prod_id = 0 
        try:
            prod_offer = ProductOffer.objects.get(product_id=product, valid_from__lte=now, valid_to__gte=now, is_active = True)
            p_offer = prod_offer.discount
            print("type of dicount/////////",type(p_offer))
        except:
            p_offer = 0

        try:
            categ_offer = CategoryOffer.objects.get(category_id=product.category,valid_from__lte=now, valid_to__gte=now, is_active = True)
            c_offer = categ_offer.discount
        except:
            c_offer = 0

        if p_offer>c_offer:
            disc_price = product.mrp_price - (product.mrp_price * p_offer)/100
            product.price = round(disc_price,2)
            product.discount_percentage = p_offer
            product.save()
        elif p_offer == c_offer and p_offer != 0:
            disc_price = product.mrp_price - (product.mrp_price * p_offer)/100
            product.price = round(disc_price,2)
            product.discount_percentage = c_offer
            product.save()
        elif p_offer == c_offer == 0 :
            product.price = product.mrp_price
            product.save()
    # breakpoint()
    hy = _cart_id(request)
    cartitem = Cart_Item.objects.filter(cart__cart_id = hy)
    print("cart item in userpage!")
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        print("home wishlist",wishlist)
        p = []
        for i in wishlist:
           p.append(i.product.id)
        print(p)
    else:
        wishlist='' 
        p=''
   
    product_offer=ProductOffer.objects.all()
    category_offer=CategoryOffer.objects.all()
    print("home products",products)
    print("productoffer home",product_offer)
    r = []
    for i in product_offer:
        r.append(i.product_id.id)
    print(r)

    context = {
        'products':products,
        'cartitem' :cartitem,
        'wishlist' : wishlist,
        'banners' : banners,
        # 'wish':wish,
        'catogeries':catogeries,
        'product_offer' : product_offer,
        'category_offer' : category_offer,
        'p':p,
        'r':r

    }
    
    return render(request,'userindex.html',context)
  
from django.core.paginator import  Paginator
@never_cache
def userproductgrid(request):
    product = Product.objects.all()
    catogeries = Category.objects.all().annotate(numpro=Count('product'))
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        print("home wishlist",wishlist)
        p = []
        for i in wishlist:
           p.append(i.product.id)
        print(p)
    else:
        messages.error(request,'no data') 

    paginator = Paginator(product, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'product' : paged_products,
        'catogeries' : catogeries,
        'wishlist':wishlist,
        'p':p
    }
    return render(request,'product-grids.html',context)


def userproductdetails(request,id):
    obj = Product.objects.get(id=id)
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        print("home wishlist",wishlist)
        p = []
        for i in wishlist:
           p.append(i.product.id)
        print(p)
    else:
        messages.error(request,'no data') 
    print("userproductdetails............",obj)
    context = {
        'obj':obj,
        'wishlist':wishlist,
        'p':p
    }
    return render(request,'userproductdetails.html',context)

@never_cache

def usersignup(request):
    if request.method == 'POST':
        form=CustomUserCreationForm(request.POST)
        print('form',form)
        if form.is_valid():
            user = form.save()
            request.session['username'] = user.username
            request.session['phoneno'] = user.phoneno
            print('username',user.username)
            
            messages.success(request,"User registered successfully")
            return redirect('userotp') 
        else:
            messages.error(request,'Invalid credentials')
            form=CustomUserCreationForm(request.POST)
            context = {
            'form' : form
            }
            return render(request,'signup.html',context)

    else:
        form=CustomUserCreationForm()
        context = {
        'form' : form
        }
        return render(request,'signup.html',context)
@never_cache

def userotp(request):
    username = request.session['username'] 
    phoneno = '+91'+request.session['phoneno']
    print(phoneno)
    if request.method == 'POST':
        
        otpgiven=request.POST['otp_input']
        account_sid = config('TWILIO_ACCOUNT_SID')
        auth_token = config('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        if(len(str(otpgiven))==6):

            verification_check = client.verify \
                            .services(config('SERVICES_SID')) \
                            .verification_checks \
                            .create(to=phoneno, code=otpgiven)
            print(verification_check.status)
        else:
            messages.error(request,"Enter a valid OTP!")
            return render(request, 'otp_verfication.html')
        if (verification_check.status == 'approved'):
            user = Userreg.objects.get(username=username)
            print(user)
            auth.login(request,user)
            return redirect('userpage')
    else:
        account_sid = config('TWILIO_ACCOUNT_SID')
        auth_token = config('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)

        verification = client.verify \
                            .services(config('SERVICES_SID')) \
                            .verifications \
                            .create(to= phoneno, channel='sms')

        print(verification.status)
        return render(request,'otp_verfication.html')

@never_cache

def userlogin(request):
    if request.user.is_authenticated and request.user.is_active == False:
        return redirect('userpage')
    # else:
    #     messages.error(request,"You have been blocked by admin")
    #     return redirect('userlogin')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == '' and password == '':
            messages.error(request,"enter valid data")
            return redirect('userlogin')
        
        user = authenticate(username=username,password=password)
       
        
        if user is not None and user.is_active == True:
            request.session['username'] = user.username
            request.session['phoneno'] = user.phoneno
            print(username)
            return redirect('userotp')
        else:
            form = AuthenticationForm()
            context = {
                'form':form
            }
            return render(request,'userlogin.html',context)
    else:
        form = AuthenticationForm()
        context = {
            'form':form
        }
        return render(request,'userlogin.html',context)
@never_cache

def userlogout(request):
    logout(request)
    return redirect('userlogin')


@never_cache
def userproductdetails(request,id):
    obj = Product.objects.get(id=id)
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        print("home wishlist",wishlist)
        p = []
        for i in wishlist:
           p.append(i.product.id)
        print(p)
    else:
        messages.error(request,'no data') 
    print("userproductdetails............",obj)
    context = {
        'obj':obj,
        'wishlist':wishlist,
        'p':p
    }
    return render(request,'userproductdetails.html',context)

@never_cache
def userprofilehome(request):
    return render(request,'userprofilehome.html')

    
@never_cache
def edituserprofile(request):
    context = {}
    id = request.user.id
    obj = Userreg.objects.get(id=id)
    
    form = EditUserForm(instance=obj)
    if request.method == 'POST':
        form = EditUserForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('userprofilehome')
        else:
            messages.error(request,"Invalid data")
    context['form'] = form
    return render(request,'edituserprofile.html',context)
    

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


from django.db.models import Count


    
@never_cache
def filterview(request,id):
    print("enteredddddddd filter view....................")
    category=Category.objects.all()
    catogeries = Category.objects.all().annotate(numpro=Count('product'))
    product = Product.objects.filter(category=id)
    

    context = {'product':product,'catogeries':catogeries}
    return render(request, "product-grids.html",context)

    
@never_cache
def contacts(request):
    if request.method == "POST":
        name=request.POST["name"]
        subject=request.POST["subject"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        
        message=request.POST["message"]
        
        

        if name and message and email:
            try:
                send_mail(name, message, email, ['baadhiraabdulla5@gmail.com'])
            except BadHeaderError:
                messages.error(request,'Invalid header found')
                return redirect('contacts')
            messages.success(request,"Form submitted successfully")
            return redirect('contacts')
        else:
        # In reality we'd use a form class
        # to get proper validation errors.
            messages.error("Make sure all fields are entered and valid.")
            return redirect('contacts')

    return render (request,"contact.html")

    
@never_cache
def hightolow(request):  
    product = Product.objects.all().order_by('-price')
    productcount=product.count()
    catogeries = Category.objects.all().annotate(numpro=Count('product'))
    context = {'product':product,'catogeries':catogeries,'count':productcount}
    return render(request, "product-grids.html",context)
# def remove_cart(request,id):
#     cart = Cart.objects.get(cart_id = _cart_id(request))
#     product = get_object_or_404(Product,id=id)
#     cart_item = Cart_Item.objects.get(product=product,cart=cart)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#         return redirect('cart')
#     return redirect('cart')

    
@never_cache
def lowtohigh(request):

    product = Product.objects.all().order_by('price')
 
    productcount=product.count()
  
    catogeries = Category.objects.all().annotate(numpro=Count('product'))
 
    context = {'product':product,'catogeries':catogeries,'count':productcount}
    return render(request, "product-grids.html",context)

    
@never_cache
def remove_cart(request,product_id, cart_item_id):
        
    product     = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item   = Cart_Item.objects.get(product = product, user=request.user, id=cart_item_id)
        else:
            cart        = Cart.objects.get(cart_id=_cart_id(request))
            cart_item   = Cart_Item.objects.get(product = product, cart = cart, id=cart_item_id)
        
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass    
    return redirect('cart')
    
@never_cache
def remove_cart_item(request):
    product_id =request.GET['prod_id']
    cart_item_id = request.GET['cartitem']
    # cart_item_id = request.GET['cartitem'] 
    product     = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item   = Cart_Item.objects.get(product = product, user = request.user, id=cart_item_id)
    else:
        cart        = Cart.objects.get(cart_id=_cart_id(request))
        cart_item   = Cart_Item.objects.get(product = product, cart = cart, id=cart_item_id)
    cart_item.delete()
    return JsonResponse({'success':'Item successfully Removed'})

    
@never_cache
def remove_cart_ajax(request):
    product_id =request.GET['prod_id']
    cart_item_id = request.GET['cart_id']
    
    product     = get_object_or_404(Product, id=product_id)
    print("product...........",product)
    try:
        print("entered first try.....................")
        if request.user.is_authenticated:
            cart_item   = Cart_Item.objects.get(product = product, user=request.user, id=cart_item_id)
            print("cart item in try..............",cart_item)
        else:
            cart        = Cart.objects.get(cart_id=_cart_id(request))
            cart_item   = Cart_Item.objects.get(product = product, cart = cart, id=cart_item_id)
            print("cart item in try..............",cart_item)
        
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
            print("cart ite,,,,,",cart_item.quantity )
        else:
            cart_item.delete()
    except:
        pass    
    return JsonResponse({'success':'Item successfully Removed'})

    
@never_cache
def add_cart_ajax(request):
    product_id = request.GET['prod_id']
    cart_item_id = request.GET['cart_id']
    product = get_object_or_404(Product, id =product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    try:
        cart_item = Cart_Item.objects.get(product=product,cart=cart,id=cart_item_id)
        cart_item.quantity += 1
        cart_item.save()
    except Cart_Item.DoesNotExist:
        cart_item = Cart_Item.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
            user = request.user
        )
        cart_item.save()
        cart.save()
    return JsonResponse({'success':"Item successfully Removed"})
    #     if request.user.is_authenticated:
    #         cart_item = Cart_Item.objects.get(product=product, user=request.user,id=cart_item_id)
    #     else:
    #         cart = Cart.objects.get(cart_id=_cart_id(request))
    #         cart_item = Cart_Item.objects.get(product=product,cart=cart,id=cart_item_id)
    #     if cart_item.quantity <= product.stocks:
    #         cart_item.quantity +=1
    #         cart_item.save()
    #     else:
    #         return redirect('cart')
    # except:
    #     pass
    # return JsonResponse({'success':"Item successfully Removed"})

@login_required(login_url='userlogin') 
@never_cache
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        grand_total = 0 
        if request.user.is_authenticated:
            cart_items = Cart_Item.objects.filter(user=request.user,is_active = True)
            print("user authenticated  cart..................",cart_items)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = Cart_Item.objects.filter(cart=cart,is_active = True)
            print("else  cart..................",cart_items)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity) 
            quantity += cart_item.quantity
        grand_total = total
        print("cart grand total........",grand_total)
    except ObjectDoesNotExist:
        return redirect('cart')
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'grand_total' : grand_total
    }
    return render(request,'cart.html',context)

@login_required(login_url='userlogin')
@never_cache  
def add_cart(request,id):
    print("entereddd add_cart......................")
    product = Product.objects.get(id=id)
    print("product add_cart...........",product)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        print("cart id...........",cart)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        print("except cart id...........",cart)
        cart.save()
    try:
        cart_item = Cart_Item.objects.get(product=product,cart=cart)
        print("cart itemmmmmmmmmm .....................add_cart",cart_item)
        cart_item.quantity += 1
        cart_item.save()
        print("cart itemmmmmmmmmm .....................add_cart........after save",cart_item)
    except Cart_Item.DoesNotExist:
        cart_item = Cart_Item.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
            user = request.user
        )
        cart_item.save()
    return redirect('cart')

    
    
@never_cache
def remove_wish_item(request):
    if request.user.is_authenticated:

        print("entered remove wishlist_item")
        product_id =request.GET['prodId']
        print('product id remove wish',product_id)
        wishlist_item = Wishlist.objects.get(user=request.user,product = product_id)
        wishlist_item.delete()
        return JsonResponse({'success':'Item successfully Removed'})
    
def deletewishlist(request):
    if request.user.is_authenticated:
        user=request.user
        Wishlist.objects.filter(user_id=user.id,product=Product.objects.get(id=id)).delete()
        return JsonResponse({'success':'Item successfully Removed'})




# def updateItem(request):
#     data = json.loads(request.data)
#     productId = data['productId']
#     action = data['action']
#     print('Action:',action)
#     print('productId:',productId)
#     return JsonResponse('Item was added',safe=False)
    
    
@never_cache
def addaddressprofile(request):
    addressconst=   Address.objects.filter(user=request.user)
    user=request.user
    if request.method == 'POST':
        
        form = AddressForm(request.POST)
        if form.is_valid():
            
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            
            messages.success(request,"Address added sucsessfully")
            return redirect('getaddress')
        else:
            form = AddressForm(request.POST)
            context = {
                
            }
        return render(request,'addaddress.html',context)
    else:
        form = AddressForm(request.POST)
        context = {
            'form' : form,
            'addressconst' : addressconst,
            'user' : user
        }
    return render(request,'addaddress.html',context)

    
@never_cache
def getaddress(request):
    user = request.user
    address = Address.objects.filter(user=user)
    context = {
        'address':address
    }
    return render(request,'useraddress.html',context)


# def deleteproduct(request,id):
#     obj = Product.objects.get(id=id)
#     obj.delete()
#     return redirect('getproduct')

    
@never_cache
def deleteaddress(request,id):
    obj = Address.objects.get(id=id)
    obj.delete()
    return redirect('getaddress')

    
@never_cache
def editaddress(request,id):
    context = {}
    obj = Address.objects.get(id=id)
    form = AddressForm(instance=obj)
    if request.method == 'POST':
        form = AddressForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('getaddress')
        else:
            messages.error(request,"Invalid data")
    context['form'] = form
    return render(request,'editaddress.html',context)


    
@never_cache
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
       
        grand_total = 0
        if request.user.is_authenticated:
            cart_items  = Cart_Item.objects.filter(user=request.user, is_active = True)
            address = Address.objects.filter(user = request.user.id).order_by('-id')[:3]
         
            for cart_item in cart_items:
                total   += (cart_item.product.mrp_price * cart_item.quantity)
                quantity += cart_item.quantity

        grand_total = round((total),2)
    except ObjectDoesNotExist:
        pass

    context     = {
        'address':address,
        'total': total, 
        'quantity': quantity, 
        'cart_items': cart_items,
        'grand_total':grand_total,
        }


    return render(request,'checkout.html',context)
# @login_required(login_url='userlogin')
# def checkout(request):
#     user= request.user
#     # print("////////////////////////////////////////////////////////////")
#     # print(request.user.username)
#     cart = Cart_Item.objects.filter(user=user)
#     address = Address.objects.filter(user=user)
    
#     # print(address)
#     context = {
#         'address':address,
#         'cart' : cart
#     }

#     return render(request,'checkout.html',context)

    
@never_cache
def addaddress(request):
    addressconst=   Address.objects.filter(user=request.user)
    user=request.user
    if request.method == 'POST':
        
        form = AddressForm(request.POST)
        if form.is_valid():
            
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            
            messages.success(request,"Address added sucsessfully")
            return redirect('placeorder')
        else:
            form = AddressForm(request.POST)
            context = {
                
            }
        return render(request,'checkoutaddress.html',context)
    else:
        form = AddressForm(request.POST)
        context = {
            'form' : form,
            'addressconst' : addressconst,
            'user' : user
        }
    return render(request,'checkoutaddress.html',context)



    
@never_cache
def placeorder(request,total=0,quantity=0):
    try:
        print("addressid :: first tryyyyyyyyyyyyy")
        address_id = request.POST['address']
    except:
        print("addres id : erroeeeeeeeeeeeeeee")
        messages.error(request,'Please select a billing address')
        return redirect('checkout')
    print("adress gotttttttttttttttttttttttttt")
    current_user= request.user
    print("userrrrrrrrrrrrrrrr",current_user)
    try:
        print("order : trryyyyyyyyyyyyyyyyyyyyy")
        order = Order.objects.get(user=current_user,is_ordered = False)
        print(order,'order number in place order')
        cart_items = Cart_Item.objects.filter(user=current_user)
        print("cart itemssssssssssssssssss",cart_items)
        grand_total =0 
        for cart_item in  cart_items:
            total += (cart_item.product_price * cart_item.quantity)
            quantity += cart_item.quantity
        grand_total = total 
        print("grand total........",grand_total)

        context = {
            'order' : order,
            'cart_items' : cart_items,
            'total' : total,
            'grand_total' : grand_total,
                    
        }
        return render(request,'payment.html',context)
    except:
        print("cartitem : exceptttttttttttttttttttttttttt")
        cart_items = Cart_Item.objects.filter(user=current_user)
        print("cart item found", cart_items)
        cart_count = cart_items.count()
        if cart_count <= 0:
            return redirect('userpage')
        
        grand_total = 0
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        grand_total = total
        print("grand total........",grand_total)
        razoypay_amount=grand_total*100
        if request.method == 'POST':
            form = CouponApplyForm()
            
            address_id = request.POST['address']
            address = Address.objects.filter(id = address_id,user= request.user.id)
            for i in address:
                first_name = i.first_name
                last_name = i.last_name
                phone = i.mobile
                email = i.email
                address_lane_1 = i.address_lane_1
                address_lane_2 = i.address_lane_2
                city = i.city
            try:
                print("user",request.user)
                data = Order.objects.get(user = request.user, is_ordered = False)
                
            except:
                print("order table excpet")
                data = Order()

            data.user = current_user
            data.first_name = first_name
            data.last_name = last_name
            data.phone = phone
            data.email = email
            data.address_lane_1 = address_lane_1
            data.address_lane_2 = address_lane_2
            data.city = city
           
            data.order_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            try:
                order = Order.objects.get(user = current_user, is_ordered = False, order_number=order_number)
                logger.info(order)
            except:
                print("exception ")

            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'grand_total' : grand_total,
                'address' : address,
                'razoypay_amount' : razoypay_amount

            }
            return render(request,'payment.html',context)
        else:
            print("lasttttttttttttttttttttttttttttttttt")
            return redirect('placeorder')

    
@never_cache
def codorder(request,order_number,total=0,quantity=0):
    print("cod function........")
    now = datetime.now()

    # breakpoint()
    order = Order.objects.get(user = request.user,is_ordered=False)
    print("order cod 1.....",order)
    code = order.coupon
    print("code.....",code)
    

    try:
        coupon = CouponCode.objects.get(code__exact = code,valid_from__lte=now, valid_to__gte=now, active = True)

        print("coupon.......",coupon)
        print("coupon........",coupon)
        if coupon:

            discount = coupon.discount
            print("discount....",discount)
            order_no = order.order_number 
            print('order_number........',order_number)           
            grand_total =0
            order.coupon = coupon
            order.discount = round(discount,2)
            order.save()
            current_user = request.user
            cart_items = Cart_Item.objects.filter(user = current_user)
            grand_total = 0
            total = 0
            quantity = 0
            for cartitem in cart_items:
                total += (cartitem.product.price * cartitem.quantity)
                quantity += cartitem.quantity

            grand_total = total
            nett_paid = grand_total
            print("grand toal at cod....",grand_total)
            discount_amount = round(grand_total * discount/100,2)
            print("discount amount....",discount_amount)
            total_after_coupon = round((float(grand_total - discount_amount)),2) 
            print("total after coupon.......",total_after_coupon)
            order.discount_amount = discount_amount
            order.nett_paid = nett_paid
            order.order_total = total_after_coupon
            order.coupon_use_status = True
            order.save()
            print("order_toAL.......",order_total)
            payment = Payment.objects.create(user=request.user,payment_method = "COD" ,amount_paid = order.order_total,payment_id = order.id)
            
            order.payment = payment
            order.is_ordered = True
            order.status = 'Completed'
            order.save()
            cartitems = Cart_Item.objects.filter(user= request.user)
            for cartitem in cartitems:
                orderproduct = OrderProduct()
                orderproduct.order = order
                orderproduct.payment = payment
                orderproduct.user = request.user
                orderproduct.product = cartitem.product
                orderproduct.quantity = cartitem.quantity
                orderproduct.product_price = cartitem.product.price
                orderproduct.save()
                product = Product.objects.get(id = cartitem.product.id)
                product.stocks -= cartitem.quantity
                product.save()
            cartitems.delete()
            try:
                order=Order.objects.get(order_number=order_number)
                print("try inside another try.........")
                ordered_products = OrderProduct.objects.get(id=order.id)
                sub_total = 0
                for i in ordered_products:
                    sub_total = i.product_price * i.quantity
                context = {
                    'order' : order,
                    # 'cartitems' : cartitems,
                    'payment' : payment,
                    'order_number': order.order_number,
                    'orderproduct' : orderproduct,
                    'subtotal':sub_total,
                    'transID' : payment.payment_id
                }
                Cart_Item.objects.filter(user=request.user).delete()
                return render(request,'ordersucess.html',context)
            except:
                pass
    except:
        try:
            order = Order.objects.get(user=request.user,is_ordered = False,order_number=order_number)
            print("second try in cod...........")
            print("order cod 2.......",order)
            payment = Payment.objects.create(user=request.user,payment_method = "COD" ,amount_paid = order.order_total,payment_id = order.id)
            payment.save()
            order.payment = payment
            order.is_ordered = True
            order.save()
            print("order number......",order_number)
            cartitems = Cart_Item.objects.filter(user = request.user)
            print("cartitems.....",cartitems)
            for cartitem in cartitems:
                print("cart item - ", cartitem)
                orderproduct = OrderProduct()
                orderproduct.order = order
                orderproduct.payment = payment
                orderproduct.user = request.user
                orderproduct.product = cartitem.product
                orderproduct.quantity = cartitem.quantity
                orderproduct.product_price = cartitem.product.price
                orderproduct.save()
                print("Orderproduct ---", orderproduct)
                product = Product.objects.get(id = cartitem.product.id)
                print("product--, going to delete quantity --")
                product.stocks -= cartitem.quantity
                product.save()
                print("qty reduced and saved")

            cartitems.delete()
            print("order number......",order_number)
            print("cartitems.....",cartitems)
            
            
            try:
                order = Order.objects.get(order_number=order_number)
                print("third try in cod..............")
                print("order number....",order_number)
                ordered_products = OrderProduct.objects.filter(id=order.id)
                print("orderproduct...",ordered_products)

                sub_total = 0
                for i in ordered_products:
                    sub_total = i.product_price * i.quantity
                print("subtotal......",sub_total)
                context = {
                    'order' : order,
                    # 'cartitems' : cartitems,
                    'payment' : payment,
                    'order_number': order.order_number,
                    'orderproduct' : orderproduct,
                    'subtotal':sub_total,
                    'transID' : payment.payment_id
                }
                Cart_Item.objects.filter(user=request.user).delete()
                
                return render(request,'ordersucess.html',context)
            except (Payment.DoesNotExist, Order.DoesNotExist):
                print("except of order is working")
                return redirect('userpage')
        except:
            print("no order numbers found, except working")
            return redirect('userpage')
    
    
@never_cache
def paypalpayment(request):
    body = json.loads(request.body)
   
    order = Order.objects.get(user = request.user,is_ordered = False,order_number=body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status']
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    cartitems=Cart_Item.objects.filter(user=request.user,is_active=True)
    for item in cartitems :
        ordered_product=OrderProduct()
        ordered_product.order=order
        ordered_product.payment=payment
        ordered_product.user=request.user
        ordered_product.product=item.product
        ordered_product.quantity=item.quantity
        ordered_product.product_price = item.product.price
        ordered_product.status = "Ordered"
        ordered_product.save()
        #reduce stock
        product=Product.objects.get(id=item.product.id)        
        product.stocks -= item.quantity
        product.save()

    #clear the cart
    print(cartitems,"before deleting")
    cartitems.delete()
    print(cartitems,"after deletion")


    data={
        'order_number':order.order_number,
        'trans_ID':payment.payment_id
    }   

    return JsonResponse(data)
    
@never_cache
@csrf_exempt
def razorpayorder(request):
    order_number = request.POST['order_number']
    print("order number at razzzzz",order_number)

    now = datetime.now()
    order = Order.objects.get(user=request.user,is_ordered=False,order_number = order_number)
    code = order.coupon
    print("code at razzzzzzzzzzz",code)

    try:
        print("entered first try in razzzzzzzzzzzzzz")
        coupon = CouponCode.objects.get(code__exact = code,valid_from__lte=now, valid_to__gte=now, active = True)
        if coupon:
            discount = coupon.discount
            order_no  = order.order_number
            print("order no at razzzzzz",order_no)
            current_user = request.user
            cart_items = Cart_Item.objects.filter(user= current_user)
            grand_total = 0
            total = 0
            quantity = 0
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            grand_total = round(total,2)
            nett_paid = grand_total
            discount_amount = grand_total * discount/100
            total_after_coupon = round(float(grand_total - discount_amount),2)
            print("total after coupon........",total_after_coupon)
            order.discount_amount = discount_amount
            order.nett_paid = nett_paid
            order.order_total = total_after_coupon
            order.coupon_use_status = True
            order.save()
            first_name = order.first_name
            last_name = order.last_name
            phone = order.phone
            email = order.email
            grand_total = order.order_total * 100
            order_number=order.order_number
            data = { "amount": grand_total, "currency": "INR", "receipt": order_number }
            print("data in raaz...",data)
            payment = client.order.create(data=data)
            context = {
                'payment':payment,
                'order':order,
                'grand_total':grand_total,
                'nett_paid' : net_paid,
                'first_name' :first_name,
                'last_name' :last_name,
                'phone' :phone,
                'email' :email,
                "order_number":order_number,
            
            }
            return JsonResponse(payment)
    except:
        order = Order.objects.get(user=request.user,is_ordered=False,order_number = order_number)
        first_name = order.first_name
        last_name = order.last_name
        phone = order.phone
        email = order.email
        grand_total = order.order_total * 100
        nett_paid = grand_total
        print("grand total at except at raaaaaaaaaaa",grand_total)
        order_number = order.order_number
        print("order_number total at except at raaaaaaaaaaa",order_number)
        data = { "amount": grand_total, "currency": "INR", "receipt": order_number }
        payment = client.order.create(data=data)
        context = {
            'payment':payment,
            'order':order,
            'grand_total':grand_total,
            'nett_paid' : nett_paid,
            'first_name' :first_name,
            'last_name' :last_name,
            'phone' :phone,
            'email' :email,
            "order_number":order_number,
            
        }
        return JsonResponse(payment)

    # order = Order.objects.get(user=request.user,is_ordered=False,order_number = order_number)
    # cart_items = Cart_Item.objects.filter(user = request.user,is_active = True)
    # grand_total = 0
    # for item in cart_items:
    #     total += (item.product.price * item.quantity)
    # grand_total = total*100
    # # payment = Payment(user=request.user,payment_id = order_number,payment_method = "Razorpay",amount_paid = grand_total,status = "COMPLETED")
    # # payment.save()
    # data = { "amount": grand_total, "currency": "INR", "receipt": order_number }
    # payment = client.order.create(data=data)
    # print(data)
    # print('all work done in razorpayorder, returning jsonresponse.')
    # return JsonResponse(payment)
    
@never_cache
def razorpayment(request):
   
    order_number = request.GET.get('order_number')
    order = Order.objects.get(user=request.user,is_ordered=False,order_number = order_number)
    
    # grand_total = 0
    # for cart_item in cart_items:
    #     total += (cart_item.product.price * cart_item.quantity)
    # grand_total = total
   
    payment = Payment(user=request.user,payment_id = order_number,payment_method = "Razorpay",amount_paid = order.order_total,status = "COMPLETED")
    print("paymenttttttttttttt at razzzzzzzz",payment)
    payment.save()
    order.payment= payment 
    order.is_ordered = True
    order.save()
    cart_items = Cart_Item.objects.filter(user = request.user,is_active = True)
    for cart_item in cart_items:
        ordered_product = OrderProduct()
        ordered_product.order = order
        ordered_product.payment = payment
        ordered_product.user = request.user
        ordered_product.product = cart_item.product
        ordered_product.quantity = cart_item.quantity
        ordered_product.product_price = cart_item.product.price
        ordered_product.status = "Ordered"
        ordered_product.save()
        product=Product.objects.get(id=cart_item.product.id)
        product.stocks -= cart_item.quantity
        product.save()
    order.is_ordered = True
    order.payment_id = payment.id 
    order.save()
    cart_items.delete()
    try:
        order = Order.objects.get(order_number=order_number)
        ordered_products = OrderProduct.objects.filter(id=order.id)
        sub_total = 0

        for i in ordered_products:
            sub_total += i.product_price * i.quantity
        context = {
            'order' : order,
            'payment' : payment,
            'ordered_product' : ordered_product,
            'order_number' : order_number
        }
        Cart_Item.objects.filter(user=request.user).delete()
        return render(request,'ordersucess.html',context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('userpage')

    
@never_cache
def userorderlist(request):
    ordered_products =  OrderProduct.objects.filter(user = request.user).order_by('-created_at')
    paginator = Paginator (ordered_products, 4)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
        'ordered_products' : paged_orders
    }
    return render(request,'userorderlist.html',context)
    
@never_cache
def cancel_order(request,id):
    if OrderProduct.objects.filter(id=id).exists():
        ordered_product = OrderProduct.objects.get(id=id)
        ordered_product.user_cancelled = True
        ordered_product.save()
        return redirect("userorderlist")
    else:
        return redirect("userorderlist")
    
    return redirect('userorderlist')
    
@never_cache
def return_order(request,id):
    if OrderProduct.objects.filter(id=id).exists():
        ordered_product = OrderProduct.objects.get(id=id)
        ordered_product.user_returned = True
        ordered_product.save()
        return redirect("userorderlist")
    else:
        return redirect("userorderlist")
    
    return redirect('userorderlist')
# def return_order(request,id):
#     if OrderProduct.objects.filter(id=id).exists():
#         ordered_product = OrderProduct.objects.get(id=id)
#         ordered_product
    
@never_cache
def user_order_return(request,order):
    order = OrderProduct.objects.get(user = request.user, order_number = order)
    # print(order, 'this is the order')
    if request.method == "POST":
        status = request.POST['user_order_return']
        # print(status)
    
    order.status = status
    order.save()

    return redirect('userorderlist')


    
@never_cache
def ClaimCoupon(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        form = form.cleaned_data['code']
        try:
            coupon = CouponCode.objects.get(code__iexact=code,valid_from__lte =now,valid_to__gte = now,active=True)
            request.session['coupon_id'] = coupon.id
        except CouponCode.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('placeorder')

from django.views.decorators.csrf import csrf_exempt
    
@never_cache
@csrf_exempt
def verifyCoupon(request):
    
    now = datetime.now()
    print('date now', now)
    if request.method == "POST":
        code= request.POST['code']
        print("code.........",code)
        try:
            coupon = CouponCode.objects.get(code__iexact=code,valid_from__lte =now,valid_to__gte = now,active=True)
            if coupon:
                try:
                    coupon_already_used = Order.objects.get(user=request.user,coupon=coupon,coupon_use_status=True)
                    if coupon_already_used:
                        context = {
                            'success' :'coupon already used'
                        }
                        return JsonResponse(context)
                    else:
                        discount = coupon.discount
                        order = Order.objects.get(user=request.user,is_ordered = False)
                        order_no = order.order_number
                        order.coupon = coupon
                        order.discount = round(discount,2)
                        order.save()
                        current_user = request.user
                        cart_items = Cart_Item.objects.filter(user = current_user)
                        grand_total = 0
                        total = 0
                        quantity = 0
                        for cartitem in cart_items:
                            total += (cartitem.product.price * cartitem.quantity)
                            quantity += cartitem.quantity
                        
                        grand_total = total
                        nett_paid = grand_total
                        
                        discount_amount = round(grand_total * discount/100,2)

                        total_after_coupon = round((float(grand_total - discount_amount)),2)

                        context = {
                            'success' : "valid",
                            'discount_amount' : discount_amount,
                            'nett_paid' : nett_paid,
                            'total_after_coupon' : total_after_coupon
                        }
                        return JsonResponse(context)
                except:
                    discount = coupon.discount
                    order = Order.objects.get(user = request.user,is_ordered= False)
                    order_no= order.order_number
                    order.coupon = coupon
                    order.discount = round(discount,2)
                    order.save()
                    current_user = request.user 
                    cart_items = Cart_Item.objects.filter(user = current_user)
                    grand_total = 0
                    total = 0
                    quantity = 0
                    for cartitem in cart_items:
                        total += (cartitem.product.price * cartitem.quantity)
                        quantity += cartitem.quantity
                    grand_total = total
                    nett_paid = grand_total
                    discount_amount = round(grand_total * discount/100,2)
                    total_after_coupon = round((float(grand_total - discount_amount)),2)

                    context = {
                        'success' : "valid",
                        'discount_amount' : discount_amount,
                        'total_after_coupon' : total_after_coupon,
                        'nett_paid' : nett_paid,
                        
                    }
                    return JsonResponse(context)
        except CouponCode.DoesNotExist:
            context = {
                'success' : 'no coupon'
            }
            return JsonResponse(context)
    
@never_cache
def _wishcart_id(request):
    wishcart        = request.session.session_key
    if not wishcart:
        wishcart    = request.session.create()
    return wishcart
    
@never_cache
@login_required(login_url='userlogin')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render (request, 'wishlist.html',context)
    
@never_cache
@login_required(login_url='userlogin')
@csrf_exempt
def add_wishlist(request):    
    if request.user.is_authenticated:
        wish_list = Wishlist.objects.filter(user = request.user.id)
        if request.method == 'POST':
            if request.user.is_authenticated:                
                product_id = request.POST['id']
                user = Userreg.objects.get(id = request.user.id)
                product = Product.objects.get(id = product_id)            
                wishlist = Wishlist()
                wishlist.product = product
                wishlist.user = user
                wish_item = Wishlist.objects.filter(product = product, user = request.user).first()
                if wish_item:
                    pass                    
                else:                    
                    wishlist.save()
                wish_item_count = Wishlist.objects.filter(user = request.user).count()
                success = 'product added to wishlist!!!'
                return JsonResponse({'success': success,'wish_items':wish_item_count})
            else:
                error = "error"
                return JsonResponse({'error':error })
    else:
        messages.error(request,"please login!!")
        return redirect('userlogin')
    wishlist_items = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render (request, 'wishlist.html',context)




def addWishList(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            productId = request.POST.get('wish_product')
            action = request.POST.get('wish_action')
            product = Product.objects.get(id=productId)
            if action == 'add_wish':
                wishlist = Wishlist.objects.get_or_create(wish_user=user,wish_product=product)
                result = 'added'
                status = 'added to'
                msg = 'success'
            elif action == 'remove_wish':
                wishlist = Wishlist.objects.get(wish_user=user,wish_product=product)
                wishlist.delete()
                result = 'removed'
                status = 'removed from'
                msg = 'error'
        data = {'result':result,'productId':productId,'status':status,'msg':msg}
    return JsonResponse(data)


def myWishList(request):
    user = request.user
    products = Wishlist.objects.filter(wish_user=user)
    counts = products.count()
    order = Order.objects.get(user = user,order_status=False)
    wish = [i.wish_product for i in  Wishlist.objects.filter(wish_user=user)]
    return render(request,'fitness/mywishlist.html',{'products':products,'wish':wish,'counts':counts,'order':order})


@never_cache
def ordersuccess(request):
    return render(request,'ordersucess.html')
    
@never_cache                       
def search(request):
    print("entered search function......................")
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            product = Product.objects.filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            print("product....................",product)
            product_count = product.count()
            print("product count..........",product_count)
        context = {
            "product": product,
            "product_count": product_count,
        }
    return render(request, "product-grids.html", context)

    









   

  

  







