from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from catalogue.models import Category, Product
from collections import defaultdict

from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout

from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
from .models import Subscriber


def home(request):
    return render( request,'index.html')

def about(request):
    return render( request,'about.html')

def contact(request):
    return render( request,'contact.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('authentication:home')  # Redirect to a home or dashboard page after login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('authentication:home')

def useradmin(request):
    if request.method == 'POST':
        if 'add_category' in request.POST:
            # Handle category addition
            name = request.POST.get('cat_name')

            
            if name:
                Category.objects.create(
                    cat_name = name,
                )
                messages.success(request, 'Category successfully added!')
                return redirect('authentication:useradmin')
                
            else:
                messages.error(request, 'Category name is required.')
                return redirect('authentication:useradmin')

        
        elif 'add_product' in request.POST:
            # Handle product addition
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            category_id = request.POST.get('category')
            image = request.FILES.get('image')
            if product_name and price:
                category = Category.objects.get(id=category_id)
                Product.objects.create(
                    product_name=product_name,
                    description=description,
                    price=price,
                    stock=stock,
                    category=category,
                    images=image
                )
            messages.success(request, 'Product successfully added!')
            return redirect('authentication:useradmin')

    else:
        
        categories = Category.objects.all()
        context =  { 'categories': categories }
        return render(request, 'useradmin.html', context)
    

def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Basic validation
        if not name or not email:
            messages.error(request, "Please provide both name and email.")
            return render( request,'index.html')
        
        # Validate email format
        from django.core.validators import validate_email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render( request,'index.html')
        
        # Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, "This email is already subscribed.")
            return render( request,'index.html')
        
        # Save subscriber
        Subscriber.objects.create(name=name, email=email)
        messages.success(request, "Thank you for subscribing!")
        return render( request,'index.html')

    return render( request,'index.html')
