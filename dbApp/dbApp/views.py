from django.http import HttpResponse
import mysql.connector

from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def index(request):
    if request.method == 'POST':
        # Handle login form submission
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, email=email, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                # Redirect to superuser-specific page
                template = loader.get_template('dbApp/admin_dashboard.html')
                context = {}
                return HttpResponse(template.render(context, request))
            else:
                # Redirect to regular user dashboard or wherever you want
                return redirect('user_dashboard')
        else:
            # Authentication failed, return error message
            context = {'error': 'Invalid username or password'}
            return render(request, 'dbApp/login.html', context)
    else:
        # Render the login form
        template = loader.get_template('dbApp/login.html')
        context = {}
        return HttpResponse(template.render(context, request))

def admin_dashboard_view(request):
    template = loader.get_template('dbApp/admin_dashboard.html')
    context = {}

    return HttpResponse(template.render(context, request))