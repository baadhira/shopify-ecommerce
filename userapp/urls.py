from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    
    path('',views.userpage,name='userpage'),
    path('signup/',views.usersignup,name='usersignup'),
    path('userotp/',views.userotp,name='userotp'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('userproductdetails/<str:id>',views.userproductdetails,name='userproductdetails'),
    path('userprofilehome/',views.userprofilehome,name='userprofilehome'),
    path('edituserprofile/',views.edituserprofile,name='edituserprofile'),
    # path('updateItem/',views.updateItem,name='updateItem'),
    path('add_cart_ajax/',views.add_cart_ajax,name='add_cart_ajax'),
    path('cart/',views.cart,name='cart'),
    path('add_cart/<str:id>',views.add_cart,name='add_cart'),
    path('remove_cart_ajax/',views.remove_cart_ajax,name='remove_cart_ajax'),
    path('remove_cart_item/',views.remove_cart_item,name='remove_cart_item'),
    path('addaddress/',views.addaddress,name='addaddress'),
    path('getaddress/',views.getaddress,name='getaddress'),
    path('checkout/',views.checkout,name='checkout'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart, name='remove_cart'),
    path('codorder/<int:order_number>',views.codorder,name='codorder'),
    path('paypalpayment/',views.paypalpayment,name='paypalpayment'),
    path('filterview/<str:id>',views.filterview,name='FilterView'),
    path('razorpayment/<int:order_number>',views.razorpayment,name='razorpayment'),
    path('userorderlist/',views.userorderlist,name='userorderlist'),
    path('razorpayment/',views.razorpayment,name='razorpayment'),
    path('razorpayorder/',views.razorpayorder,name='razorpayorder'),
    path('cancel_order/<str:id>',views.cancel_order,name='cancel_order'),
    path('return_order/<str:id>',views.return_order,name='return_order'),
    path('ClaimCoupon/',views.ClaimCoupon,name='ClaimCoupon'),
    path('verifyCoupon/',views.verifyCoupon,name='verifyCoupon'),
    path('userproductgrid/',views.userproductgrid,name='userproductgrid'),
    path('contacts/',views.contacts,name='contacts'),
    path('hightolow/',views.hightolow,name='hightolow'),
    path('lowtohigh/',views.lowtohigh,name='lowtohigh'),

   
    path('user_order_return/',views.user_order_return,name='user_order_return'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('remove_wish_item/',views.remove_wish_item, name='remove_wish_item'),
    path('ordersuccess/',views.ordersuccess, name='ordersuccess'),
    path('add_wishlist/',views.add_wishlist,name='add_wishlist'),
    path('search/',views.search,name='search'),
]