from itertools import count
from django.shortcuts import render

# Create your views here.
from multiprocessing import context
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from adminapp.forms import *
from django.contrib import messages,auth
from adminapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import timezone
from datetime import date
from datetime import datetime
''' logger module'''
import logging
logger = logging.getLogger(__name__)
import csv
import xlwt
from dash import dcc
from datetime import date


def adminpage(request):
    products = Product.objects.all()
   
    ordered = OrderProduct.objects.filter(status = 'Ordered').count()
    print("ordereddddddddddd",ordered)
    shipped = OrderProduct.objects.filter(status = 'Shipped').count()
    delivered = OrderProduct.objects.filter(status = 'Delivered').count()
    cancelled = OrderProduct.objects.filter(status = 'Cancelled').count()
    returned = OrderProduct.objects.filter(status = 'Returned').count()
    order_status = [ordered,shipped,delivered,cancelled,returned]

    cod = Payment.objects.filter(payment_method = 'COD').count()
    payp = Payment.objects.filter(payment_method = 'Paypal').count()
    razorp = Payment.objects.filter(payment_method = 'Razorpay').count()
    payment_type= [cod,payp,razorp]

    customsc = Userreg.objects.all().count()
    ordersc = Order.objects.all().count()
    productsc = Product.objects.all().count()
    total_sales = Payment.objects.all().aggregate(Sum('amount_paid'))
    # print(total_sales,'total_sales..........')
    # sales = total_sales.amount_paid__sum/ordersc
    # average_sale = round(sales,2)
    

    context = {'products' : products,'total_sales':total_sales,'customsc':customsc,'productsc': productsc,'ordersc':ordersc,'order_status':order_status,'payment_type':payment_type,'dashboard':'dashboard',}
    return render(request,'main.html',context)






def addproduct(request):
    if request.method == 'POST':
        form = Productform(request.POST,request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request,"Product added successfully")
            return redirect('getproduct')
        else:
            form = Productform(request.POST,request.FILES)
            context = {
                'form' : form
            }
            return render(request, 'addproduct.html', context)
    else:
        form = Productform(request.POST,request.FILES)
        context = {
                'form' : form
            }
        return render(request, 'addproduct.html', context)

from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator

    
def getproduct(request):
    product = Product.objects.all()
    paginator = Paginator (product, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'product':paged_products,
        'pro':'pro'
    }
    return render(request,'productlist.html',context)


def editproduct(request,id):
    context = {}
    obj = Product.objects.get(id=id)
    form = Productform(instance = obj)
    if request.method == 'POST':
        form = Productform(request.POST,request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('getproduct')
        else:
            messages.error(request,'Form is not valid')
    context['form'] = form
    return render(request,'editproduct.html',context)

def deleteproduct(request,id):
    obj = Product.objects.get(id=id)
    obj.delete()
    return redirect('getproduct')


def getusers(request):
    user = Userreg.objects.all()
   
    context = {
        'user' : user,
        'cust' : 'cust'
    }
    return render(request,'customers.html',context)

# def editusers(request,id):
#     context = {}
#     obj = Userreg.objects.get(id=id)
#     form = EditUserForm(instance = obj)
#     if request.method == 'POST':
#         form = EditUserForm(request.POST,instance=obj)
#         if form.is_valid():
#             form.save()
#             return redirect('getusers')
#         else:
#             messages.error(request,'Form is not valid')
#     context['form'] = form
#     return render(request,'editusers.html',context)


def blockuser(request,id):
    obj = Userreg.objects.get(id=id)
    if obj.is_active == True:
        obj.is_active=False
    else:
        obj.is_active=True
    obj.save()
    return redirect('getusers')

def addcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request,'Category created successfully')
            return redirect('getcategory')
        else:
            form = CategoryForm(request.POST)
            context = {
                'form':form
            }
            return render(request,'addcategory.html',context)
    else:
        form = CategoryForm(request.POST)
        context = {
            'form':form
        }
        return render(request,'addcategory.html',context)

# def editcoupon(request,id):
#     context = {}
#     obj = CouponCode.objects.get(id=id)
#     form = EditCouponForm(instance = obj)
#     if request.method == 'POST':
#         form = EditCouponForm(request.POST,instance=obj)
#         if form.is_valid():
#             form.save()
#             return redirect('displaycoupon')
#         else:
#             messages.error(request,'Form is not valid')
#     context['form'] = form
#     return render(request,'editcoupon.html',context)


def editcategory(request,id):
    context = {}
    obj = Category.objects.get(id=id)
    form = EditCategoryForm(instance= obj)
    if request.method == 'POST':
        form = EditCategoryForm(request.POST, instance= obj)
        if form.is_valid():
            form.save()
            return redirect('getcategory')
        else:
            messages.error(request,'Form is not valid')
    context['form'] = form
    return render(request,'editcategory.html',context)


def getcategory(request):
    cat = Category.objects.all()
    context = {
        'cat' : cat,
        'catogeries':'catogeries'
    }
    return render(request,'categorylists.html',context)


def deletecategory(request,id):
    obj = Category.objects.get(id=id)
    obj.delete()
    return redirect('getcategory')


def adminlogin(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('adminpage')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None and user.is_staff == True :
            return redirect('adminpage')
        else:
            messages.error(request,'Invalid credentials')
            return render(request,'adminlogin.html')
    return render(request,'adminlogin.html')


def adminlogout(request):
    logout(request)
    return redirect('adminlogin')

def displayorderadmin(request,total=0):
    obj = OrderProduct.objects.all()
    paginator = Paginator (obj, 4)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
        'obj' : paged_orders,
        'abc':'abc'
    }
    return render(request,'adminorderlist.html',context)

def editorderadmin(request,id):
    print('in edit order')
    if request.method == 'POST':
        obj = OrderProduct.objects.get(id=id)
        obj.status=request.POST['status']
        obj.save()
        return redirect('displayorderadmin')
    else:
        return redirect('displayorderadmin')

def statusOrder(request,id):
    if request.method == "GET":
        status=request.GET.get('status')
        print(status)
        order_instance = OrderProduct.objects.get(id=id)
        if status :
            order_instance.status = status
            order_instance.save()
        
    return redirect('displayorderadmin')  


    # paginator = Paginator (product, 4)
    # page = request.GET.get('page')
    # paged_products = paginator.get_page(page)
    # context = {
    #     'product':paged_products
    # }


def displaycoupon(request):
    obj = CouponCode.objects.all()
    paginator = Paginator (obj, 3)
    page = request.GET.get('page')
    paged_coupon = paginator.get_page(page)
    context = {
        'coupon' : paged_coupon,
        'Coupons' :'Coupons'
    }
    return render(request,'displaycoupon.html',context)

# def chart(request):
#     return render(request,'chart.html')      
    

def addCoupon(request):
    if request.method == 'POST':
        form = CouponApplyForm(request.POST)
        if form.is_valid():
            coupon = form.save()
            messages.success(request,'Coupon created successfully')
            return redirect('displaycoupon')
        else:
            form = CouponApplyForm(request.POST)
            context = {
                'form' : form
            }
            return render(request,'addcoupon.html',context)
    else:
        form = CouponApplyForm(request.POST)
        context = {
            'form' : form
        }
        return render(request,'addcoupon.html',context)


def editcoupon(request,id):
    context = {}
    obj = CouponCode.objects.get(id=id)
    form = EditCouponForm(instance = obj)
    if request.method == 'POST':
        form = EditCouponForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('displaycoupon')
        else:
            messages.error(request,'Form is not valid')
    context['form'] = form
    return render(request,'editcoupon.html',context)

def deletecoupon(request,id):
    obj = CouponCode.objects.get(id=id)
    obj.delete()
    return redirect('displaycoupon')

# def editusers(request,id):
#     context = {}
#     obj = Userreg.objects.get(id=id)
#     form = EditUserForm(instance = obj)
#     if request.method == 'POST':
#         form = EditUserForm(request.POST,instance=obj)
#         if form.is_valid():
#             form.save()
#             return redirect('getusers')
#         else:
#             messages.error(request,'Form is not valid')
#     context['form'] = form
#     return render(request,'editusers.html',context)






#  if request.method == 'POST':
#         form = Productform(request.POST,request.FILES)
#         if form.is_valid():
#             product = form.save()
#             messages.success(request,"Product added successfully")
#             return redirect('adminpage')
#         else:
#             form = Productform(request.POST,request.FILES)
#             context = {
#                 'form' : form
#             }
#             return render(request, 'addproduct.html', context)
#     else:
#         form = Productform(request.POST,request.FILES)
#         context = {
#                 'form' : form
#             }
#         return render(request, 'addproduct.html', context)


# def salesReport(request):
#     orderpro = Order.objects.all()
#     context = {
#         'orderpro' : orderpro 
#     }
#     return render(request,'salesreport.html',context)





def salesReport(request):
    print("Im innnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
    
    global orderpro
    orderpro = Order.objects.all()
    yr = []
    ag = 2000
    months = ['January', 'February', 'March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for i in range(0,51):
        yr.append(ag + i)
    if request.method == 'POST':
        datestr = request.POST.get('daterange')
        print(datestr,"########################")
            #start date
        mo = datestr[:2]
        da = datestr[3:5]
        ye = datestr[6:10]
        #enddate
        mo1 = datestr[13:15]
        da1 = datestr[16:18]
        ye1 = datestr[19:]
        from_date = ye+'-'+mo+'-'+da
        to_date = ye1+'-'+mo1+'-'+da1

    
        year = request.POST.get('year')
        print(year,"///////////////////////////////")
        month = request.POST.get('month')
        print(month)
        print(month,"?????????????????????????????????")
        m = month
        yrr=year
        
        print(m)
  
        if  month != '' :
            orderpro = Order.objects.filter(created_at__month=m).order_by('created_at')
        elif  year != '' :
            orderpro = Order.objects.filter(created_at__year=yrr).order_by('created_at')
        elif from_date != '' and to_date != '' :
            order_data = Order.objects.filter(created_at__range=[from_date,to_date]).order_by('created_at')

    context = {'orderpro': orderpro, 'years': yr,'months':months,'sales':'sales'}
    return render(request,'salesreport.html', context)












def export_csv(request):
    order_data = OrderProduct.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ShopifyOrder'+'.csv'
    writer = csv.writer(response)   
    writer.writerow(['Order No','Name','Number Of Products','Order Date','Amount','Payment Type'])
    for data in order_data:
        writer.writerow([data.order.order_number, data.user.username, data.quantity,data.created_at, data.payment.amount_paid,data.payment.payment_method])
    return response
    

def export_excel(request):
    order_data = OrderProduct.objects.all()
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ShopifyOrder'+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Order No','Name','Number Of Products','Order Date','Amount','Payment Type']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)

    font_style = xlwt.XFStyle()

    rows = order_data.values_list(
        'order__order_number','user__username','quantity','created_at','payment__amount_paid','payment__payment_method'
    )
    
    for row in rows:
        row_num = row_num + 1

        for col_num in range(len(columns)):
             ws.write(row_num,col_num,str(row[col_num]),font_style)
    wb.save(response)

    return response


def displaycatoffer(request):
    coupon = CategoryOffer.objects.all()
    paginator = Paginator (coupon, 3)
    page = request.GET.get('page')
    paged_coupon = paginator.get_page(page)
    context = {
        'coupon' : paged_coupon
    }
    return render(request,'displaycatoffer.html',context)



def addcatoffer(request):
    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            catoff = form.save()
            messages.success(request,"Category offer created succesffully")
            return redirect('displaycatoffer')
        else:
            form = CategoryOfferForm(request.POST)
            context = {
                'form' : form
            }
            return render(request,'addcatoffer.html',context)
    else:
        form = CategoryOfferForm(request.POST)
        context = {
            'form' : form
        }
        return render(request,'addcatoffer.html',context)



def editcatoffer(request,id):
    context = {}
    obj = CategoryOffer.objects.get(id=id)
    form = EditCouponCatForm(instance = obj)
    if request.method == 'POST':
        form = EditCouponCatForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect("displaycatoffer")
        else:
            messages.error(request,'Form is not valid')
    context['form'] = form
    return render(request,'editcatform.html',context)

# def deletecoupon(request,id):
#     obj = CouponCode.objects.get(id=id)
#     obj.delete()
#     return redirect('displaycoupon')

def deletecatoffer(request,id):
    obj = CategoryOffer.objects.get(id=id)
    obj.delete()
    return redirect("displaycatoffer")


def displayprooffer(request):
    coupon = ProductOffer.objects.all()
    context = {
        'coupon' : coupon
    }
    return render(request,'displayprooffer.html',context)


def editprooffer(request,id):
    context = {}
    obj = ProductOffer.objects.get(id=id)
    form = EditProductOffer(instance = obj)
    if request.method == 'POST':
        form = EditProductOffer(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return redirect('displayprooffer')
        else:
            messages.error(request,'Form is not valid')
    context['form'] = form 
    return render(request, 'editprooffer.html',context)


# def deletecatoffer(request,id):
#     obj = CategoryOffer.objects.get(id=id)
#     obj.delete()
#     return redirect("displaycatoffer")



def deleteprooffer(request,id):
    obj = ProductOffer.objects.get(id=id)
    obj.delete()
    return redirect('displayprooffer')



def orderdetail(request,id):
    order = Order.objects.get(id=id)
    items = order.orderproduct_set.all()
    context = {
        'order' : order,
        'items' : items
    }

    return render(request,'order-detail.html',context)





    


    


