from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'restaurant/main.html')

import random
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.urls import reverse
import random

from django.shortcuts import render, redirect
from django.urls import reverse
import random

def order(request):
    menu = {
        'Pizza': 10.00,
        'Burger': 8.50,
        'Pasta': 12.00,
        'Salad': 7.00
    }
    daily_special = random.choice(list(menu.items()))

    if request.method == 'POST':
        # Get selected items
        selected_items = request.POST.getlist('menu_items')
        
        # Store both item names and prices
        ordered_items = []
        total_price = 0
        for item in selected_items:
            item_price = menu[item]  # Get price for each item
            ordered_items.append({'name': item, 'price': item_price})
            total_price += item_price
        
        # Store order data in session
        order_data = {
            'name': request.POST.get('name'),
            'phone': request.POST.get('phone'),
            'email': request.POST.get('email'),
            'menu_items': ordered_items,  # Store items with prices
            'instructions': request.POST.get('instructions'),
            'total_price': total_price  # Store total price
        }
        request.session['order_data'] = order_data
        
        # Redirect to confirmation page
        return redirect('confirmation')

    context = {'menu': menu, 'daily_special': daily_special}
    return render(request, 'restaurant/order.html', context)

from django.shortcuts import render
import random
import time

def confirmation(request):
    # Retrieve order data from the session
    order_data = request.session.get('order_data', {})

    # Calculate a random ready time (30-60 minutes from now)
    ready_time = time.time() + random.randint(30, 60) * 60
    ready_time_str = time.strftime('%H:%M:%S', time.localtime(ready_time))

    context = {
        'name': order_data.get('name'),
        'phone': order_data.get('phone'),
        'email': order_data.get('email'),
        'menu_items': order_data.get('menu_items', []),  # Get ordered items
        'instructions': order_data.get('instructions'),
        'total_price': order_data.get('total_price', 0),  # Get total price
        'ready_time': ready_time_str
    }

    return render(request, 'restaurant/confirmation.html', context)

