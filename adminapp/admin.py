from django.contrib import admin

from adminapp.models import *

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display        = ('category_name','slug',)



admin.site.register(Userreg)
admin.site.register(Product)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Cart)
admin.site.register(Cart_Item)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(CouponCode)
admin.site.register(WishCart)
admin.site.register(Wishlist)
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(BannerUpdate)
