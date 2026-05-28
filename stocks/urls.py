from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('create/', views.stock_create, name='stock_create'),
    path('<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('<int:pk>/delete/', views.stock_delete, name='stock_delete'),

]
