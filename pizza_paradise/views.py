from .forms import *
from .models import *
from django.http import HttpResponse
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from datetime import timedelta
from operator import attrgetter


# Views function to redirect user to the homepage
def index(request):
    return render(request, 'index.html')

# Views function to redirect user to the about page upon clicking the link
def about(request):
    return render(request, 'about.html')

# Class & functions for creating a new user
class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/order_history/")


# Class for logging in an already existing user
class UserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = UserLoginForm   # Specify the custom login form


# Function for logging out an already existing user
@login_required
def logout_user(request):
    logout(request)
    return redirect("/")

# Function to check if an already existing user is currently logged in 
def some_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect("/order_history/")   # the user is logged in, do something
    else:
        # code to run if the user is not logged in
        # e.g. redirect them to the homepage 
        return redirect("/")
    

# Function to show the existing users' previous orders
@login_required
def show_order_history(request):
    # Check if the current user has any pizzas in the database
    has_pizzas = Pizza.objects.filter(user=request.user).exists()

    # Assuming Order model has a foreign key field named 'user' to link it to the User model
    orders = Order.objects.filter(user_id=request.user.id).order_by('placed_at')
    pizzas = Pizza.objects.filter(user_id=request.user.id).order_by('id')

    # Create lists to store order and pizza details
    order_details = list(orders)
    pizza_details = list(pizzas)

    # Zip the lists
    order_pizza_details = zip(order_details, pizza_details)

    return render(request, 'order_history.html', {'order_pizza_details': order_pizza_details, 'has_pizzas': has_pizzas})


# Function to create a new instance of the pizza class for the user
@login_required
def createPizza(request):
    if request.method == "POST":
        form = UserPizzaForm(request.POST)
        if form.is_valid():
            # If form is valid, save the form data to create a new Pizza instance
            pizza = form.save(commit=False)  # Use commit=False to create an unsaved instance
            # Assign the current user to the pizza
            pizza.user = request.user
            # Save the pizza instance to the database
            pizza.save()
            # Redirect to the delivery_details page with the pizza ID (pid) as parameter
            return redirect('delivery_details', pid=pizza.id)
        else:
            # Handle form errors
            return render(request, 'create_pizza.html', {'form': form})
    else:
        form = UserPizzaForm()
        return render(request, 'create_pizza.html', {'form': form})
    
    
# Function to redirect users to order confirmation page
@login_required
def deliveryDetails(request, pid):
    if request.method == "POST":
        form = UserDeliveryForm(request.POST)
        if form.is_valid():

            # If form is valid, save the form data to create a new Order instance
            order = form.save(commit=False)   # Use commit=False to create an unsaved instance
            pizza = get_object_or_404(Pizza, id=pid)
            order.pizza = pizza
            # Assign the current user to the order
            order.user = request.user
            
            # Save the order instance to the database
            order.save()
            # Redirect to the order_confirmation page 
            return redirect('order_confirmation')
        else:
            # Handle form errors
            return render(request, 'delivery_details.html', {'form': form, 'pid':pid})
    else:
        form = UserDeliveryForm()
        return render(request, 'delivery_details.html', {'form': form, 'pid':pid})


# Function to pass the user's pizza and order models into the order confirmation page
@login_required
def orderConfirmation(request):
    # Fetch the most recent pizza created by the current user
    latest_pizza = Pizza.objects.filter(user=request.user).latest('id')

    # Fetch the most recent order details filled in by the current user
    latest_order = Order.objects.filter(user=request.user).latest('id')

    # Calculate the expected delivery arrival time
    expected_delivery_time = latest_order.placed_at + timedelta(minutes=20)
    if latest_order.placed_at.hour >= 23 and latest_order.placed_at.minute >= 40:
        expected_delivery_time += timedelta(days=1)

    # Render the template with the provided context
    return render(request, 'order_confirmation.html', {'latest_pizza': latest_pizza, 'latest_order': latest_order, 'expected_delivery_time': expected_delivery_time})
