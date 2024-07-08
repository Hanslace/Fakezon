from store.models import Category , Cart

def extras(request):
    categories = Category.objects.all()
    if request.user.is_authenticated and request.user.is_customer:
        cart = 	Cart.objects.get(customer = request.user )
    else:
        cart = {}
    return {'categories' : categories , 'cart' : cart}

