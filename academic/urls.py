"""academic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from academic import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('staff/', admin.site.urls),
    path('admin/login', views.adminlogin),
    path('', views.index),
    path('login/', views.login_user),
    path('dashboard/', views.dashboard),
    path('username/', views.username),
    path('logout/', views.logout_user),
    path('register/', views.register),
    path('index/', views.index),
    path('messages/', views.message_list),
    path('write_message/', views.write_message),
]

urlpatterns = format_suffix_patterns(urlpatterns)