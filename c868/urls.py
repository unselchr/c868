"""
URL configuration for c868 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from c868 import settings
from . import views as views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='dashboard'),
	path('part/<int:pk>/edit/', views.PartDetailView.as_view(), name='partdetail'),
	path('part/<int:pk>/delete/', views.PartDeleteView.as_view(), name='partdelete'),
	path('part/create/', views.PartCreateView.as_view(), name='partcreate'),
	path('part/create/<int:parent_pk>/', views.PartCreateView.as_view(), name='partcreatesubpart'),
	path('users/', views.UserListView.as_view(), name='userlist'),
	path('users/<int:pk>/edit/', views.UserDetailView.as_view(), name='userdetail'),
	path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='userdelete'),
	path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password-reset/', views.PasswordChange.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
	path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
]

if settings.DEBUG:
	urlpatterns.append(path(r'__debug__/', include(debug_toolbar.urls)))

handler404 = views.error_404
# handler500 = views.error_500
handler403 = views.error_403
handler400 = views.error_400
