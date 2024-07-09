from django.urls import path 
from . import views
from .models import Product

urlpatterns = [
    path('' , views.home , name = 'home'),
    path('about/' , views.about , name = 'about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('update_info/', views.update_info, name='update_info'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_user/', views.update_user, name='update_user'),
    path('customer/register/', views.customer_register, name='customer_register'),
    path('seller/register/', views.seller_register, name='seller_register'),
    path('customer/home/', views.customer_home, name='customer_home'),
    path('seller/home/', views.seller_home, name='seller_home'),
    path('create_product/', views.create_product, name='create_product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
    path('update_product/<int:pk>', views.update_product, name='update_product'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:pk>', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_to_wishlist/<int:pk>', views.add_to_wishlist, name='add_to_wishlist'),
    path('cart/', views.cart, name='cart'),
    path('orders/', views.orders, name='orders'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('cartitem/<int:pk>', views.cartitem, name='cartitem'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:pk>', views.order, name='order'),
    path('rate/<Product:product>/<int:quantity>' , views.rate , name='rate')
]
