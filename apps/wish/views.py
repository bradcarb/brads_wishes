# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib import messages
from .models import User, Product, UserManager, ProductManager

def index(request):
    return render(request, 'wish/index.html')

def login(request):
    result = User.objects.login(request.POST)
    if result[0]:
        request.session['user_id'] = result[1].id    
        # id = str(request.session['id'])
        return redirect("/home")
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
    return redirect('/')

def registration(request):
    return render(request, 'wish/registration.html')

def validate_registration(request):
    result = User.objects.validate_registration(request.POST)
    if result[0]:
        request.session['user_id'] = result[1].id    
        # id = str(request.session['id'])
        return redirect("/home")
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
    return redirect('/registration')

def home(request):
    print request.session['user_id']
    if request.session['user_id'] != 0:
        user = User.objects.get(id=request.session['user_id'])
        all_products = Product.objects.all()
        my_wishlist = Product.objects.filter(wishers = user)
        other_products = all_products.exclude(wishers = user)
        context = {
            'user' : user,
            'all_products' : all_products,
            'my_wishlist' : my_wishlist,
            'other_products' : other_products
        }    
        return render(request,'wish/home.html', context)
    return redirect('/index')

def product(request, product_id):
    print request.session['user_id']
    product = Product.objects.get(id=product_id)
    wishers = Product.objects.get(id=product_id).wishers.all()
    context = {
        'product' : product,
        'wishers' : wishers
    }
    return render(request, 'wish/product.html', context)

def validate_product(request):
    print request.session['user_id']
    id = request.session['user_id']
    result = Product.objects.validateProduct(request.POST, id)
    if result[0]:
        return redirect("/home")
    else:
        for error in result[1]:
            messages.add_message(request, messages.INFO, error)
    return redirect('/add_product')

def add_product(request):
    return render(request, 'wish/add_product.html')

def join(request, product_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_product = Product.objects.get(id = product_id)
    this_user.wished.add(this_product)

    return redirect('/home')

def delete(request, product_id):
    this_product = Product.objects.get(id = product_id)
    this_product.delete()
    return redirect('/home')

def remove(request, product_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_product = Product.objects.get(id = product_id)
    this_user.wished.remove(this_product)
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')
