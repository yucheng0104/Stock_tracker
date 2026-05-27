from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('register/', views.register, name='register'),
    path('create/', views.stock_create, name='stock_create'),

]
