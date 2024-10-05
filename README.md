# Pizza-Paradise

Pizza Paradise is a Django-based web application that allows users to easily order customizable pizzas through a user-friendly interface. The system features user authentication, form handling, and data validation, with BootStrap for visually appealing design. Customers can create accounts, view their past orders, and place new orders with a wide selection of pizza sizes, crusts, sauces, cheeses, and toppings.

## Features
- **User Authentication**: Users can create an account, log in, and view their order history.
- **Custom Pizza Creation**: Users can customize their pizza by selecting the size, crust, sauce, cheese, and a variety of toppings.
- **Order Confirmation**: Upon placing an order, users are redirected to a page displaying their order details, including the pizza specifications, delivery address, and expected delivery time.
- **Form Validation**: Ensures all fields are completed correctly, including payment details such as card number, expiration date, and CVV.
- **Admin Functionality**: Admins can manage pizza options, such as adding new sizes, cheeses, sauces, and more via the Django admin interface.

## Getting Started

### Prerequisites:
- Python 3.x
- Django

### Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/PjayEvangelio/Pizza-Paradise.git

2. Navigate to the project directory:
   ```bash
   cd Pizza-Paradise

3. Run the Django development server:
   ```bash
   python3 manage.py runserver

4. Access the application by visiting:
   ```bash
   http://127.0.0.1:8000

### SuperUser Account for Admin Access:

NOTE: There is already a superuser set up for the Django admin interface. You can use the following credentials to log in:
  - Email: pjay.evangelio@gmail.com
  - Password: pjayisthebest123

Navigate to the Django admin page to add new pizza sizes, cheeses, sauces, etc.
```bash
http://127.0.0.1:8000/admin
```

## Project Stewardship
- Head Maintainer: Patrick John Evangelio

## Getting Assitance
If you run into any challenges or have inquiries regarding this project, you can:
- Create an issue in the [GitHub Issues](https://github.com/PjayEvangelio/Pizza-Paradise/issues) section.
- Contact the Head Maintainer (me) directly via email for support.

## References

### Acknowledgements:
A huge thanks to [Dr. Michael Scriney](https://www.dcu.ie/computing/people/michael-scriney) for guiding the development of this pizza ordering system.
