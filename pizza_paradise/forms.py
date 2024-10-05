from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction
from django.core import validators
from django.core.exceptions import ValidationError
from datetime import date, datetime
from django.utils.dateparse import parse_date


# Class & function for creating a new user
class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['username']
        user.save()
        return user
    

# Class for logging in an already existing user
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

# Class for making the pizza form for the user to complete
class UserPizzaForm(forms.ModelForm):
    class Meta:
            model = Pizza
            fields = ['size', 'crust', 'sauce', 'cheese', 'pepperoni', 'chicken', 'ham', 'pineapple', 'peppers', 'mushrooms', 'onions']

# Class for making the delivery form for the user to complete
class UserDeliveryForm(forms.ModelForm):
    class Meta:
            model = Order
            fields = ['name', 'delivery_address', 'card_number', 'card_expiry_date', 'card_cvv']

    # Validation error checks
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) == 0:
            raise ValidationError("Name cannot be empty.")
        return name

    def clean_delivery_address(self):
        delivery_address = self.cleaned_data['delivery_address']
        if len(delivery_address.strip()) == 0:
            raise ValidationError("Delivery address cannot be empty.")
        return delivery_address

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.isdigit():
            raise ValidationError("Card number must contain only digits.")
        if len(card_number) != 16:
            raise ValidationError("Card number must be 16 digits long.")
        return card_number

    def clean_card_expiry_date(self):
        card_expiry_date = self.cleaned_data['card_expiry_date']
        today = datetime.now().date()

        try:
            # Split the date string into month and year
            month_str, year_str = card_expiry_date.split('/')
        
            # Check if month and year contain only digits
            if not (month_str.isdigit() and year_str.isdigit()):
                raise ValidationError("(MM/YY) fields must contain only digits.")

            month = int(month_str)
            year = int(year_str)

            # Check if month and year have length of 2
            if len(month_str) != 2 or len(year_str) != 2:
                raise ValidationError("Enter a valid expiration date (MM/YY).")

            # Check if month is between 1 and 12
            if not (1 <= month <= 12):
                raise ValidationError("Month field must be between 1 and 12.")

            current_year = today.year % 100
            current_month = today.month
            # Check if the card expiry year is in the past
            if year < current_year or (year == current_year and month < current_month):
                raise ValidationError("Card expiration date has already passed.")

        except ValueError:
            raise ValidationError("Enter a valid expiration date (MM/YY).")

        return card_expiry_date

    def clean_card_cvv(self):
        card_cvv = self.cleaned_data['card_cvv']
        if not card_cvv.isdigit():
            raise ValidationError("CVV must contain only digits.")
        if len(card_cvv) != 3:
            raise ValidationError("CVV must be 3 digits long.")
        return card_cvv

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data