from django.http import HttpResponse
import mysql.connector

from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

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
                # Check if user belongs to instructor or student group
                if Group.objects.filter(user=user, name='instructors').exists():
                    # Redirect to instructor dashboard
                    template = loader.get_template('dbApp/instructor_dashboard.html')
                    context = {}
                    return HttpResponse(template.render(context, request))
                elif Group.objects.filter(user=user, name='students').exists():
                    # Redirect to student dashboard
                    template = loader.get_template('dbApp/student_dashboard.html')
                    context = {}
                    return HttpResponse(template.render(context, request))
                else:
                    template = loader.get_template('dbApp/login.html')
                    context = {'error': 'Invalid username or password'}
                    return HttpResponse(template.render(context, request))
    else:
        # Render the login form
        template = loader.get_template('dbApp/login.html')
        context = {}
        return HttpResponse(template.render(context, request))

def admin_dashboard_view(request):
    template = loader.get_template('dbApp/admin_dashboard.html')
    context = {}

    return HttpResponse(template.render(context, request))

def instructor_dashboard_view(request):
    template = loader.get_template('dbApp/instructor_dashboard.html')
    context = {}

    return HttpResponse(template.render(context, request))

def student_dashboard_view(request):
    template = loader.get_template('dbApp/student_dashboard.html')
    context = {}

    return HttpResponse(template.render(context, request))