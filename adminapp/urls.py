from django import views
from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.adminpage,name="adminpage"),
    path('addproduct/',views.addproduct,name="addproduct"),
    path('getproduct/',views.getproduct,name="getproduct"),
    path('editproduct/<str:id>',views.editproduct,name="editproduct"),
    path('deleteproduct/<str:id>',views.deleteproduct,name="deleteproduct"),
    path('getusers/',views.getusers,name="getusers"),
    path('blockuser/<str:id>',views.blockuser,name="blockuser"),
    path('addcategory/',views.addcategory,name="addcategory"),
    path('getcategory/',views.getcategory,name="getcategory"),
    path('deletecategory/<str:id>',views.deletecategory,name="deletecategory"),
    path('adminlogin',views.adminlogin,name="adminlogin"),
    path('adminlogout',views.adminlogout,name="adminlogout"),
    path('displayorderadmin/',views.displayorderadmin,name="displayorderadmin"),
    path('editorderadmin/<int:id>/',views.editorderadmin,name="editorderadmin"),
    path('statusOrder/<int:id>',views.statusOrder,name="statusOrder"),
    path('salesReport',views.salesReport,name="salesReport"),
    path('export_csv',views.export_csv,name="export_csv"),
    path('export_excel',views.export_excel,name="export_excel"),
    # path('chart/',views.chart,name="chart"),
    path('displaycoupon/',views.displaycoupon,name="displaycoupon"),
    path('addCoupon/',views.addCoupon,name="addCoupon"),
     path('editcoupon/<str:id>',views.editcoupon,name="editcoupon"),
     path('deletecoupon/<str:id>',views.deletecoupon,name="deletecoupon"),
     path('displaycatoffer/',views.displaycatoffer,name="displaycatoffer"),
     path('addcatoffer/',views.addcatoffer,name="addcatoffer"),
     path('editcatoffer/<str:id>',views.editcatoffer,name="editcatoffer"),
     path('deletecatoffer/<str:id>',views.deletecatoffer,name="deletecatoffer"),
     path('displayprooffer/',views.displayprooffer,name="displayprooffer"),
     path('editprooffer/<str:id>',views.editprooffer,name="editprooffer"),
     path('deleteprooffer/<str:id>',views.deleteprooffer,name="deleteprooffer"),
     path('orderdetail/<str:id>',views.orderdetail,name="orderdetail"),
]