from django.http import HttpResponse
import mysql.connector
from .models import Instructor, Teaches, Takes, Funding, Papers, Students
from django.db.models import Min, Max, Avg, Sum
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        # Handle login form submission
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                template = loader.get_template('dbApp/admin_dashboard.html')
                context = {}
                return HttpResponse(template.render(context, request))
            else:
                if Group.objects.filter(user=user, name='instructors').exists():
                    template = loader.get_template('dbApp/instructor_dashboard.html')
                    context = {}
                    return HttpResponse(template.render(context, request))
                elif Group.objects.filter(user=user, name='students').exists():
                    template = loader.get_template('dbApp/student_dashboard.html')
                    context = {}
                    return HttpResponse(template.render(context, request))
        else:
            print("Invalid login attempt")
            messages.error(request, 'Invalid username or password.')
            template = loader.get_template('dbApp/login.html')
            context = {'error': True}
            return HttpResponse(template.render(context, request))
    else:
        # Render the login form
        template = loader.get_template('dbApp/login.html')
        context = {}
        return HttpResponse(template.render(context, request))

def admin_dashboard_view(request):
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'sort_instructors':
                sort_by = request.GET.get('sort_by')
                instructors = Instructor.objects.all().order_by(sort_by)
                context = {'instructors': instructors}
                template = loader.get_template('dbApp/admin_dashboard.html')
                return HttpResponse(template.render(context, request))
            elif action == 'sort_salary':
                sort_by = request.GET.get('sort_by')
                if sort_by == 'MIN':
                    instructors = Instructor.objects.values('dept_name').annotate(salary=Min('salary'))
                elif sort_by == 'MAX':
                    instructors = Instructor.objects.values('dept_name').annotate(salary=Max('salary'))
                elif sort_by == 'AVG':
                    instructors = Instructor.objects.values('dept_name').annotate(salary=Avg('salary'))
                else:
                    # Default behavior if sort_by is not recognized
                    instructors = Instructor.objects.all()

                instructors = instructors.order_by('-salary')
                context = {'salaries': instructors}
                template = loader.get_template('dbApp/admin_dashboard.html')
                return HttpResponse(template.render(context, request))
            elif action == 'performance':
                instructor_name = request.GET.get('instructor')
                instructor_semester = request.GET.get('semester')
                instructor_year = request.GET.get('year')
                print(instructor_name, instructor_semester, instructor_year)
                instructor = Instructor.objects.get(name=instructor_name)
                instructor_id = instructor.id
                instructor_performance = []
                # Query to get courses taught by the instructor in a specific semester and year
                courses_taught = Teaches.objects.values('teacher_id', 'course_id', 'sec_id', 'semester', 'year')
                courses_taught_filter = courses_taught.filter(teacher_id=instructor_id, semester=instructor_semester, year=instructor_year)
                courses_taught_filter_count = courses_taught.filter(teacher_id=instructor_id, semester=instructor_semester, year=instructor_year).count()
                enrollment_count = []
                for course in courses_taught_filter:
                    enrollment_count = Takes.objects.filter(course_id=course['course_id'], sec_id=course['sec_id'], semester=course['semester'], year=course['year']).count()

                instructor_funding = Funding.objects.values('name', 'semester', 'funding', 'year')
                instructor_funding_filter = instructor_funding.filter(name=instructor_name, year=instructor_year, semester = instructor_semester)
                instructor_funding_sum = instructor_funding_filter.aggregate(total_funding=Sum('funding'))
                total_funding_sum = instructor_funding_sum['total_funding'] if instructor_funding_sum['total_funding'] else 0

                instructor_papers = Papers.objects.values('name', 'semester', 'papers', 'years')
                print(instructor_papers)
                instructor_papers_filter = instructor_papers.filter(name=instructor_name, years=instructor_year, semester = instructor_semester)
                print(instructor_papers_filter)
                instructor_papers_sum = instructor_papers_filter.aggregate(total_papers=Sum('papers'))

                instructor_performance.append((instructor.name, courses_taught_filter_count, enrollment_count, total_funding_sum, f"{instructor_papers_sum}"))
                print(instructor_performance)
                context = {'instructor_performance': instructor_performance}
                template = loader.get_template('dbApp/admin_dashboard.html')
                return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('dbApp/admin_dashboard.html')
        context = {}
        return HttpResponse(template.render(context, request))

def instructor_dashboard_view(request):
    if request.method == 'GET':
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'course_summary':
                instructor_name = request.GET.get('instructor')
                semester = request.GET.get('semester')
                year = request.GET.get('year')

                # Query to get instructor ID based on name
                instructor = Instructor.objects.get(name=instructor_name)
                instructor_id = instructor.id
                # Query to get courses taught by the instructor in a specific semester and year
                courses_taught = Teaches.objects.values('teacher_id', 'course_id', 'sec_id', 'semester', 'year')
                courses_taught_filter = courses_taught.filter(teacher_id=instructor_id, semester=semester, year=year)

                print(courses_taught_filter)

                # Query to get student enrollments for each course
                course_enrollments = []
                for course in courses_taught_filter:
                    enrollment_count = Takes.objects.filter(course_id=course['course_id'], sec_id=course['sec_id'], semester=course['semester'], year=course['year']).count()
                    course_enrollments.append((f"{course['course_id']} - {course['sec_id']}", enrollment_count))
                
                context = {'course_enrollments': course_enrollments}
                template = loader.get_template('dbApp/instructor_dashboard.html')
                return HttpResponse(template.render(context, request))
            elif action == 'student_enrollment':
                instructor_name = request.GET.get('instructor')
                semester = request.GET.get('semester')
                year = request.GET.get('year')
                course = request.GET.get('course')
                # Query to get instructor ID based on name
                instructor = Instructor.objects.get(name=instructor_name)
                instructor_id = instructor.id
                # Query to get courses taught by the instructor in a specific semester and year
                courses_taught = Teaches.objects.values('teacher_id', 'course_id', 'sec_id', 'semester', 'year')
                courses_taught_filter = courses_taught.filter(teacher_id=instructor_id, semester=semester, year=year)

                print(courses_taught_filter)

                student_enrollments = []
                for course in courses_taught_filter:
                    student_names = Takes.objects.filter(course_id=course['course_id'], sec_id=course['sec_id'], semester=course['semester'], year=course['year'])
                    student_enrollments.append((student_names))
                print(student_enrollments)
                # student_names = Students.objects.filter(student_id=)
                
                context = {'student_enrollments': student_enrollments}
                template = loader.get_template('dbApp/instructor_dashboard.html')
                return HttpResponse(template.render(context, request))

    
    else:
        template = loader.get_template('dbApp/instructor_dashboard.html')
        context = {}
        return HttpResponse(template.render(context, request))

def student_dashboard_view(request):
    template = loader.get_template('dbApp/student_dashboard.html')
    context = {}
    return HttpResponse(template.render(context, request))