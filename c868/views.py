from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http.response import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden
from django.template import loader
# from users.utils import check_roles
# from users.models import Role
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import PasswordResetView
from . import forms as forms
from . import models as models
from .utils import check_roles

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

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                # login(request, user)
                print('user created')
            else:
                print("user is not authenticated")
            return redirect('dashboard')
    else:
        form = forms.UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class PasswordChange(SuccessMessageMixin, PasswordResetView):
    
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'Reset your password'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('dashboard')

class HomeView(LoginRequiredMixin, generic.base.TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parts = models.Part.objects.filter()
        context['parts'] = parts
        return context

@check_roles
class UserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'user_management.html'
    allowed_roles = [models.Role.ADMIN]
    model = models.CustomUser
    paginate_by = 20