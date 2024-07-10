from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import re
from .models import *
from .forms import   *
from django.contrib.auth.decorators import login_required
from .Signal import *
from .decoraters import *



	

	
def home(request , products = None):
	if products == None:
		products = Product.objects.all()
	query = request.GET.get('q')
	if query:
		products = products.filter(name__icontains=query)
	if request.user.is_authenticated:
		if hasattr(request.user, 'is_customer') and request.user.is_customer:
			return redirect('customer_home')
		elif hasattr(request.user, 'is_seller') and request.user.is_seller:
			return redirect('seller_home')
	return render(request, 'home.html', {'products':products})


def about(request):
    return render(request , 'about.html' , {})


@unauthenticated_user
def login_user(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				if hasattr(user, 'is_customer') and user.is_customer:
					return redirect('customer_home')
				elif hasattr(user, 'is_seller') and user.is_seller:
					return redirect('seller_home')
				else:
					return redirect('home')  
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form})

@authenticated_user
def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')


@authenticated_user
def product(request,pk):
	product = Product.objects.get(productID=pk)
	try :
		CartItem.objects.get(cart = request.user.cart , product = product )
		in_cart =True 
	except:
		in_cart = False
	return render(request, 'product.html', {'product':product ,'in_cart' :in_cart})


def category(request, foo):
	category = Category.objects.get(categoryName=foo)
	products = Product.objects.filter(category=category)
	return redirect('home.html', products)

@authenticated_user
def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
	
		form = UserInfoForm(request.POST or None, instance=current_user)

		if form.is_valid() :
			# Save original form
			form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')
	
@authenticated_user
def update_user(request):
	if request.user.is_authenticated:
		current_user = CustomUser.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')
	
@authenticated_user
def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

@unauthenticated_user
def customer_register(request):

	if request.method == 'POST':
		form = CustomerRegistrationForm(request.POST)
		if form.is_valid():
				user = form.save()
				login(request, user)
				messages.success(request, ("Customer Registered - Please Fill Out Your User Info Below..."))
				return redirect('update_info')	
	else:
				form = CustomerRegistrationForm()
	return render(request, 'register.html', {'form': form})
	

@unauthenticated_user
def seller_register(request):
	if request.method == 'POST':
				form = SellerRegistrationForm(request.POST)
				if form.is_valid():
					user = form.save()
					login(request, user)
					messages.success(request, ("Seller Registered - Please Fill Out Your User Info Below..."))
					return redirect('update_info')	
	else:
		form = SellerRegistrationForm()
	return render(request, 'register.html', {'form': form})
	
@login_required
def customer_home(request):
	if not request.user.is_customer:
		return redirect('home')
	products = Product.objects.all()
	query = request.GET.get('q')
	if query:
		products = products.filter(name__icontains=query)
	return render(request, 'customer_home.html' , {'products' : products})

@login_required
def seller_home(request):
	if not request.user.is_seller:
		return redirect('home')
	products = Product.objects.filter(seller = request.user)
	query = request.GET.get('q')
	if query:
		products = products.filter(name__icontains=query,seller = request.user)
	seller = Profile.objects.get(user = request.user )
	return render(request, 'seller_home.html' , {'seller' : seller , 'products' : products})

@authenticated_seller
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES ,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('seller_home') 
    else:
        form = ProductForm(user=request.user)
    return render(request, 'create_product.html', {'form': form})
@authenticated_seller
def delete_product(request, pk):

	product = Product.objects.get(productID=pk)
	name= product.name
	product.delete()
	products = Product.objects.filter(seller=request.user)
	messages.success(request, (f"Product: {name} has been deleted."))
	return render(request, 'seller_home.html', {'products':products})

@authenticated_seller
def update_product(request, pk ):


	product = Product.objects.get(productID=pk)
	product_form = UpdateProductForm(request.POST or None, instance=product)

	if product_form.is_valid():
		product_form.save()


		messages.success(request, f"Product: {product} Has Been Updated!!")
		return redirect('seller_home')
	return render(request, "update_product.html", {'product_form':product_form , 'product':product})

@authenticated_customer
def wishlist(request):

	products = Product.objects.filter(wishlisted=request.user.wishlist)
	return render(request, 'wishlist.html', {'products':products})

@authenticated_customer
def remove_from_wishlist(request, pk):
	product = Product.objects.get(productID=pk)
	product.wishlisted.remove(request.user.wishlist)
	messages.success(request, (f"Product: {product.name} has been removed from wishlist."))
	return redirect('product' , pk)

@authenticated_customer
def add_to_wishlist(request , pk):
	product = Product.objects.get(productID=pk)
	product.wishlisted.add(request.user.wishlist)
	messages.success(request, (f"Product: {product.name} has been Added to wishlist."))
	return redirect('product' , pk)

@authenticated_customer
def cart(request):
	cartitems = CartItem.objects.filter(cart = request.user.cart)
	total_cost = sum( item.quantity * item.product.price for item in cartitems)
	products = CartItem.objects.filter(cart = request.user.cart)
	return render(request, 'cart.html', {'products':products , 'total_cost' : total_cost})

@authenticated_customer
def orders(request):

	products = Order.objects.filter(customer = request.user)
	return render(request, 'orders.html', {'products':products})

@authenticated_customer
def add_to_cart(request , pk):

	product = Product.objects.get(productID=pk)
	

	if request.method == 'POST':
		form = CartForm(request.POST, request.FILES ,cart=request.user.cart , product = product)
		if form.is_valid():
			form.save()
			messages.success(request, (f"Product: {product.name} has been Added to cart."))
			return redirect('product' , pk)
	else:
		form = CartForm(cart=request.user.cart , product = product)
	return render(request, "get_quantity.html", {'form':form , 'product' : product})


		
@authenticated_customer
def remove_from_cart(request , pk):
	product = Product.objects.get(productID=pk)

	item = CartItem.objects.get(cart=request.user.cart , product = product)
	item.delete()
	messages.success(request, (f"Product: {product.name} has been removed from cart."))
	return redirect('product' , pk)
	
@authenticated_user
def cartitem(request,pk):
	product = Product.objects.get(productID=pk)
	item = CartItem.objects.get(cart = request.user.cart  , product = product )
	try :
		CartItem.objects.get(cart = request.user.cart , product = product )
		in_cart =True 
	except:
		in_cart = False
	return render(request, 'cartitem.html', {'product':item ,'in_cart' :in_cart})

@authenticated_customer
def checkout(request):
	items = CartItem.objects.filter(cart = request.user.cart)
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			paymentMethod = form.cleaned_data['paymentMethod']
			address = form.cleaned_data['address']

		for item in items:
			if item.quantity < item.product.stock :
				item.product.stock -= item.quantity
				item.product.sales += item.quantity
				Order.objects.create(product = item.product ,paymentMethod = paymentMethod ,cost = item.calc_cost , customer = request.user, address = address , quantity = item.quantity)
				item.delete()
		
		messages.success(request, (f"Thanks for shopping with us!!"))
		return redirect('customer_home')
	else:
		form = OrderForm()
	return render(request, 'orderinfo.html', {'form': form})

@authenticated_customer
def order(request,pk):
	order = Order.objects.get(orderID=pk)

	return render(request, 'order.html', {'product':order })

@authenticated_customer
def rate(request , pk ):
	order = Order.objects.get(orderID=pk)
	product = order.product
	quantity = order.quantity
	if request.method == 'POST':
		form = RatingForm(request.POST)
		if form.is_valid():
			rating = form.cleaned_data['rating']
			

		product.rating = round(((rating*quantity) + (product.rating*(product.sales - quantity)))/product.sales , 2)
		
		messages.success(request, (f"Thanks for your feedback!!"))
		return redirect('order' , pk)
	else:
		form = RatingForm()
	return render(request, 'rate.html', {'form': form , 'ID':pk})