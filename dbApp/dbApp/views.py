from django.http import HttpResponse
import mysql.connector

from django.template import loader


def index(request):

    template = loader.get_template('dbApp/login.html')
    context = { }

    return HttpResponse(template.render(context, request))
