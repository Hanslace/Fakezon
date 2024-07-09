from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

def authenticated_user(view_func):
    def wrapper_func(request , *args, **kwargs):
        if request.user.is_authenticated:
            
            return view_func(request , *args , **kwargs)
        else:
            messages.success(request, ("You to be a logged in user to see this !!"))
            return redirect('home')
    return wrapper_func

def unauthenticated_user(view_func):
    def wrapper_func(request , *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, ("You to be logged out to see this !!"))
            return redirect('home')
        else:
            
            return view_func(request , *args , **kwargs)
    return wrapper_func


def authenticated_seller(view_func):
    def wrapper_func(request , *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
           return view_func(request , *args , **kwargs)
        else:
            messages.success(request, ("You to be a logged in seller to see this !!"))
            return redirect('home')
    return wrapper_func


def authenticated_customer(view_func):
    def wrapper_func(request , *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            
            return view_func(request , *args , **kwargs)
        else:
            messages.success(request, ("You to be a logged in customer to see this !!"))

            return redirect('home')
    return wrapper_func