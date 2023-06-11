
from django.urls import path
from oursite import views
from oursite.views import *

urlpatterns = [
    path('', index, name='home'),
    path('restaurants/', views.restaurants, name='restaurants'),
    path('restaurants/<slug:rest_slug>/', views.show_rest, name='restaurant'),
    path('registration', views.Register.as_view(), name='login'),
    path('authorization', views.Login.as_view(), name='auth'),
    path('update', views.update_data, ),
    path('logout', views.logout_user),
    path('add-to-cart/', views.add_to_cart, name='cart'),
    path('get-cart/', views.get_cart, name='get_cart'),
    path('remove-all/', views.remove_all),
    path('order/', views.order),
    path('confirm-order/', views.successful_order, name='successful_order'),
    path('get-locations/', views.locations, ),
    path('update-location/', views.update_location, ),
    path('get-orders/', views.orders, ),
]
