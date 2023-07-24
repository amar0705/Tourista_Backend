"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from djangoProject.views import YourModelAPIView, HostAPIView, LoginAPIView, HostPropertyAPIView, LogoutAPIView, \
    PropertyTypeAPIView, StateAPIView, CityAPIView, GuestAPIView, AllPropertiesAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('host/', HostAPIView.as_view()),
    path('guest/', GuestAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('host/property', HostPropertyAPIView.as_view()),
    path('host/property/<int:task_id>/', HostPropertyAPIView.as_view()),
    path('host/logout', LogoutAPIView.as_view()),
    path('state/', StateAPIView.as_view()),
    path('city/', CityAPIView.as_view()),
    path('property_type/', PropertyTypeAPIView.as_view()),
    path('properties/', AllPropertiesAPIView.as_view())
]
