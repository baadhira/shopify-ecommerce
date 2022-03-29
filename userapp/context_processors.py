from .views import _cart_id, _wishcart_id
from adminapp.models import Cart,Cart_Item,Category,Wishlist


def counter(request):
    cart_count = 0

    if 'admin' in request.path:
        return {}
    else:
        try:
            cart        = Cart.objects.filter(cart_id = _cart_id(request))
            if request.user.is_authenticated:
                cart_items   = Cart_Item.objects.all().filter(user = request.user)
            else:
                cart_items   = Cart_Item.objects.all().filter(cart = cart [:1])
            # above query will return only one result

            # Now getting the quantity from cart_item (as the quantity is mentioned in the model)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)

def wish_list(request):
    if request.user.is_authenticated:
        wish_items = Wishlist.objects.filter(user = request.user).count()
        return{'wish_items': wish_items}
    else:
        return{'wish_items': 0}


def menu_links(request):
    links = Category.objects.all()
    return dict(links = links)