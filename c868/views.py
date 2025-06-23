from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden
from django.template import loader
# from users.utils import check_roles
# from users.models import Role
from django.contrib.auth.mixins import LoginRequiredMixin

def error_404(request, exception):
    t = loader.get_template('error_404.html')
    response = HttpResponseNotFound(t.render())
    response.status_code = 404
    return response

def error_500(request):
    t = loader.get_template('error_500.html')
    response = HttpResponseServerError(t.render())
    response.status_code = 500
    return response

def error_403(request, exception):
    t = loader.get_template('error_403.html')
    response = HttpResponseForbidden(t.render())
    response.status_code = 403
    return response

class HomeView(generic.base.TemplateView):
    template_name = 'dashboard.html'

