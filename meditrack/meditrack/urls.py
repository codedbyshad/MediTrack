"""
URL configuration for meditrack project.

The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path
from app1 import views

# ----------------------------
# URL Patterns for the Project
# ----------------------------
urlpatterns = [
path('admin/', admin.site.urls),
    path('', views.home),
    path('login', views.login),
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('addmedicine', views.add_medicine),
    path('addsales', views.add_sales, name='add_sales'),  # add a name here too
    path('savesale/', views.save_sale, name='save_sale'),  # this fixes the error
    path('logout', views.logout),
    path('sale_invoice/<int:sale_id>/', views.sale_invoice, name='sale_invoice'),
    path('viewsales/', views.view_sales, name='view_sales'),
    path('delete_sale/<int:sale_id>/', views.delete_sale, name='delete_sale'),










]
