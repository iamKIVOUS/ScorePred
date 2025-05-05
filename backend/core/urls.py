# backend/core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin
    path('api/basketball/', include('basketball.urls')),  # Include basketball URLs
]
