from django.conf.urls import url, include
from . import views

urlpatterns = [  
    url(r'^$', views.index),
    url(r'^login', views.login),
    url(r'^delete/(?P<product_id>\d+)', views.delete),
    url(r'^remove/(?P<product_id>\d+)', views.remove),
    url(r'^registration', views.registration),
    url(r'^validate_registration', views.validate_registration),
    url(r'^home', views.home),
    url(r'^add_product', views.add_product),
    url(r'^validate_product', views.validate_product),
    url(r'^product/(?P<product_id>\d+)', views.product),
    url(r'^logout', views.logout),
    url(r'^join/(?P<product_id>\d+)', views.join)

]