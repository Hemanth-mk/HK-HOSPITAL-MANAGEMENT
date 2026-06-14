# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Restored to valid standard admin module routing
    path('', include('main.urls')),   # Connects application sub-routing paths securely
]