import re
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http.response import HttpResponseServerError, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.core.exceptions import BadRequest
from django.template import loader
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetView
from . import forms as forms
from . import models as models
from .utils import check_roles

def logout_view(request):
    logout(request)
    # Redirect to a desired page after logout, e.g., the login page
    return redirect('login/') 

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

def error_400(request, exception):
    t = loader.get_template('error_400.html')
    response = HttpResponseBadRequest(t.render({'message': exception.message}))
    response.status_code = 400
    return response

def signup(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=user.email, password=raw_password)
            if user is not None:
                # login(request, user)
                print('user created')
            else:
                print("user is not authenticated")
            return redirect('userlist')
    else:
        form = forms.CustomUserCreationForm()
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

class HomeView(LoginRequiredMixin, generic.ListView):
    template_name = 'dashboard.html'
    model = models.Part
    ordering = ['-pk']
    paginate_by = 20
    
    def get_queryset(self):
        parts = super().get_queryset()
        source = self.request.GET.get('source')
        if source:
            parts = parts.filter(source=source)
        search = self.request.GET.get('search')
        if search:
            search = search.lower()
            parts = parts.filter(
                Q(name__icontains=search)|
                Q(sku__icontains=search)|
                Q(source_id__icontains=search)|
                Q(price__icontains=search))
        return parts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['source_choices'] = models.Part.SOURCE_CHOICES
        params = []

        source = self.request.GET.get('source')
        if source:
            params.append('source=%s'%source)
            context['source']=source
        
        search = self.request.GET.get('search')
        if search:
            params.append('search=%s'%search)
            context['search']=search
        
        qs = '&'.join(params)
        
        context['source_qs'] = re.sub(r'source=[A-Z]+&?', '', qs)
        context['search_qs'] = re.sub(r'search=[^&]+&?', '', qs)
       
        return context

@check_roles
class PartDetailView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'part_detail.html'
    allowed_roles = [models.Role.ADMIN, models.Role.USER]
    model = models.Part
    form_class = forms.EditPartForm
    success_url = reverse_lazy('dashboard')

@check_roles
class PartCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'part_create.html'
    allowed_roles = [models.Role.ADMIN, models.Role.USER]
    success_url = reverse_lazy('dashboard')
    def get_form_class(self):
        if self.kwargs.get('parent_pk'):
            return forms.CreateSubPartForm
        return forms.CreatePartForm
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.kwargs.get('parent_pk'):
            kwargs['parent_pk'] = self.kwargs['parent_pk']
        return kwargs
    def form_valid(self, form):
        newpart = form.save()
        parent_pk = form.cleaned_data.get('parent_pk')
        if parent_pk:
            parent = models.Part.objects.get(pk=parent_pk)
            parent.sub_parts.add(newpart)
            parent.save()
        return super().form_valid(form)

@check_roles
class PartDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    allowed_roles = [models.Role.ADMIN, models.Role.USER]
    success_url = reverse_lazy('dashboard')
    model = models.Part
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        pk = kwargs['pk']
        part = models.Part.objects.get(pk=pk)
        if part.sub_parts.exists():
            raise BadRequest('Cannot delete a part that has sub-parts. You must delete sub-parts first.')
        return super().delete(request, *args, **kwargs)

@check_roles
class UserListView(LoginRequiredMixin, generic.ListView):
    template_name = 'userlist.html'
    allowed_roles = [models.Role.ADMIN]
    model = models.CustomUser
    ordering = ['-pk']
    paginate_by = 20

@check_roles
class UserDetailView(LoginRequiredMixin, generic.edit.UpdateView):
    template_name = 'basic_form.html'
    allowed_roles = [models.Role.ADMIN]
    model = models.CustomUser
    fields = ['role']
    success_url = reverse_lazy('userlist')

@check_roles
class UserDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    allowed_roles = [models.Role.ADMIN]
    model = models.CustomUser
    success_url = reverse_lazy('userlist')
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)