from .forms import *
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('signup/', views.UserSignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('order_history/', views.show_order_history, name="order_history"),
    path('create_pizza/', views.createPizza, name="create_pizza"),
    path('delivery_details/<int:pid>/', views.deliveryDetails, name="delivery_details"),
    path('order_confirmation/', views.orderConfirmation, name="order_confirmation")
]
