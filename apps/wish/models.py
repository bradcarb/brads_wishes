# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_registration(self, POST):
        errors=[]
        if len(POST['name']) == 0:
            errors.append('Name is a required field')
        elif len(POST['name']) < 3:
            errors.append('Name must have at least three characters')
        if len(POST['username']) == 0:
            errors.append('Username is a required field')
        elif len(POST['name']) < 3:
            errors.append('Username must have at least three characters')
        elif len(User.objects.filter(username=POST['username'])) != 0:
            errors.append('Username is already in use')
        if len(POST['email']) == 0:
            errors.append('Email is a required field')
        elif not re.match(EMAIL_REGEX, POST['email']):
            errors.append('Please enter a valid email address')
        elif len(User.objects.filter(email=POST['email'])) != 0:
            errors.append('Email is already in use')
        if len(POST['password']) == 0:
            errors.append('Password is a required field')
        elif len(POST['password']) < 8:
            errors.append('Password must have at least eight characters')
        elif POST['password'] != POST['confirm_password']:
            errors.append('Passwords do not match')
        if len(errors) > 0:
            print "false"
            return (False, errors)

        else:
            pwhash = bcrypt.hashpw((POST['password'].encode()), bcrypt.gensalt(5))

            new_user = User.objects.create(
                name = POST['name'],
                username = POST['username'],
                email = POST['email'],
                password = pwhash
            )        
            return (True, new_user)


    def login(self, POST):
        errors = []
        if len(POST['email']) == 0:
            errors.append('Please enter a valid email address')
        elif not re.match(EMAIL_REGEX, POST['email']):
            errors.append('Please enter a valid email address')
        if len(POST['password']) == 0:
            errors.append('Password must be entered')
        elif len(self.filter(email=POST['email'])) != 0:
            user = self.filter(email=POST['email'])[0]
            if not bcrypt.checkpw(POST['password'].encode(), user.password.encode()):
                errors.append('Email/Password combination invalid')
        else: 
            errors.append('Email/Password combination invalid')
        if len(errors) > 0:
            return (False, errors)
        return (True, user)

class ProductManager(models.Manager):
    def validateProduct(self, POST, id):

        errors = []
        if len(POST['name']) == 0:
            errors.append('Name is required')
        elif len(POST['name']) < 4:
            errors.append('Name must be at least four characters')

        if len(errors) > 0:
            return (False, errors)
        else:
            new_product = Product.objects.create(
                name = POST['name'],
                created_by = User.objects.get(id=id),
            )        
            
        return (True, new_product)

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateField(null=True)
    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)  
    objects = ProductManager()
    created_by = models.ForeignKey(User, related_name="user_products")
    wishers = models.ManyToManyField(User, related_name="wished")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "Product name:" + ' ' + self.name + "Wishers:" + ' ' + self.wishers