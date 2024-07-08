from django.contrib import admin

from .models import Category ,  Product ,Order , CartItem , Cart , Wishlist   , Profile  , CustomUser

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Wishlist)

